from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional

from sqlalchemy import text
from app.core.db import SessionLocal
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/api/admin/users",
    tags=["Admin Users Management"]
)


def verify_admin_role(current_user=Depends(get_current_user)):
    if str(current_user.role) not in ["ADMIN", "admin", "superadmin", "UserRole.ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بدخول لوحة التحكم الإدارية"
        )
    return current_user


@router.get("")
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


@router.post("/toggle-status")
def toggle_user_status(
    user_email: str,
    new_status: str,
    current_admin=Depends(verify_admin_role)
):
    if new_status not in ["ACTIVE", "BANNED"]:
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
            "status": new_status,
            "email": user_email
        }
    )

    db.commit()
    db.close()

    return {
        "message": f"تم تحديث حالة المستخدم إلى {new_status}"
    }
