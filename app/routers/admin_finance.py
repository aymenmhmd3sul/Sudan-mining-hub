from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.core.dependencies import verify_admin_token
from app.models.user import User
from app.models.finance import Invoice, Escrow
from app.models.financial import PaymentTransaction
from app.models.commission import CommissionLedger

router = APIRouter(
    prefix="/api/v1/admin/finance",
    tags=["Admin Finance Control"]
)

def get_current_admin(current_user: User = Depends(verify_admin_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": "admin"
    }

@router.get("/stats")
def get_finance_stats(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """إحصائيات مالية شاملة للوحة التحكم الإدارية"""
    total_invoices = db.query(Invoice).count() if hasattr(Invoice, 'id') else 0
    total_transactions = db.query(PaymentTransaction).count() if hasattr(PaymentTransaction, 'id') else 0
    total_escrows = db.query(Escrow).count() if hasattr(Escrow, 'id') else 0
    total_commissions = db.query(CommissionLedger).count() if hasattr(CommissionLedger, 'id') else 0

    return {
        "status": "success",
        "data": {
            "total_invoices": total_invoices,
            "total_transactions": total_transactions,
            "total_escrows": total_escrows,
            "total_commissions": total_commissions
        }
    }

@router.get("/invoices")
def list_admin_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """عرض كافة الفواتير المسجلة بالنظام"""
    invoices = db.query(Invoice).offset(skip).limit(limit).all()
    return {
        "status": "success",
        "count": len(invoices),
        "data": invoices
    }

@router.get("/commissions")
def list_admin_commissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """سجل العمولات والإيرادات المستحقة"""
    commissions = db.query(CommissionLedger).offset(skip).limit(limit).all()
    return {
        "status": "success",
        "count": len(commissions),
        "data": commissions
    }
