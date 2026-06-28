from fastapi import APIRouter, Depends, HTTPException
from app.core.security.jwt import get_current_user
from app.schemas.negotiation import CreateRoom, MessageIn
from app.services.negotiation_service import (
    get_active_offer,
    room_exists,
    create_room_logic,
    get_user_rooms,
    get_room_messages
)
from app.services.security import assert_user_valid

router = APIRouter()


# ---------------- CREATE ROOM ----------------
@router.post("/rooms")
def create_room(data: CreateRoom, user=Depends(get_current_user)):

    assert_user_valid(user)

    offer = get_active_offer(data.offer_id)

    if not offer:
        raise HTTPException(status_code=404, detail="Invalid or inactive offer")

    buyer_id = user["id"]
    seller_id = offer["seller_id"]

    if buyer_id == seller_id:
        raise HTTPException(status_code=400, detail="Self negotiation not allowed")

    if room_exists(data.offer_id, buyer_id):
        raise HTTPException(status_code=409, detail="Room already exists")

    room_id = create_room_logic(data.offer_id, buyer_id, seller_id)

    return {"room_id": room_id}


# ---------------- GET ROOMS ----------------
@router.get("/rooms")
def get_rooms(user=Depends(get_current_user)):
    assert_user_valid(user)
    return get_user_rooms(user["id"])


# ---------------- GET MESSAGES ----------------
@router.get("/messages/{room_id}")
def messages(room_id: int, user=Depends(get_current_user)):
    assert_user_valid(user)
    return get_room_messages(room_id)
