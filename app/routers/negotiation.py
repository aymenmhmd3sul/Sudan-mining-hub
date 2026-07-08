from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.negotiation import RoomCreate, RoomResponse, RoomDetailResponse, MessageCreate, MessageResponse
from app.services.negotiation_service import NegotiationService

router = APIRouter(prefix="/negotiation", tags=["Negotiation Engine"])

# --- غرف التفاوض ---
@router.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_negotiation_room(room_data: RoomCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return NegotiationService.create_room(db=db, room_data=room_data, buyer_id=current_user.id)

@router.get("/rooms", response_model=List[RoomResponse])
async def get_my_rooms(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return NegotiationService.get_user_rooms(db=db, user_id=current_user.id)

@router.get("/rooms/{room_id}", response_model=RoomDetailResponse)
async def get_room_details(room_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return NegotiationService.get_room_by_id(db=db, room_id=room_id, user_id=current_user.id)

# --- نظام المحادثة والرسائل ---
@router.post("/rooms/{room_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message_to_room(
    room_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    إرسال رسالة نصية جديدة داخل غرف التفاوض المفتوحة.
    """
    return NegotiationService.send_message(db=db, room_id=room_id, sender_id=current_user.id, message_data=message_data)

@router.get("/rooms/{room_id}/messages", response_model=List[MessageResponse])
async def get_room_messages(
    room_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    جلب سجل الرسائل الخاص بالغرفة مرتباً تصاعدياً مع دعم الـ Pagination.
    """
    return NegotiationService.get_messages(db=db, room_id=room_id, user_id=current_user.id, limit=limit, offset=offset)

@router.post("/rooms/{room_id}/read", status_code=status.HTTP_200_OK)
async def mark_room_messages_as_read(room_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    تحديث حالة جميع الرسائل غير المقروءة الواردة إليك في هذه الغرفة لتصبح مقروءة.
    """
    return NegotiationService.mark_as_read(db=db, room_id=room_id, current_user_id=current_user.id)
