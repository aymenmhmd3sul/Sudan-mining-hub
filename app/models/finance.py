from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, Column, Numeric
from decimal import Decimal
from datetime import datetime
from app.schemas.invoice import InvoiceStatus
from app.schemas.escrow import EscrowStatus

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: int
    buyer_id: int
    seller_id: int
    invoice_number: str = Field(unique=True, index=True)
    status: InvoiceStatus = Field(default=InvoiceStatus.DRAFT)
    
    subtotal: Decimal = Field(default=Decimal("0.00"), sa_column=Column(Numeric(12, 2)))
    total_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(Numeric(12, 2)))
    
    currency: str = "USD"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # فرض علاقة 1:1 برمجياً
    escrow: Optional["Escrow"] = Relationship(
        back_populates="invoice",
        sa_relationship_kwargs={"uselist": False}
    )

class Escrow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoice.id", unique=True)
    
    amount: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    currency: str = "USD"
    status: EscrowStatus = Field(default=EscrowStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    invoice: Invoice = Relationship(back_populates="escrow")
