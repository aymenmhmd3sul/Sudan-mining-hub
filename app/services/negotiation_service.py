from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.marketplace import MiningAsset
from app.models.negotiation import MarketDeal, NegotiationMessage
from app.schemas.negotiation import RoomCreate, MessageCreate

class NegotiationService:

    @staticmethod
    def create_room(db: Session, room_data: RoomCreate, buyer_id: int):
        asset = db.query(MiningAsset).filter(MiningAsset.id == room_data.asset_id).first()
        if not asset:
            raise HTTPException(status_code=404, detail="الأصل أو المعدة غير موجودة")
        
        if asset.owner_id == buyer_id:
            raise HTTPException(status_code=400, detail="لا يمكنك فتح غرفة تفاوض لشراء أصل تملكه")

        existing_room = db.query(MarketDeal).filter(
            MarketDeal.asset_id == room_data.asset_id,
            MarketDeal.buyer_id == buyer_id,
            MarketDeal.status == "OPEN"
        ).first()

        room_obj = existing_room
        if not room_obj:
            new_room = MarketDeal(
                asset_id=room_data.asset_id,
                buyer_id=buyer_id,
                seller_id=asset.owner_id,
                status="OPEN"
            )
            db.add(new_room)
            db.commit()
            db.refresh(new_room)
            room_obj = new_room

        return {
            "id": room_obj.id,
            "asset_id": room_obj.asset_id,
            "seller_id": room_obj.seller_id,
            "buyer_id": room_obj.buyer_id,
            "status": str(room_obj.status),
            "created_at": room_obj.created_at if room_obj.created_at else datetime.utcnow(),
            "updated_at": room_obj.updated_at if room_obj.updated_at else datetime.utcnow(),
            "last_message_at": None,
            "unread_count": 0,
            "last_offer_id": None
        }

    @staticmethod
    def send_message(db: Session, room_id: int, sender_id: int, message_data: MessageCreate, offer_id: int = None):
        room = db.query(MarketDeal).filter(MarketDeal.id == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="غرفة التفاوض غير موجودة")
        if room.buyer_id != sender_id and room.seller_id != sender_id:
            raise HTTPException(status_code=403, detail="غير مصرح لك بالإرسال داخل هذه الغرفة")
        
        if room.status in ["CLOSED", "ACCEPTED", "REJECTED"]:
            raise HTTPException(status_code=400, detail="لا يمكن إرسال رسائل في غرفة تفاوض منتهية أو مغلقة")
        
        new_msg = NegotiationMessage(
            room_id=room_id,
            sender_id=sender_id,
            message=message_data.message,
            message_type=getattr(message_data, "message_type", "TEXT") or "TEXT",
            offer_id=offer_id
        )
        db.add(new_msg)
        room.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(new_msg)

        return {
            "id": new_msg.id,
            "room_id": new_msg.room_id,
            "sender_id": new_msg.sender_id,
            "message_type": str(new_msg.message_type),
            "message": str(new_msg.message),
            "offer_id": new_msg.offer_id,
            "reply_to_id": getattr(new_msg, "reply_to_id", None),
            "is_read": getattr(new_msg, "is_read", False),
            "created_at": new_msg.created_at if new_msg.created_at else datetime.utcnow(),
            "updated_at": new_msg.updated_at if new_msg.updated_at else datetime.utcnow()
        }

    @staticmethod
    def get_messages(db: Session, room_id: int, user_id: int, limit: int = 50, offset: int = 0):
        room = db.query(MarketDeal).filter(MarketDeal.id == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="غرفة التفاوض غير موجودة")
        if room.buyer_id != user_id and room.seller_id != user_id:
            raise HTTPException(status_code=403, detail="غير مصرح لك بالاطلاع على رسائل هذه الغرفة")

        messages = db.query(NegotiationMessage).filter(
            NegotiationMessage.room_id == room_id
        ).order_by(NegotiationMessage.created_at.asc()).limit(limit).offset(offset).all()

        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "room_id": msg.room_id,
                "sender_id": msg.sender_id,
                "message_type": str(msg.message_type),
                "message": str(msg.message),
                "offer_id": msg.offer_id,
                "reply_to_id": getattr(msg, "reply_to_id", None),
                "is_read": getattr(msg, "is_read", False),
                "created_at": msg.created_at,
                "updated_at": msg.updated_at
            })
        return result

    @staticmethod
    def mark_as_read(db: Session, room_id: int, current_user_id: int):
        db.query(NegotiationMessage).filter(
            NegotiationMessage.room_id == room_id,
            NegotiationMessage.sender_id != current_user_id,
            NegotiationMessage.is_read == False
        ).update({"is_read": True}, synchronize_session=False)
        db.commit()
        return {"status": "success", "detail": "تم تحديث حالة الرسائل إلى مقروءة"}
