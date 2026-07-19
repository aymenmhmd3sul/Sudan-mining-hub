from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GoldPrice(BaseModel):
    price: float
    currency: str
    unit: str
    trend: str
    manual_override: Optional[bool] = False

class MarketActivity(BaseModel):
    volume_24h: float
    active_deals: int
    active_merchants: int

class OracleStatus(BaseModel):
    status: str
    sources: List[str]
    last_sync: datetime

class MarketStatsResponse(BaseModel):
    gold_spot: GoldPrice
    gold_local: GoldPrice
    premium_percent: float
    market_activity: MarketActivity
    oracle: OracleStatus

class PriceUpdateRequest(BaseModel):
    price: float
    currency: str = "SDG"
    reason: str
