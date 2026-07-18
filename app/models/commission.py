from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class CommissionLedger(Base):
    __tablename__ = "commission_ledger"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("invoice.id"),
        nullable=False
    )

    transaction_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("financial_transactions.id"),
        nullable=True
    )

    seller_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        nullable=False
    )

    commission_type: Mapped[str] = mapped_column(
        String(20),
        default="PERCENTAGE"
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
