from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from decimal import Decimal

class EscrowStatus(str, Enum):
    PENDING = "pending"
    FUNDED = "funded"
    RELEASED = "released"
    REFUNDED = "refunded"
    DISPUTED = "disputed"

class EscrowBase(BaseModel):
    invoice_id: int
    amount: Decimal = Field(..., decimal_places=2)
    currency: str = "USD"
    status: EscrowStatus = EscrowStatus.PENDING
    provider: Optional[str] = None
    transaction_reference: Optional[str] = None
    dispute_id: Optional[int] = None

class EscrowCreate(EscrowBase):
    pass

class Escrow(EscrowBase):
    id: int
    created_at: datetime
    deposited_at: Optional[datetime] = None
    released_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None

    class Config:
        from_attributes = True
