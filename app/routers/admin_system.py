from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.database import get_db
from app.core.dependencies import verify_admin_token
from app.models.user import User
from app.models.commission_audit import CommissionAuditLog

router = APIRouter(
    prefix="/api/v1/admin/system",
    tags=["Admin System & Operations Control"]
)

def get_current_admin(current_user: User = Depends(verify_admin_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": "admin"
    }

# --- Analytics & Live System Summary ---
@router.get("/analytics/summary")
def get_system_analytics(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """إحصائيات حقيقية من قاعدة البيانات لمركز القيادة"""
    total_users = db.query(func.count(User.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
    
    return {
        "status": "success",
        "data": {
            "metrics": {
                "total_users": total_users,
                "active_users": active_users,
                "system_status": "Operational"
            }
        }
    }

@router.get("/reports/overview")
def get_system_reports(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """تقارير العمليات الحية"""
    total_users = db.query(func.count(User.id)).scalar() or 0
    return {
        "status": "success",
        "data": {
            "total_registered_entities": total_users,
            "data_source": "Live Production DB"
        }
    }

# --- Audit Logs ---
@router.get("/audit/logs")
def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """سجلات المراجعة والتدقيق الفعلية من قاعدة البيانات"""
    try:
        logs = db.query(CommissionAuditLog).offset(skip).limit(limit).all()
        return {
            "status": "success",
            "count": len(logs),
            "data": logs
        }
    except Exception as e:
        return {
            "status": "success",
            "count": 0,
            "data": [],
            "error": str(e)
        }
