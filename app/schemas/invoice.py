from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from decimal import Decimal

class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PAID = "paid"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class InvoiceBase(BaseModel):
    opportunity_id: int
    buyer_id: int
    seller_id: int
    invoice_number: str
    reference: Optional[str] = None
    status: InvoiceStatus = InvoiceStatus.DRAFT
    subtotal: Decimal = Field(..., decimal_places=2)
    commission: Decimal = Field(Decimal("0.00"), decimal_places=2)
    tax: Decimal = Field(Decimal("0.00"), decimal_places=2)
    total_amount: Decimal = Field(..., decimal_places=2)
    currency: str = "USD"
    notes: Optional[str] = None
    due_date: Optional[datetime] = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
