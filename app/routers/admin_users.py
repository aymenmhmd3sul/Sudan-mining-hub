from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import datetime, timezone
from typing import Optional
from app.core.db import get_db_connection
from app.core.security import get_current_user

router = APIRouter(prefix="/api/admin/users", tags=["Admin Users Management"])

def log_admin_action(admin_email: str, action: str, target_user: str, details: str):
    """حفظ سجلات العمليات الإدارية."""
    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO security_breach_logs (user_email, attempted_action, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (admin_email, f"ADMIN_{action}", f"Target: {target_user} | {details}", datetime.now(timezone.utc).isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        pass

def verify_admin_role(current_user: dict = Depends(get_current_user)) -> dict:
    """التحقق الحقيقي والصارم من صلاحية الآدمن بناءً على التوكن الموحد."""
    if current_user.get("role") != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بدخول لوحة التحكم الإدارية"
        )
    return current_user

@router.get("")
def list_users(
    status_filter: Optional[str] = Query(None, alias="status", description="ACTIVE, BANNED, PENDING_VERIFICATION"),
    current_admin: dict = Depends(verify_admin_role)
):
    conn = get_db_connection()
    # استبعاد trader_category مؤقتاً لعدم وجود العمود في الجدول الحالي
    query = "SELECT id, email, role, status, created_at FROM users WHERE 1=1"
    params = []
    
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)
        
    users = conn.execute(query, params).fetchall()
    conn.close()
    return {"total": len(users), "users": [dict(u) for u in users]}

@router.post("/toggle-status")
def toggle_user_status(
    user_email: str,
    new_status: str,
    current_admin: dict = Depends(verify_admin_role)
):
    if new_status not in ["ACTIVE", "BANNED"]:
        raise HTTPException(status_code=400, detail="حالة حساب غير قانونية")
        
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(TRIM(email)) = ?", (user_email.strip().lower(),)).fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
        
    conn.execute("UPDATE users SET status = ? WHERE LOWER(TRIM(email)) = ?", (new_status, user_email.strip().lower()))
    conn.commit()
    conn.close()
    
    log_admin_action(
        admin_email=current_admin["email"],
        action="TOGGLE_STATUS",
        target_user=user_email,
        details=f"تم تغيير حالة الحساب إلى {new_status}"
    )
    return {"message": f"تم تحديث حالة المستخدم {user_email} بنجاح إلى {new_status}"}
