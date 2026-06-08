from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class MarketItem(SQLModel, table=True):
    __tablename__ = "market_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str
    description: str
    location: Optional[str] = None
    price: Optional[float] = None
    status: str = Field(default="active")
    contact_locked: bool = Field(default=True)

    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )
