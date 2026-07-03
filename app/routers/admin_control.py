from fastapi import APIRouter, Depends, HTTPException, Query, Header
from datetime import datetime
from typing import Optional
from app.core.db import get_db
from app.core.security.jwt import decode_token

router = APIRouter(prefix="/admin/control", tags=["Admin Control (Offers & Finance)"])

# ==================== [ طبقة الحماية والمصادقة ] ====================

def get_current_admin(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="صلاحيات غير كافية - للمشرفين فقط")
            
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="توكن غير صالح أو منتهي الصلاحية")

def log_admin_action(admin_email: str, action: str, target_id: str, details: str):
    try:
        db = get_db()
        db.execute("""
            INSERT INTO security_breach_logs (user_email, attempted_action, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (admin_email, f"ADMIN_{action}", f"Target ID: {target_id} | {details}", datetime.utcnow().isoformat()))
        db.commit()
    except Exception:
        pass  # حماية السيرفر من التوقف في حال فشل تسجيل اللوج

# ==================== [ أولاً: رقابة وإدارة الإعلانات ] ====================

@router.get("/offers")
def list_all_offers_for_admin(
    category: Optional[str] = Query(None, description="LIGHT_EQUIPMENT, HEAVY_EQUIPMENT, ASSETS_FACILITIES"),
    status: Optional[str] = Query(None, description="ACTIVE, HIDDEN"),
    admin_email: str = Depends(get_current_admin)
):
    db = get_db()
    query = "SELECT id, trader_email, title, category, price, custom_commission, status, created_at FROM offers WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    if status:
        query += " AND status = ?"
        params.append(status)
        
    offers = db.execute(query, params).fetchall()
    return {"total_offers": len(offers), "offers": [dict(o) for o in offers]}

@router.post("/offers/toggle-visibility")
def toggle_offer_visibility(
    offer_id: int,
    action: str,  # HIDE, ACTIVATE
    admin_email: str = Depends(get_current_admin)
):
    if action not in ["HIDE", "ACTIVATE"]:
        raise HTTPException(status_code=400, detail="إجراء غير قانوني لتعديل حالة الإعلان")
        
    db = get_db()
    offer = db.execute("SELECT id, title FROM offers WHERE id = ?", (offer_id,)).fetchone()
    if not offer:
        raise HTTPException(status_code=404, detail="الإعلان غير موجود")
        
    new_status = "HIDDEN" if action == "HIDE" else "ACTIVE"
    
    db.execute("UPDATE offers SET status = ? WHERE id = ?", (new_status, offer_id))
    db.commit()
    
    log_admin_action(admin_email, "OFFER_MODERATION", str(offer_id), f"تمت إعادة تعيين حالة الإعلان إلى {new_status}")
    return {"message": f"تم بنجاح تعديل حالة الإعلان ({offer['title']}) إلى {new_status}"}

# ==================== [ ثانياً: الرقابة المالية والعمولات ] ====================

@router.get("/finance/commissions")
def view_commissions_report(
    status: Optional[str] = Query(None, description="UNPAID, PAID"),
    admin_email: str = Depends(get_current_admin)
):
    db = get_db()
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
        
    commissions = db.execute(query, params).fetchall()
    total_amount = sum(float(row["final_commission"]) for row in commissions)
    
    return {
        "commissions_count": len(commissions),
        "total_value_sdg": total_amount,
        "report": [dict(c) for c in commissions]
    }

@router.post("/finance/mark-paid")
def mark_commission_as_paid(
    room_id: int,
    admin_email: str = Depends(get_current_admin)
):
    db = get_db()
    room = db.execute("SELECT id, final_commission, commission_status FROM negotiation_rooms WHERE id = ?", (room_id,)).fetchone()
    
    if not room:
        raise HTTPException(status_code=404, detail="غرفة التفاوض أو الصفقة المستهدفة غير موجودة")
        
    if room["commission_status"] == "PAID":
        return {"message": "العمولة مسجلة بالفعل كمدفوعة مسبقاً"}
        
    db.execute("UPDATE negotiation_rooms SET commission_status = 'PAID' WHERE id = ?", (room_id,))
    db.commit()
    
    log_admin_action(admin_email, "COMMISSION_COLLECTION", str(room_id), f"تم استلام وتأكيد مبلغ العمولة البالغ {room['final_commission']} ج.س")
    return {"message": f"🔒 تم إثبات استلام العمولة بنجاح وإقفال قيد الصفقة رقم {room_id}"}
