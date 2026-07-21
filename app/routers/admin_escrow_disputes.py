from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.core.dependencies import verify_admin_token
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/admin/escrow-disputes",
    tags=["Admin Escrow & Disputes Control"]
)

def get_current_admin(current_user: User = Depends(verify_admin_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": "admin"
    }

# --- Escrow Summary ---
@router.get("/escrow/summary")
def get_escrow_summary(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """إحصائيات المبالغ والضمانات المالية المعلقة"""
    try:
        escrow_count = db.execute(text("SELECT COUNT(*) FROM escrows")).scalar() if db.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'escrows')")).scalar() else 0
    except Exception:
        escrow_count = 0

    return {
        "status": "success",
        "data": {
            "active_escrows": escrow_count,
            "escrow_system_status": "Operational"
        }
    }

# --- Disputes Summary ---
@router.get("/disputes/summary")
def get_disputes_summary(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """ملخص النزاعات والشكاوى التجارية بين الأطراف"""
    try:
        disputes_count = db.execute(text("SELECT COUNT(*) FROM disputes")).scalar() if db.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'disputes')")).scalar() else 0
    except Exception:
        disputes_count = 0

    return {
        "status": "success",
        "data": {
            "open_disputes": disputes_count,
            "dispute_resolution_status": "Active"
        }
    }
