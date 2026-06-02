"""
Quick smoke-tests – run with:  pytest test_webhook.py -v
No live MT5 connection required; the broker layer is mocked.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def mock_trade_manager():
    """Prevent real MT5 initialisation during tests."""
    with patch("webhook_server.trade_manager") as mock_tm:
        mock_tm.is_connected.return_value = True
        mock_tm.open_trade = AsyncMock(return_value={"status": "ok", "order": 999, "retcode": 10009})
        mock_tm.close_trade = AsyncMock(return_value={"status": "ok", "closed": [{"ticket": 999}]})
        yield mock_tm


@pytest.fixture
def client(mock_trade_manager):
    # Import after mocking so lifespan doesn't fire a real connect
    with patch("webhook_server.TradeManager") as MockTM:
        MockTM.return_value = mock_trade_manager
        # Patch connect so lifespan doesn't block
        mock_trade_manager.connect = AsyncMock(return_value=True)
        mock_trade_manager.disconnect = AsyncMock()

        from webhook_server import app
        with TestClient(app, raise_server_exceptions=True) as c:
            yield c


# ── Helpers ──────────────────────────────────────────────────────────────────

OPEN_BUY = {
    "action": "OPEN",
    "symbol": "XAUUSD",
    "side": "BUY",
    "qty": 0.01,
    "order_type": "market",
    "entry": 2345.50,
    "stop_loss": 2343.00,
    "take_profit": 2347.90,
    "risk_points": 2.50,
    "rr": 1.0,
    "score": 95,
    "session": "NY_LONDON_OVERLAP",
    "reason": "XAU_BFF_SCALP_OB_PLUS_20_200_LONG",
}

OPEN_SELL = {**OPEN_BUY, "side": "SELL", "stop_loss": 2348.00, "take_profit": 2343.00, "reason": "XAU_BFF_SCALP_OB_PLUS_20_200_SHORT"}

CLOSE_BUY = {
    "action": "CLOSE",
    "symbol": "XAUUSD",
    "side": "BUY",
    "qty": 0.01,
    "reason": "TAKE_PROFIT",
    "simulated_R": 1.0,
}


# ── Tests ────────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_open_buy(client, mock_trade_manager):
    r = client.post("/webhook", json=OPEN_BUY)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    mock_trade_manager.open_trade.assert_awaited_once()


def test_open_sell(client, mock_trade_manager):
    r = client.post("/webhook", json=OPEN_SELL)
    assert r.status_code == 200
    mock_trade_manager.open_trade.assert_awaited_once()


def test_close(client, mock_trade_manager):
    r = client.post("/webhook", json=CLOSE_BUY)
    assert r.status_code == 200
    mock_trade_manager.close_trade.assert_awaited_once()


def test_bad_json(client):
    r = client.post("/webhook", content=b"{bad json}", headers={"content-type": "application/json"})
    assert r.status_code == 400


def test_unknown_action(client):
    r = client.post("/webhook", json={**OPEN_BUY, "action": "MODIFY"})
    assert r.status_code == 422


def test_model_symbol_normalised():
    from models import WebhookPayload
    p = WebhookPayload(**{**OPEN_BUY, "symbol": "xauusd"})
    assert p.symbol == "XAUUSD"
