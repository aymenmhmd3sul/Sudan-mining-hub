from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.negotiation import MarketDeal, NegotiationMessage, Offer

router = APIRouter(
    prefix="/admin/operations",
    tags=["Admin Negotiation Details"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/negotiation-room/{room_id}")
def negotiation_room_details(
    room_id: int,
    db: Session = Depends(get_db)
):

    room = db.query(MarketDeal).filter(
        MarketDeal.id == room_id
    ).first()

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    messages = db.query(
        NegotiationMessage
    ).filter(
        NegotiationMessage.room_id == room_id
    ).order_by(
        NegotiationMessage.created_at.asc()
    ).all()


    offers = db.query(
        Offer
    ).filter(
        Offer.room_id == room_id
    ).order_by(
        Offer.created_at.desc()
    ).all()


    return {
        "status": "success",
        "room": {
            "id": room.id,
            "asset_id": room.asset_id,
            "buyer_id": room.buyer_id,
            "seller_id": room.seller_id,
            "status": room.status,
            "created_at": room.created_at,
            "updated_at": room.updated_at
        },

        "messages": [
            {
                "id": m.id,
                "sender_id": m.sender_id,
                "message": m.message,
                "type": m.message_type,
                "created_at": m.created_at
            }
            for m in messages
        ],

        "offers": [
            {
                "id": o.id,
                "amount": o.amount,
                "currency": o.currency,
                "status": o.status,
                "created_at": o.created_at
            }
            for o in offers
        ]
    }
