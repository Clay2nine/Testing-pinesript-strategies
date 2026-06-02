"""
TradingView → BlackBull MT5 Webhook Server
Receives JSON alert() payloads from the XAUUSD BlackBull PROP Auto 20/200 Pine Script
and executes / closes trades via MetaTrader 5.

Run:  uvicorn webhook_server:app --host 0.0.0.0 --port 8000
"""

import asyncio
import logging
import hmac
import hashlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse

from config import settings
from trade_manager import TradeManager
from models import WebhookPayload, WebhookAction

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
log = logging.getLogger("webhook")

# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

trade_manager: TradeManager | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global trade_manager
    trade_manager = TradeManager()
    await trade_manager.connect()
    log.info("TradeManager connected – server ready")
    yield
    if trade_manager:
        await trade_manager.disconnect()
    log.info("TradeManager disconnected – server shutdown")


app = FastAPI(title="BB XAUUSD Webhook Bridge", lifespan=lifespan)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _verify_signature(body: bytes, signature: str | None) -> bool:
    """Optional HMAC-SHA256 verification of incoming TradingView payload."""
    if not settings.WEBHOOK_SECRET:
        return True
    if not signature:
        return False
    expected = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature.removeprefix("sha256="))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
async def health():
    connected = trade_manager.is_connected() if trade_manager else False
    return {"status": "ok", "mt5_connected": connected}


@app.post("/webhook")
async def webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
):
    body = await request.body()

    if not _verify_signature(body, x_signature):
        log.warning("Rejected request – invalid signature")
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        data = await request.json()
    except Exception as exc:
        log.error("JSON parse error: %s", exc)
        raise HTTPException(status_code=400, detail=f"Bad JSON: {exc}") from exc

    log.info("Received payload: %s", data)

    try:
        payload = WebhookPayload(**data)
    except Exception as exc:
        log.error("Payload validation error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if not trade_manager or not trade_manager.is_connected():
        log.error("MT5 not connected – attempting reconnect")
        if trade_manager:
            await trade_manager.connect()
        if not trade_manager or not trade_manager.is_connected():
            raise HTTPException(status_code=503, detail="Broker not connected")

    try:
        if payload.action == WebhookAction.OPEN:
            result = await trade_manager.open_trade(payload)
        elif payload.action == WebhookAction.CLOSE:
            result = await trade_manager.close_trade(payload)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {payload.action}")
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("Trade execution error")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return JSONResponse(content=result)
