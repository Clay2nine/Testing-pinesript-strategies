"""
Central configuration – values come from environment variables or a .env file.
Copy .env.example → .env and fill in your credentials.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # ── MetaTrader 5 ────────────────────────────────────────────────────────
    MT5_LOGIN: int = 0
    MT5_PASSWORD: str = ""
    MT5_SERVER: str = ""                # e.g. "BlackBull-Live"
    MT5_PATH: str = ""                  # full path to terminal64.exe, or "" to auto-detect
    MT5_TIMEOUT_MS: int = 10_000        # connection timeout
    MT5_MAX_RETRIES: int = 3

    # ── Order defaults ───────────────────────────────────────────────────────
    # Symbol as it appears in MT5 (may differ from TV symbol)
    MT5_SYMBOL_MAP: str = '{"XAUUSD":"XAUUSD"}'   # JSON string {"TV":"MT5"}
    DEFAULT_MAGIC: int = 202001                     # EA magic number
    DEVIATION_POINTS: int = 20                      # max slippage in points
    USE_SL_TP: bool = True                          # send SL/TP with order
    FILL_MODE: str = "IOC"                          # IOC | FOK | RETURN

    # ── Webhook security ─────────────────────────────────────────────────────
    WEBHOOK_SECRET: str = ""   # leave blank to skip HMAC check

    # ── Logging ──────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"


settings = Settings()
