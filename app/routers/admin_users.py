from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional

from app.core.db import SessionLocal
from app.security.auth import get_current_user
from app.models.user import UserRole, UserStatus

router = APIRouter(
    prefix="/api/admin/users",
    tags=["Admin Users Management"]
)


def verify_admin_role(current_user=Depends(get_current_user)):
    role = getattr(current_user.role, "value", current_user.role)
    if str(role).lower() != UserRole.ADMIN.value.lower():
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

    query = "SELECT id, email, role, status, created_at FROM users WHERE 1=1"
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
    active_res = db.execute(
        text("SELECT COUNT(*) FROM users WHERE LOWER(status) = LOWER(:status)"),
        {"status": UserStatus.ACTIVE.value},
    ).scalar() or 0

    suspended_res = db.execute(
        text("SELECT COUNT(*) FROM users WHERE LOWER(status) = LOWER(:status)"),
        {"status": UserStatus.SUSPENDED.value},
    ).scalar() or 0
    
    db.close()

    return {
        "status": "success",
        "data": {
            "total_users": total_res,
            "active_users": active_res,
            "suspended_users": suspended_res
        }
    }


@router.post("/toggle-status")
def toggle_user_status(
    user_email: str,
    new_status: str,
    current_admin=Depends(verify_admin_role)
):
    normalized_status = str(new_status).strip().lower()

    allowed_statuses = {
        UserStatus.ACTIVE.value,
        UserStatus.SUSPENDED.value,
    }

    if normalized_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="حالة حساب غير قانونية"
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
        SET status = :status
        WHERE LOWER(email)=LOWER(:email)
        """),
        {
            "status": normalized_status,
            "email": user_email
        }
    )

    db.commit()
    db.close()

    return {
        "message": f"تم تحديث حالة المستخدم إلى {new_status}"
    }


@router.post("/change-role")
def change_user_role(
    user_email: str,
    new_role: str,
    current_admin=Depends(verify_admin_role)
):
    """تعديل صلاحيات ودور المستخدم"""
    normalized_role = str(new_role).strip().lower()

    allowed_roles = {role.value for role in UserRole}

    if normalized_role not in allowed_roles:
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
            "role": normalized_role,
            "email": user_email
        }
    )

    db.commit()
    db.close()

    return {
        "message": f"تم تغيير دور المستخدم إلى {normalized_role}"
    }
