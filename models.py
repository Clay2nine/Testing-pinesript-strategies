"""Pydantic models matching the Pine Script alert() JSON schemas."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class WebhookAction(str, Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class TradeSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "market"


class WebhookPayload(BaseModel):
    """
    Covers both f_jsonEntry (OPEN) and f_jsonExit (CLOSE) shapes from the
    Pine Script.
    """

    action: WebhookAction
    symbol: str

    # Present in both OPEN and CLOSE
    side: TradeSide
    qty: float = Field(gt=0)

    # OPEN-only fields
    order_type: Optional[OrderType] = None
    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    risk_points: Optional[float] = None
    rr: Optional[float] = None
    score: Optional[int] = None
    session: Optional[str] = None
    reason: Optional[str] = None

    # CLOSE-only fields
    simulated_R: Optional[float] = None

    @field_validator("symbol")
    @classmethod
    def normalise_symbol(cls, v: str) -> str:
        return v.upper().strip()
