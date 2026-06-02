"""
Thin async wrapper around the MetaTrader 5 Python library.
All MT5 calls are blocking, so they run in an executor to avoid blocking
the FastAPI event loop.
"""

import asyncio
import json
import logging
from functools import wraps
from typing import Any

import MetaTrader5 as mt5  # pip install MetaTrader5

from config import settings

log = logging.getLogger("broker")


def _run_sync(func):
    """Decorator: run a sync MT5 call in the default thread-pool executor."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return wrapper


class BrokerConnector:
    def __init__(self):
        self._connected = False
        self._symbol_map: dict[str, str] = json.loads(settings.MT5_SYMBOL_MAP)

    # ── Connection ──────────────────────────────────────────────────────────

    async def connect(self) -> bool:
        for attempt in range(1, settings.MT5_MAX_RETRIES + 1):
            ok = await self._init_mt5()
            if ok:
                self._connected = True
                info = mt5.account_info()
                log.info(
                    "MT5 connected | account=%s server=%s balance=%.2f",
                    info.login if info else "?",
                    info.server if info else "?",
                    info.balance if info else 0.0,
                )
                return True
            log.warning("MT5 init attempt %d/%d failed", attempt, settings.MT5_MAX_RETRIES)
            await asyncio.sleep(2 ** attempt)
        return False

    @_run_sync
    def _init_mt5(self) -> bool:
        kwargs: dict[str, Any] = {
            "login": settings.MT5_LOGIN,
            "password": settings.MT5_PASSWORD,
            "server": settings.MT5_SERVER,
            "timeout": settings.MT5_TIMEOUT_MS,
        }
        if settings.MT5_PATH:
            kwargs["path"] = settings.MT5_PATH
        return mt5.initialize(**kwargs)

    async def disconnect(self):
        await asyncio.get_event_loop().run_in_executor(None, mt5.shutdown)
        self._connected = False
        log.info("MT5 disconnected")

    def is_connected(self) -> bool:
        if not self._connected:
            return False
        # Quick live check
        return mt5.terminal_info() is not None

    # ── Symbol helpers ───────────────────────────────────────────────────────

    def resolve_symbol(self, tv_symbol: str) -> str:
        return self._symbol_map.get(tv_symbol, tv_symbol)

    @_run_sync
    def symbol_info_tick(self, symbol: str):
        return mt5.symbol_info_tick(symbol)

    @_run_sync
    def symbol_info(self, symbol: str):
        return mt5.symbol_info(symbol)

    # ── Order helpers ────────────────────────────────────────────────────────

    @_run_sync
    def _send_order(self, request: dict) -> Any:
        return mt5.order_send(request)

    async def send_order(self, request: dict):
        result = await self._send_order(request)
        if result is None:
            err = mt5.last_error()
            log.error("order_send returned None – MT5 error: %s", err)
            return None
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            log.error(
                "Order failed retcode=%d comment=%s",
                result.retcode,
                result.comment,
            )
        return result

    @_run_sync
    def get_positions(self, symbol: str | None = None):
        if symbol:
            return mt5.positions_get(symbol=symbol)
        return mt5.positions_get()

    @_run_sync
    def _order_check(self, request: dict):
        return mt5.order_check(request)

    async def order_check(self, request: dict):
        return await self._order_check(request)
