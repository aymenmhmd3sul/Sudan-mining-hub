from sqlalchemy.orm.exc import StaleDataError
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

        # غرفة واحدة فقط لكل مشتري + أصل.
        # لا ننشئ غرفة جديدة إذا كانت هناك غرفة سابقة
        # حتى لو كانت ACCEPTED أو CLOSED أو REJECTED.
        existing_room = db.query(MarketDeal).filter(
            MarketDeal.asset_id == room_data.asset_id,
            MarketDeal.buyer_id == buyer_id
        ).order_by(MarketDeal.id.asc()).first()

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
    def get_user_rooms(db: Session, user_id: int):
        """
        إرجاع جميع غرف التفاوض التي يكون المستخدم طرفاً فيها.
        """
        rooms = (
            db.query(MarketDeal)
            .filter(
                (MarketDeal.buyer_id == user_id) |
                (MarketDeal.seller_id == user_id)
            )
            .order_by(MarketDeal.updated_at.desc())
            .all()
        )

        result = []

        for room in rooms:
            last_message = (
                db.query(NegotiationMessage)
                .filter(NegotiationMessage.room_id == room.id)
                .order_by(NegotiationMessage.created_at.desc())
                .first()
            )

            from app.models.negotiation import Offer

            last_offer = (
                db.query(Offer)
                .filter(Offer.room_id == room.id)
                .order_by(Offer.created_at.desc())
                .first()
            )

            unread_count = (
                db.query(NegotiationMessage)
                .filter(
                    NegotiationMessage.room_id == room.id,
                    NegotiationMessage.sender_id != user_id,
                    NegotiationMessage.is_read == False
                )
                .count()
            )

            result.append({
                "id": room.id,
                "asset_id": room.asset_id,
                "seller_id": room.seller_id,
                "buyer_id": room.buyer_id,
                "status": str(room.status),
                "created_at": (
                    room.created_at
                    if room.created_at
                    else datetime.utcnow()
                ),
                "updated_at": (
                    room.updated_at
                    if room.updated_at
                    else datetime.utcnow()
                ),
                "last_message_at": (
                    last_message.created_at
                    if last_message
                    else None
                ),
                "unread_count": unread_count,
                "last_offer_id": (
                    last_offer.id
                    if last_offer
                    else None
                )
            })

        return result

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

    @staticmethod
    def create_offer(db: Session, room_id: int, seller_id: int, amount: float, currency: str = "USD"):
        from app.models.negotiation import Offer

        room = db.query(MarketDeal).filter(MarketDeal.id == room_id).first()

        if not room:
            raise HTTPException(status_code=404, detail="غرفة التفاوض غير موجودة")

        if room.seller_id != seller_id:
            raise HTTPException(status_code=403, detail="فقط مالك الأصل يستطيع تقديم عرض")

        if room.status != "OPEN":
            raise HTTPException(status_code=400, detail="الغرفة غير مفتوحة")

        offer = Offer(
            room_id=room_id,
            amount=amount,
            currency=currency,
            status="PENDING"
        )

        db.add(offer)
        db.commit()
        db.refresh(offer)

        return {
            "id": offer.id,
            "room_id": offer.room_id,
            "amount": offer.amount,
            "currency": offer.currency,
            "status": offer.status,
            "created_at": offer.created_at,
        }


    @staticmethod
    def get_offers(db: Session, room_id: int, user_id: int):
        from app.models.negotiation import Offer

        room = db.query(MarketDeal).filter(MarketDeal.id == room_id).first()

        if not room:
            raise HTTPException(status_code=404, detail="الغرفة غير موجودة")

        if user_id not in [room.buyer_id, room.seller_id]:
            raise HTTPException(status_code=403, detail="غير مصرح")

        return db.query(Offer).filter(
            Offer.room_id == room_id
        ).order_by(Offer.created_at.desc()).all()


    @staticmethod
    def accept_offer(db: Session, offer_id: int, user_id: int):
        from app.models.negotiation import Offer

        offer = db.query(Offer).filter(Offer.id == offer_id).first()

        if not offer:
            raise HTTPException(status_code=404, detail="العرض غير موجود")

        room = db.query(MarketDeal).filter(
            MarketDeal.id == offer.room_id
        ).first()

        if not room:
            raise HTTPException(status_code=404, detail="الغرفة غير موجودة")

        if room.buyer_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="فقط المشتري يستطيع قبول العرض"
            )

        # منع إعادة قبول عرض سبق قبوله
        if str(offer.status).upper() == "ACCEPTED":
            raise HTTPException(
                status_code=409,
                detail="العرض مقبول بالفعل"
            )

        # لا يمكن قبول أي عرض بعد إغلاق الغرفة
        if str(room.status).upper() in ["ACCEPTED", "CLOSED", "REJECTED"]:
            raise HTTPException(
                status_code=409,
                detail="غرفة التفاوض مغلقة ولا يمكن قبول عروض جديدة"
            )

        # لا يمكن قبول عرض ليس في حالة الانتظار
        if str(offer.status).upper() != "PENDING":
            raise HTTPException(
                status_code=409,
                detail="العرض ليس في حالة انتظار"
            )

        # قبول عرض واحد فقط داخل الغرفة
        db.query(Offer).filter(
            Offer.room_id == room.id,
            Offer.id != offer.id
        ).update(
            {"status": "REJECTED"},
            synchronize_session=False
        )

        offer.status = "ACCEPTED"
        room.status = "ACCEPTED"

        db.commit()
        db.refresh(offer)

        return {
            "id": offer.id,
            "room_id": offer.room_id,
            "amount": offer.amount,
            "currency": offer.currency,
            "status": offer.status,
            "created_at": offer.created_at,
        }

    @staticmethod
    def get_room_by_id(db: Session, room_id: int, user_id: int):
        room = db.query(MarketDeal).filter(
            MarketDeal.id == room_id
        ).first()

        if not room:
            raise HTTPException(status_code=404, detail="غرفة التفاوض غير موجودة")

        if user_id not in [room.buyer_id, room.seller_id]:
            raise HTTPException(status_code=403, detail="غير مصرح لك")

        messages = db.query(NegotiationMessage).filter(
            NegotiationMessage.room_id == room_id
        ).order_by(
            NegotiationMessage.created_at.asc()
        ).all()

        from app.models.negotiation import Offer

        offers = db.query(Offer).filter(
            Offer.room_id == room_id
        ).order_by(
            Offer.created_at.desc()
        ).all()

        return {
            "id": room.id,
            "asset_id": room.asset_id,
            "seller_id": room.seller_id,
            "buyer_id": room.buyer_id,
            "status": room.status,
            "created_at": room.created_at,
            "updated_at": room.updated_at,
            "last_message_at": messages[-1].created_at if messages else None,
            "unread_count": 0,
            "last_offer_id": offers[0].id if offers else None,
            "messages": [
                {
                    "id": m.id,
                    "room_id": m.room_id,
                    "sender_id": m.sender_id,
                    "message": m.message,
                    "message_type": str(m.message_type),
                    "created_at": m.created_at
                }
                for m in messages
            ],
            "offers": [
                {
                    "id": o.id,
                    "room_id": o.room_id,
                    "amount": o.amount,
                    "currency": o.currency,
                    "status": o.status,
                    "created_at": o.created_at
                }
                for o in offers
            ]
        }
