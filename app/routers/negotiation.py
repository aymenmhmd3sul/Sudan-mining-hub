from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.db import get_db_connection
from app.core.dependencies import get_current_user, require_buyer, require_any_user
from app.database import get_db
from app.models.negotiation import MarketDeal, DealMilestone

router = APIRouter(tags=["Negotiation & Deals Engine"])

# الـ Payloads مستوردة مركزيًا من طبقة الـ Schemas
from app.schemas.negotiation import CreateRoomPayload, SendMessagePayload, RoomStatusPayload, DealCreatePayload, MilestoneUpdatePayload

# =========================================================================
# 1. المسارات القديمة (مستمرة للعمل مع الشات والغرف الحالية)
# =========================================================================

@router.post("/rooms", status_code=status.HTTP_201_CREATED)
def open_negotiation_room(payload: CreateRoomPayload, current_user: dict = Depends(require_buyer)):
    conn = get_db_connection()
    cursor = conn.cursor()
    asset = cursor.execute("SELECT * FROM mining_assets WHERE id = ? AND state = 'PUBLISHED'", (payload.asset_id,)).fetchone()
    if not asset:
        conn.close()
        raise HTTPException(status_code=404, detail="الأصل غير موجود")
    asset_dict = dict(asset)
    cursor.execute('INSERT INTO negotiation_rooms (asset_id, buyer_id, seller_id) VALUES (?, ?, ?)', (payload.asset_id, current_user["id"], asset_dict["owner_id"]))
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"message": "تم فتح الغرفة", "room_id": room_id}

@router.post("/rooms/{room_id}/messages", status_code=status.HTTP_201_CREATED)
def send_negotiation_message(room_id: int, payload: SendMessagePayload, current_user: dict = Depends(require_any_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO negotiation_messages (room_id, sender_id, message, offer_price) VALUES (?, ?, ?, ?)', (room_id, current_user["id"], payload.message, payload.offer_price))
    conn.commit()
    conn.close()
    return {"message": "تم إرسال الرسالة"}

@router.get("/rooms/{room_id}/messages")
def get_room_messages(room_id: int, current_user: dict = Depends(require_any_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    messages = cursor.execute("SELECT * FROM negotiation_messages WHERE room_id = ? ORDER BY created_at ASC", (room_id,)).fetchall()
    conn.close()
    return [dict(m) for m in messages]

@router.post("/rooms/{room_id}/status")
def update_room_status(room_id: int, payload: RoomStatusPayload, current_user: dict = Depends(require_any_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE negotiation_rooms SET status = ? WHERE id = ?", (payload.status, room_id))
    conn.commit()
    conn.close()
    return {"message": f"تم تحديث حالة الغرفة إلى {payload.status} بنجاح."}

# =========================================================================
# 2. المسارات الجديدة (المرحلة الثالثة: محرك العقود والـ Milestones التجريدي)
# =========================================================================

@router.post("/deals", status_code=status.HTTP_201_CREATED)
def create_formal_deal(payload: DealCreatePayload, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """تحويل الاتفاق الشفهي داخل الغرفة إلى صفقة رسمية مجدولة بالمراحل."""
    seller_id = current_user.id if hasattr(current_user, 'id') else current_user.get('id')
    
    # صياغة الصفقة الأساسية
    new_deal = MarketDeal(
        listing_id=payload.listing_id,
        buyer_id=payload.buyer_id,
        seller_id=seller_id,
        final_price=payload.final_price,
        currency=payload.currency,
        status="PENDING_APPROVAL"
    )
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)

    # توليد المراحل التنفيذية المرفقة للصفقة تلقائياً حسب طلب البائع
    for idx, milestone_title in enumerate(payload.milestones, start=1):
        ms = DealMilestone(
            deal_id=new_deal.id,
            title=milestone_title,
            step_order=idx,
            status="PENDING",
            is_critical=True
        )
        db.add(ms)
    
    db.commit()
    return {"status": "success", "message": "تم إبرام الصفقة الرسمية وتوليد خطة التنفيذ الميدانية", "deal_id": new_deal.id}

@router.patch("/deals/{deal_id}/milestones/{milestone_id}")
def update_milestone_status(deal_id: int, milestone_id: int, payload: MilestoneUpdatePayload, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """تحديث حالة خطوة معينة في جدول الصفقة (تحول المعمل، النقل، أو الدفع)."""
    milestone = db.query(DealMilestone).filter(DealMilestone.id == milestone_id, DealMilestone.deal_id == deal_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="الخطوة التنفيذية المستهدفة غير موجودة")
        
    milestone.status = payload.status
    db.commit()
    return {"status": "success", "message": f"تم تحديث خطوة [{milestone.title}] إلى الحالة {payload.status} بنجاح"}
