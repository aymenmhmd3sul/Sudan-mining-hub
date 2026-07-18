from sqlalchemy.orm import Session
from app.models.commission import CommissionLedger
from app.models.commission_audit import CommissionAuditLog


def update_commission_status(
    db: Session,
    commission_id: int,
    new_status: str,
    changed_by: int,
    reason: str | None = None
):
    commission = (
        db.query(CommissionLedger)
        .filter(CommissionLedger.id == commission_id)
        .first()
    )

    if not commission:
        raise ValueError("Commission not found")

    old_status = commission.status

    if old_status == new_status:
        return commission

    commission.status = new_status

    audit = CommissionAuditLog(
        commission_id=commission.id,
        old_status=old_status,
        new_status=new_status,
        changed_by=changed_by,
        reason=reason
    )

    db.add(audit)
    db.commit()
    db.refresh(commission)

    return commission
