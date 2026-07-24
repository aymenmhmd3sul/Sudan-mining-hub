from fastapi import APIRouter, Depends, HTTPException, Query, Header
from datetime import datetime
from typing import Optional
from app.core.db import get_db_connection
from app.core.dependencies import verify_admin_token

router = APIRouter(prefix="/admin/control", tags=["Admin Control (Offers & Finance)"])

# ==================== [ طبقة الحماية والمصادقة ] ====================

def get_current_admin(current_user=Depends(verify_admin_token)):
    # جلب إيميل الأدمن بعد التحقق التام من صلاحياته برمجياً
    return getattr(current_user, "email", "admin@sudanmininghub.com")

def log_admin_action(admin_email: str, action: str, target_id: str, details: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO security_breach_logs (user_email, attempted_action, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (admin_email, f"ADMIN_{action}", f"Target ID: {target_id} | {details}", datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        pass

# ==================== [ أولاً: رقابة وإدارة الإعلانات ] ====================
