from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.core.dependencies import verify_admin_token
from app.models.user import User
from app.models.mining_site import MiningSite

router = APIRouter(
    prefix="/api/v1/admin/mining",
    tags=["Admin Mining Control"]
)

def get_current_admin(current_user: User = Depends(verify_admin_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": "admin"
    }

@router.get("/stats")
def get_mining_stats(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """إحصائيات مواقع التعدين والآبار للوحة التحكم الإدارية"""
    total_sites = db.query(MiningSite).count() if hasattr(MiningSite, 'id') else 0

    return {
        "status": "success",
        "data": {
            "total_sites": total_sites
        }
    }

@router.get("/sites")
def list_admin_sites(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """عرض كافة مواقع التعدين المسجلة بالنظام"""
    sites = db.query(MiningSite).offset(skip).limit(limit).all()
    return {
        "status": "success",
        "count": len(sites),
        "data": sites
    }
