from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, nullable=False)
    buyer_id = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=False)

    invoice_number = Column(String(100), unique=True, index=True)
    reference = Column(String(100), nullable=True)

    status = Column(String(50), default="draft")

    subtotal = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)

    currency = Column(String(10), default="USD")
    notes = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Escrow(Base):
    __tablename__ = "escrow"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoice.id"),
        unique=True
    )

    invoice = relationship("Invoice")

    amount = Column(Float, nullable=False)

    currency = Column(String(10), default="USD")

    status = Column(String(50), default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
