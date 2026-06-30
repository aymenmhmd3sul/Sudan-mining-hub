from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from typing import Optional
import sqlite3
import json

router = APIRouter(prefix="/admin/control", tags=["Admin Control (Offers & Finance)"])

DB_PATH = "local.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_admin_action(admin_email: str, action: str, target_id: str, details: str):
    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO security_breach_logs (user_email, attempted_action, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (admin_email, f"ADMIN_{action}", f"Target ID: {target_id} | {details}", datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        pass

def verify_admin():
    return "admin_chief@gold.sd"

# ==================== [ أولاً: رقابة وإدارة الإعلانات] ====================

@router.get("/offers")
def list_all_offers_for_admin(
    category: Optional[str] = Query(None, description="LIGHT_EQUIPMENT, HEAVY_EQUIPMENT, ASSETS_FACILITIES"),
    status: Optional[str] = Query(None, description="ACTIVE, HIDDEN"),
    admin_email: str = Depends(verify_admin)
):
    conn = get_db_connection()
    query = "SELECT id, trader_email, title, category, price, custom_commission, status, created_at FROM offers WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    if status:
        query += " AND status = ?"
        params.append(status)
        
    offers = conn.execute(query, params).fetchall()
    conn.close()
    return {"total_offers": len(offers), "offers": [dict(o) for o in offers]}

@router.post("/offers/toggle-visibility")
def toggle_offer_visibility(
    offer_id: int,
    action: str, # HIDE, ACTIVATE
    admin_email: str = Depends(verify_admin)
):
    if action not in ["HIDE", "ACTIVATE"]:
        raise HTTPException(status_code=400, detail="إجراء غير قانوني لتعديل حالة الإعلان")
        
    new_status = "HIDDEN" if action == "HIDE" else "ACTIVE"
    
    conn = get_db_connection()
    offer = conn.execute("SELECT id, title FROM offers WHERE id = ?", (offer_id,)).fetchone()
    if not offer:
        conn.close()
        raise HTTPException(status_code=404, detail="الإعلان غير موجود")
        
    conn.execute("UPDATE offers SET status = ? WHERE id = ?", (new_status, offer_id))
    conn.commit()
    conn.close()
    
    log_admin_action(admin_email, "OFFER_MODERATION", str(offer_id), f"تمت إعادة تعيين حالة الإعلان إلى {new_status}")
    return {"message": f"تم بنجاح تعديل حالة الإعلان ({offer['title']}) إلى {new_status}"}

# ==================== [ ثانياً: الرقابة المالية والعمولات ] ====================

@router.get("/finance/commissions")
def view_commissions_report(
    status: Optional[str] = Query(None, description="UNPAID, PAID"),
    admin_email: str = Depends(verify_admin)
):
    conn = get_db_connection()
    query = """
        SELECT n.id as room_id, n.offer_id, n.buyer_id, n.seller_id, n.final_commission, n.commission_status, n.last_updated, o.category 
        FROM negotiation_rooms n
        JOIN offers o ON n.offer_id = o.id
        WHERE n.state = 'ACCEPT'
    """
    params = []
    if status:
        query += " AND n.commission_status = ?"
        params.append(status)
        
    commissions = conn.execute(query, params).fetchall()
    
    # حساب إجمالي المبالغ في التقرير الحالي للوحة التحكم
    total_amount = sum(float(row["final_commission"]) for row in commissions)
    
    conn.close()
    return {
        "commissions_count": len(commissions),
        "total_value_sdg": total_amount,
        "report": [dict(c) for c in commissions]
    }

@router.post("/finance/mark-paid")
def mark_commission_as_paid(
    room_id: int,
    admin_email: str = Depends(verify_admin)
):
    conn = get_db_connection()
    room = conn.execute("SELECT id, final_commission, commission_status FROM negotiation_rooms WHERE id = ?", (room_id,)).fetchone()
    
    if not room:
        conn.close()
        raise HTTPException(status_code=404, detail="غرفة التفاوض أو الصفقة المستهدفة غير موجودة")
        
    if room["commission_status"] == "PAID":
        conn.close()
        return {"message": "العمولة مسجلة بالفعل كمدفوعة مسبقاً"}
        
    conn.execute("UPDATE negotiation_rooms SET commission_status = 'PAID' WHERE id = ?", (room_id,))
    conn.commit()
    conn.close()
    
    log_admin_action(admin_email, "COMMISSION_COLLECTION", str(room_id), f"تم استلام وتأكيد مبلغ العمولة البالغ {room['final_commission']} ج.س")
    return {"message": f"🔒 تم إثبات استلام العمولة بنجاح وإقفال قيد الصفقة رقم {room_id}"}