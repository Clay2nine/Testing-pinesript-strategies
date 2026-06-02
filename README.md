# XAUUSD BlackBull PROP Auto – Webhook Bridge

Receives TradingView `alert()` JSON payloads from the **XAUUSD BlackBull PROP Auto 20/200 v1.1** Pine Script indicator and executes / closes trades on your BlackBull MT5 account in real time.

---

## Architecture

```
TradingView alert()
     │  JSON over HTTPS
     ▼
webhook_server.py  (FastAPI, port 8000)
     │
     ▼
trade_manager.py   (validate, size, route)
     │
     ▼
broker_connector.py  (MetaTrader5 Python library)
     │
     ▼
BlackBull MT5 terminal
```

---

## Quick Start

### 1 – Prerequisites

| Requirement | Notes |
|---|---|
| Windows VPS (or local PC) | MetaTrader5 Python library only works on Windows |
| BlackBull MT5 terminal installed | Download from your BlackBull portal |
| Python 3.11+ | |
| Public HTTPS URL | ngrok, Cloudflare Tunnel, or a VPS with a domain |

### 2 – Install

```bash
git clone https://github.com/clay2nine/testing-pinesript-strategies.git
cd testing-pinesript-strategies
pip install -r requirements.txt
```

### 3 – Configure

```bash
copy .env.example .env       # Windows
# or
cp .env.example .env         # Linux/Mac
```

Edit `.env` with your BlackBull MT5 credentials:

```ini
MT5_LOGIN=12345678
MT5_PASSWORD=YourPassword
MT5_SERVER=BlackBull-Live
```

### 4 – Run

```bash
uvicorn webhook_server:app --host 0.0.0.0 --port 8000
```

Expose port 8000 publicly (e.g. with ngrok):

```bash
ngrok http 8000
```

### 5 – Set up TradingView alert

1. Add the **XAUUSD BlackBull PROP Auto 20/200 v1.1** indicator to your 5m XAUUSD chart.
2. Create a new alert → **Any alert() function call**.
3. Set **Alert frequency** → **Once Per Bar Close**.
4. In **Notifications → Webhook URL**, enter:
   ```
   https://your-domain.com/webhook
   ```
5. Leave the message body as-is (the indicator sends JSON automatically via `alert()`).

---

## Payload Reference

### OPEN (entry signal)

```json
{
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
  "reason": "XAU_BFF_SCALP_OB_PLUS_20_200_LONG"
}
```

### CLOSE (TP / SL / time exit)

```json
{
  "action": "CLOSE",
  "symbol": "XAUUSD",
  "side": "BUY",
  "qty": 0.01,
  "reason": "TAKE_PROFIT",
  "simulated_R": 1.0
}
```

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | MT5 connection status |
| `POST` | `/webhook` | Receives TradingView alerts |

---

## Security

Set `WEBHOOK_SECRET` in `.env` to a long random string and pass it as the
`X-Signature: sha256=<hmac>` header in your TradingView webhook URL, or leave
blank to skip signature checking during development.

---

## Tests

```bash
pip install pytest httpx
pytest test_webhook.py -v
```

---

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `MT5_LOGIN` | — | MT5 account number |
| `MT5_PASSWORD` | — | MT5 password |
| `MT5_SERVER` | — | Broker server name |
| `MT5_PATH` | auto | Path to `terminal64.exe` |
| `MT5_SYMBOL_MAP` | `{"XAUUSD":"XAUUSD"}` | TV→MT5 symbol mapping |
| `DEFAULT_MAGIC` | `202001` | EA magic number |
| `DEVIATION_POINTS` | `20` | Max slippage in points |
| `USE_SL_TP` | `true` | Attach SL/TP to order |
| `FILL_MODE` | `IOC` | `IOC`, `FOK`, or `RETURN` |
| `WEBHOOK_SECRET` | _(blank)_ | HMAC secret (optional) |

---

## Disclaimer

This software is for educational and personal use only.
Always test on a **demo account** before going live.
Automated trading involves substantial risk of loss.
