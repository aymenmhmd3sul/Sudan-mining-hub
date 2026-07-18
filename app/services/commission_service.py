from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.commission import CommissionLedger
from app.models.operations import SystemSetting


DEFAULT_COMMISSION = Decimal("0.02")


def get_commission_rate(db: Session) -> Decimal:
    setting = (
        db.query(SystemSetting)
        .filter(SystemSetting.key == "commission_rate")
        .first()
    )

    if setting:
        return Decimal(setting.value)

    return DEFAULT_COMMISSION


def create_commission(
    db: Session,
    invoice,
    transaction_id: int
):
    existing = (
        db.query(CommissionLedger)
        .filter(
            CommissionLedger.transaction_id == transaction_id
        )
        .first()
    )

    if existing:
        return existing

    rate = get_commission_rate(db)

    amount = invoice.total_amount * rate

    commission = CommissionLedger(
        invoice_id=invoice.id,
        transaction_id=transaction_id,
        seller_id=invoice.seller_id,
        amount=amount,
        commission_type="PERCENTAGE",
        status="PENDING"
    )

    db.add(commission)

    return commission
