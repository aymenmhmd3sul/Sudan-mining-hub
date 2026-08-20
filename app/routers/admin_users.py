from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException, Query, Form, status
from typing import Optional

from app.core.db import SessionLocal
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/api/admin/users",
    tags=["Admin Users Management"]
)


def verify_admin_role(current_user=Depends(get_current_user)):
    role = getattr(current_user.role, "value", current_user.role)
    is_admin = str(role).lower() in {
        "admin",
        "superadmin",
    }

    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بدخول لوحة التحكم الإدارية"
        )

    return current_user


@router.get("/manage")
def list_users(
    status_filter: Optional[str] = Query(None, alias="status"),
    current_admin=Depends(verify_admin_role)
):
    db = SessionLocal()

    query = "SELECT id, name, email, phone, role, status, created_at FROM users WHERE 1=1"
    params = {}

    if status_filter:
        query += " AND status = :status"
        params["status"] = status_filter

    result = db.execute(text(query), params)
    users = [dict(row._mapping) for row in result.fetchall()]

    db.close()

    return {
        "total": len(users),
        "users": users
    }


@router.get("/stats")
def get_user_stats(current_admin=Depends(verify_admin_role)):
    """إحصائيات المستخدمين والهوية للوحة التحكم الإدارية"""
    db = SessionLocal()
    
    total_res = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
    active_res = db.execute(text("SELECT COUNT(*) FROM users WHERE LOWER(status) = 'active'")).scalar() or 0
    banned_res = db.execute(text("SELECT COUNT(*) FROM users WHERE LOWER(status) = 'suspended'")).scalar() or 0
    
    db.close()

    return {
        "status": "success",
        "data": {
            "total_users": total_res,
            "active_users": active_res,
            "banned_users": banned_res
        }
    }


@router.post("/toggle-status")
def toggle_user_status(
    user_email: str = Form(...),
    new_status: str = Form(...),
    current_admin=Depends(verify_admin_role)
):
    status_map = {
        "ACTIVE": ("active", True),
        "SUSPENDED": ("suspended", False),
        "PENDING": ("pending", False),
        "REJECTED": ("rejected", False),
        "BANNED": ("suspended", False),
    }

    normalized_status = str(new_status).strip().upper()

    if normalized_status not in status_map:
        raise HTTPException(
            status_code=400,
            detail="حالة حساب غير قانونية"
        )

    db_status, db_is_active = status_map[normalized_status]

    db = SessionLocal()

    result = db.execute(
        text("SELECT id FROM users WHERE LOWER(email)=LOWER(:email)"),
        {"email": user_email}
    )

    user = result.fetchone()

    if not user:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="المستخدم غير موجود"
        )

    db.execute(
        text("""
        UPDATE users
        SET status = :status,
            is_active = :is_active
        WHERE LOWER(email)=LOWER(:email)
        """),
        {
            "status": db_status,
            "is_active": db_is_active,
            "email": user_email
        }
    )

    db.commit()
    db.close()

    return {
        "message": f"تم تحديث حالة المستخدم إلى {db_status}",
        "status": db_status,
        "is_active": db_is_active
    }


@router.post("/change-role")
def change_user_role(
    user_email: str,
    new_role: str,
    current_admin=Depends(verify_admin_role)
):
    """تعديل صلاحيات ودور المستخدم"""
    role_map = {
        "ADMIN": "admin",
        "admin": "admin",
        "MERCHANT": "merchant",
        "merchant": "merchant",
        "SELLER": "merchant",
        "seller": "merchant",
        "BUYER": "buyer",
        "buyer": "buyer",
        "AGENT": "agent",
        "agent": "agent",
        "USER": "buyer",
        "user": "buyer",
    }

    normalized_role = str(new_role).strip()
    db_role = role_map.get(normalized_role)
    if db_role is None:
        db_role = role_map.get(normalized_role.upper())

    if db_role is None:
        raise HTTPException(
            status_code=400,
            detail="دور غير صالح"
        )

    db = SessionLocal()

    result = db.execute(
        text("SELECT id FROM users WHERE LOWER(email)=LOWER(:email)"),
        {"email": user_email}
    )

    user = result.fetchone()

    if not user:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="المستخدم غير موجود"
        )

    db.execute(
        text("""
        UPDATE users
        SET role = :role
        WHERE LOWER(email)=LOWER(:email)
        """),
        {
            "role": db_role,
            "email": user_email
        }
    )

    db.commit()
    db.close()

    return {
        "message": f"تم تغيير دور المستخدم إلى {db_role}",
        "role": db_role
    }
