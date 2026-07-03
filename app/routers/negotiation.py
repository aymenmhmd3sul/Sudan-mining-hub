from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.core.db import get_db_connection
from app.core.dependencies import require_buyer, require_any_user

router = APIRouter(tags=["Negotiation Engine"])

class CreateRoomPayload(BaseModel):
    asset_id: int

class SendMessagePayload(BaseModel):
    message: str
    offer_price: Optional[float] = None

class RoomStatusPayload(BaseModel):
    status: str

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
