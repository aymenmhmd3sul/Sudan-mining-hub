from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from typing import Optional, List
import sqlite3

router = APIRouter(prefix="/admin/users", tags=["Admin Users Management"])

DB_PATH = "local.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_admin_action(admin_email: str, action: str, target_user: str, details: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            INSERT INTO security_breach_logs (user_email, attempted_action, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (admin_email, f"ADMIN_{action}", f"Target: {target_user} | {details}", datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        pass

def verify_admin():
    return "admin_chief@gold.sd"

@router.get("")
def list_users(
    status: Optional[str] = Query(None, description="ACTIVE, BANNED, PENDING_VERIFICATION"),
    category: Optional[str] = Query(None, description="LIGHT_EQUIPMENT, HEAVY_EQUIPMENT, ASSETS_FACILITIES"),
    admin_email: str = Depends(verify_admin)
):
    conn = get_db_connection()
    query = "SELECT id, email, role, trader_category, status, created_at FROM users WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    if category:
        query += " AND trader_category = ?"
        params.append(category)
        
    users = conn.execute(query, params).fetchall()
    conn.close()
    return {"total": len(users), "users": [dict(u) for u in users]}

@router.post("/toggle-status")
def toggle_user_status(
    user_email: str,
    new_status: str,
    admin_email: str = Depends(verify_admin)
):
    if new_status not in ["ACTIVE", "BANNED"]:
        raise HTTPException(status_code=400, detail="حالة حساب غير قانونية")
        
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (user_email,)).fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
        
    conn.execute("UPDATE users SET status = ? WHERE email = ?", (new_status, user_email))
    conn.commit()
    conn.close()
    
    log_admin_action(
        admin_email=admin_email,
        action="TOGGLE_STATUS",
        target_user=user_email,
        details=f"تم تغيير حالة الحساب إلى {new_status}"
    )
    
    return {"message": f"تم تحديث حالة المستخدم {user_email} بنجاح إلى {new_status}"}

@router.post("/update-category")
def update_trader_category(
    trader_email: str,
    category: str,
    admin_email: str = Depends(verify_admin)
):
    if category not in ["LIGHT_EQUIPMENT", "HEAVY_EQUIPMENT", "ASSETS_FACILITIES"]:
        raise HTTPException(status_code=400, detail="تصنيف تجاري غير مدرج بالنظام")
        
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (trader_email,)).fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
        
    conn.execute("UPDATE users SET trader_category = ? WHERE email = ?", (category, trader_email))
    conn.commit()
    conn.close()
    
    log_admin_action(
        admin_email=admin_email,
        action="UPDATE_CATEGORY",
        target_user=trader_email,
        details=f"تم ترقية/تعديل تصنيف التاجر إلى {category}"
    )
    
    return {"message": f"تم تحديث تصنيف التاجر {trader_email} إلى {category}"}