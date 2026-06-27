from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Trader:
    id: str
    name: str
    is_active: bool = True


@dataclass
class BuyerRequest:
    id: str
    buyer_id: str
    title: str
    description: str


@dataclass
class Offer:
    id: str
    trader_id: str
    request_id: str
    price: float
    media_url: Optional[str] = None


@dataclass
class Deal:
    id: str
    offer_id: str
    status: str  # pending / accepted / rejected
    commission: float
