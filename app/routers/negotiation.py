from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import sqlite3

from app.core.security.jwt import get_current_user

router = APIRouter(prefix="/negotiation", tags=["Negotiation"])

DB = "local.db"


# =========================
# DB Helper
# =========================
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# Schemas
# =========================
class CreateRoom(BaseModel):
    offer_id: int


class MessageIn(BaseModel):
    room_id: int
    message: str


# =========================
# 1. Create Room (SECURE)
# =========================
@router.post("/rooms")
def create_room(data: CreateRoom, user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    offer = cur.execute(
        "SELECT seller_id FROM trader_offers WHERE id=?",
        (data.offer_id,)
    ).fetchone()

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    buyer_id = user["user_id"]
    seller_id = offer["seller_id"]

    # منع إنشاء غرفة لنفسه
    if buyer_id == seller_id:
        raise HTTPException(status_code=400, detail="Invalid negotiation")

    cur.execute("""
        INSERT INTO negotiation_rooms (offer_id, buyer_id, seller_id)
        VALUES (?, ?, ?)
    """, (data.offer_id, buyer_id, seller_id))

    conn.commit()

    return {"status": "room created"}


# =========================
# 2. Get My Rooms (SECURE)
# =========================
@router.get("/rooms")
def get_rooms(user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    user_id = user["user_id"]

    rooms = cur.execute("""
        SELECT * FROM negotiation_rooms
        WHERE buyer_id=? OR seller_id=?
    """, (user_id, user_id)).fetchall()

    return [dict(r) for r in rooms]


# =========================
# 3. Send Message (SECURE)
# =========================
@router.post("/message")
def send_message(data: MessageIn, user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    user_id = user["user_id"]

    # تحقق أن المستخدم داخل الغرفة
    room = cur.execute("""
        SELECT * FROM negotiation_rooms WHERE id=?
    """, (data.room_id,)).fetchone()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if user_id not in (room["buyer_id"], room["seller_id"]):
        raise HTTPException(status_code=403, detail="Not allowed")

    cur.execute("""
        INSERT INTO messages (room_id, sender_id, message)
        VALUES (?, ?, ?)
    """, (data.room_id, user_id, data.message))

    conn.commit()

    return {"status": "message sent"}


# =========================
# 4. Get Messages (SECURE)
# =========================
@router.get("/{room_id}/messages")
def get_messages(room_id: int, user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    user_id = user["user_id"]

    room = cur.execute("""
        SELECT * FROM negotiation_rooms WHERE id=?
    """, (room_id,)).fetchone()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if user_id not in (room["buyer_id"], room["seller_id"]):
        raise HTTPException(status_code=403, detail="Not allowed")

    msgs = cur.execute("""
        SELECT * FROM messages WHERE room_id=?
        ORDER BY created_at ASC
    """, (room_id,)).fetchall()

    return [dict(m) for m in msgs]
