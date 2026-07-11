from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from enum import Enum
from datetime import datetime
from decimal import Decimal
from .common import PaymentProvider, PaymentMethod, Currency

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentBase(BaseModel):
    invoice_id: int
    escrow_id: Optional[int] = None
    amount: Decimal = Field(..., decimal_places=2)
    currency: Currency = Currency.USD
    provider: PaymentProvider = PaymentProvider.OTHER
    method: PaymentMethod = PaymentMethod.WIRE
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_reference: Optional[str] = None
    failure_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    paid_at: Optional[datetime] = None

    class Config:
        orm_mode = True
