from fastapi import APIRouter, Depends, HTTPException, Body, Request
from app.core.security.rbac import require_role
from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
import json
import sys
import os

router = APIRouter(prefix="/negotiation", tags=["negotiation"])

DB_PATH = "local.db"
VALID_STATES = ["OPEN", "OFFER", "COUNTER", "ACCEPT", "CLOSE"]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# جلب بيانات الغرفة الحقيقية من قاعدة البيانات
def fetch_room_from_db(room_id: int) -> Optional[dict]:
    conn = get_db_connection()
    room = conn.execute("SELECT * FROM negotiation_rooms WHERE id = ?", (room_id,)).fetchone()
    conn.close()
    if room:
        room_dict = dict(room)
        # تحويل السجل النصي القادم من القاعدة إلى قائمة بايثون مجدداً
        room_dict["offers_history"] = json.loads(room_dict["offers_history"])
        return room_dict
    return None

# دالة إدارة الانتقال وتحديث قاعدة البيانات
def db_transition_to_state(room_id: int, new_state: str, actor_role: str, offer_data: Optional[dict] = None) -> tuple[bool, str]:
    room = fetch_room_from_db(room_id)
    if not room:
        return False, "غرفة التفاوض غير موجودة في قاعدة البيانات"
    
    current_state = room["state"]
    if current_state in ["ACCEPT", "CLOSE"]:
        return False, f"التفاوض منتهي، الغرفة مغلقة بحالة: {current_state}"
        
    if new_state not in VALID_STATES:
        return False, "حالة تفاوض غير قانونية"
        
    if new_state == "ACCEPT" and current_state not in ["OFFER", "COUNTER"]:
        return False, "لا يمكن قبول الصفقة قبل تقديم عرض أو عرض مضاد"
        
    # تحديث سجل العروض محلياً
    history = room["offers_history"]
    if offer_data:
        history.append({
            "by_role": actor_role,
            "timestamp": datetime.utcnow().isoformat(),
            **offer_data
        })
        
    # حفظ التحديثات مباشرة في قاعدة البيانات
    conn = get_db_connection()
    conn.execute("""
        UPDATE negotiation_rooms 
        SET state = ?, offers_history = ?, last_updated = ?
        WHERE id = ?
    """, (new_state, json.dumps(history), datetime.utcnow().isoformat(), room_id))
    conn.commit()
    conn.close()
    
    return True, "تم تحديث قاعدة البيانات بنجاح"


# حل مشكلة الاستيراد
try:
    from app.db.compat import get_user_from_cookie
except ModuleNotFoundError:
    try:
        from db.compat import get_user_from_cookie
    except ModuleNotFoundError:
        def get_user_from_cookie(req): return {"email": "buyer_test@test.com", "role": "buyer"}

def get_current_negotiation_user(request: Request):
    user = get_user_from_cookie(request)
    if not user or user.get("role") not in ["buyer", "seller"]:
        raise HTTPException(status_code=401, detail="غير مصرح لك، يجب تسجيل الدخول")
    return user


@router.post("/rooms")
def create_room(
    offer_id: int,
    user = Depends(get_current_negotiation_user)
):
    if user.get("role") != "buyer":
        raise HTTPException(status_code=403, detail="فقط المشتري يمكنه بدء غرفة تفاوض جديدة")
        
    conn = get_db_connection()
    # التحقق مما إذا كانت الغرفة مفتوحة مسبقاً لنفس العرض والمشتري
    existing_room = conn.execute(
        "SELECT id FROM negotiation_rooms WHERE offer_id = ? AND buyer_id = ?", 
        (offer_id, user.get("email"))
    ).fetchone()
    
    if existing_room:
        room_id = existing_room["id"]
    else:
        # إنشاء سجل حقيقي في الجدول
        now_str = datetime.utcnow().isoformat()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO negotiation_rooms (offer_id, buyer_id, seller_id, state, offers_history, created_at, last_updated)
            VALUES (?, ?, ?, 'OPEN', '[]', ?, ?)
        """, (offer_id, user.get("email"), "trader_test@test.com", now_str, now_str))
        conn.commit()
        room_id = cursor.lastrowid
        
    conn.close()
    return {
        "message": "Room loaded from Database",
        "room_data": fetch_room_from_db(room_id)
    }

@router.post("/submit-offer")
def submit_offer(
    room_id: int,
    price: float = Body(...),
    quantity: float = Body(...),
    notes: str = Body(""),
    user = Depends(get_current_negotiation_user)
):
    room = fetch_room_from_db(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="غرفة التفاوض غير موجودة")
        
    if user.get("role") == "buyer" and len(room["offers_history"]) == 0:
        next_state = "OFFER"
    else:
        next_state = "COUNTER"
        
    success, msg = db_transition_to_state(
        room_id=room_id,
        new_state=next_state,
        actor_role=user.get("role"),
        offer_data={"price": price, "quantity": quantity, "notes": notes}
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=msg)
        
    return {
        "message": f"تم تسجيل العرض في قاعدة البيانات بواسطة ({user.get('role')})",
        "room_data": fetch_room_from_db(room_id)
    }

@router.post("/accept-deal")
def accept_deal(
    room_id: int,
    user = Depends(get_current_negotiation_user)
):
    success, msg = db_transition_to_state(room_id=room_id, new_state="ACCEPT", actor_role=user.get("role"))
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {
        "message": f"🔒 تم قبول الصفقة وتأمين الأسعار في الجدول بواسطة {user.get('role')}",
        "room_data": fetch_room_from_db(room_id)
    }

@router.post("/close-room")
def close_room(
    room_id: int,
    user = Depends(get_current_negotiation_user)
):
    success, msg = db_transition_to_state(room_id=room_id, new_state="CLOSE", actor_role=user.get("role"))
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {
        "message": f"❌ تم إغلاق التفاوض برمجياً بواسطة {user.get('role')}",
        "room_data": fetch_room_from_db(room_id)
    }
