"""
High-level trade orchestration layer.
Translates validated WebhookPayload objects into MT5 order_send() calls.
"""

import logging
import json
from typing import Any

import MetaTrader5 as mt5

from broker_connector import BrokerConnector
from config import settings
from models import WebhookPayload, TradeSide

log = logging.getLogger("trade_manager")

_FILL_MAP = {
    "IOC": mt5.ORDER_FILLING_IOC,
    "FOK": mt5.ORDER_FILLING_FOK,
    "RETURN": mt5.ORDER_FILLING_RETURN,
}


class TradeManager:
    def __init__(self):
        self._broker = BrokerConnector()

    async def connect(self):
        return await self._broker.connect()

    async def disconnect(self):
        await self._broker.disconnect()

    def is_connected(self) -> bool:
        return self._broker.is_connected()

    # ── Open ──────────────────────────────────────────────────────────────

    async def open_trade(self, payload: WebhookPayload) -> dict[str, Any]:
        mt5_symbol = self._broker.resolve_symbol(payload.symbol)
        await self._ensure_symbol(mt5_symbol)

        tick = await self._broker.symbol_info_tick(mt5_symbol)
        if tick is None:
            raise RuntimeError(f"Could not get tick for {mt5_symbol}")

        info = await self._broker.symbol_info(mt5_symbol)
        digits = info.digits if info else 5
        volume_min = info.volume_min if info else 0.01
        volume_step = info.volume_step if info else 0.01

        is_buy = payload.side == TradeSide.BUY
        price = tick.ask if is_buy else tick.bid
        order_type = mt5.ORDER_TYPE_BUY if is_buy else mt5.ORDER_TYPE_SELL

        volume = self._normalise_volume(payload.qty, volume_min, volume_step)

        request: dict[str, Any] = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": mt5_symbol,
            "volume": volume,
            "type": order_type,
            "price": round(price, digits),
            "deviation": settings.DEVIATION_POINTS,
            "magic": settings.DEFAULT_MAGIC,
            "comment": f"TV {payload.reason or 'AUTO'}"[:31],
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": _FILL_MAP.get(settings.FILL_MODE, mt5.ORDER_FILLING_IOC),
        }

        if settings.USE_SL_TP:
            if payload.stop_loss is not None:
                request["sl"] = round(payload.stop_loss, digits)
            if payload.take_profit is not None:
                request["tp"] = round(payload.take_profit, digits)

        log.info("Opening %s %s x%.2f | SL=%.5f TP=%.5f score=%s",
                 payload.side, mt5_symbol, volume,
                 payload.stop_loss or 0, payload.take_profit or 0, payload.score)

        result = await self._broker.send_order(request)
        if result is None:
            return {"status": "error", "detail": "order_send returned None"}

        outcome = {
            "status": "ok" if result.retcode == mt5.TRADE_RETCODE_DONE else "error",
            "retcode": result.retcode,
            "order": result.order,
            "volume": result.volume,
            "price": result.price,
            "comment": result.comment,
            "side": payload.side,
            "symbol": mt5_symbol,
            "sl": request.get("sl"),
            "tp": request.get("tp"),
            "score": payload.score,
            "session": payload.session,
        }
        log.info("Open result: %s", outcome)
        return outcome

    # ── Close ─────────────────────────────────────────────────────────────

    async def close_trade(self, payload: WebhookPayload) -> dict[str, Any]:
        mt5_symbol = self._broker.resolve_symbol(payload.symbol)
        positions = await self._broker.get_positions(symbol=mt5_symbol)

        if not positions:
            log.warning("CLOSE received but no open positions for %s", mt5_symbol)
            return {"status": "noop", "detail": "no open positions"}

        results = []
        for pos in positions:
            # Only close positions that match direction from Pine Script signal
            is_buy_pos = pos.type == mt5.POSITION_TYPE_BUY
            signal_is_buy = payload.side == TradeSide.BUY

            # Pine CLOSE side = direction of the trade being closed
            if is_buy_pos != signal_is_buy:
                continue

            tick = await self._broker.symbol_info_tick(mt5_symbol)
            info = await self._broker.symbol_info(mt5_symbol)
            digits = info.digits if info else 5

            close_price = tick.bid if is_buy_pos else tick.ask
            close_type = mt5.ORDER_TYPE_SELL if is_buy_pos else mt5.ORDER_TYPE_BUY

            request: dict[str, Any] = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": mt5_symbol,
                "volume": pos.volume,
                "type": close_type,
                "position": pos.ticket,
                "price": round(close_price, digits),
                "deviation": settings.DEVIATION_POINTS,
                "magic": settings.DEFAULT_MAGIC,
                "comment": f"TV {payload.reason or 'CLOSE'}"[:31],
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": _FILL_MAP.get(settings.FILL_MODE, mt5.ORDER_FILLING_IOC),
            }

            log.info("Closing ticket=%d %s x%.2f | reason=%s R=%.2f",
                     pos.ticket, mt5_symbol, pos.volume,
                     payload.reason, payload.simulated_R or 0.0)

            result = await self._broker.send_order(request)
            if result is None:
                results.append({"ticket": pos.ticket, "status": "error"})
                continue

            results.append({
                "ticket": pos.ticket,
                "status": "ok" if result.retcode == mt5.TRADE_RETCODE_DONE else "error",
                "retcode": result.retcode,
                "comment": result.comment,
                "reason": payload.reason,
                "simulated_R": payload.simulated_R,
            })

        if not results:
            return {"status": "noop", "detail": "no matching direction positions found"}

        log.info("Close results: %s", results)
        return {"status": "ok", "closed": results}

    # ── Helpers ───────────────────────────────────────────────────────────

    async def _ensure_symbol(self, symbol: str):
        """Make sure the symbol is visible/subscribed in MarketWatch."""
        info = await self._broker.symbol_info(symbol)
        if info is None or not info.visible:
            import MetaTrader5 as _mt5
            import asyncio
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: _mt5.symbol_select(symbol, True))

    @staticmethod
    def _normalise_volume(qty: float, vol_min: float, vol_step: float) -> float:
        if qty < vol_min:
            return vol_min
        # Round to nearest valid step
        steps = round((qty - vol_min) / vol_step)
        return round(vol_min + steps * vol_step, 8)
