from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.negotiation import MarketDeal, Offer
from app.core.dependencies import verify_admin_token


router = APIRouter(
    prefix="/admin/operations",
    tags=["Admin Negotiation Actions"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/negotiation-room/{room_id}/close")
def close_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(verify_admin_token)
):

    room = db.query(MarketDeal).filter(
        MarketDeal.id == room_id
    ).first()

    if not room:
        raise HTTPException(
            status_code=404,
            detail="الغرفة غير موجودة"
        )

    room.status = "CLOSED"

    db.commit()

    return {
        "status": "success",
        "message": "تم إغلاق غرفة التفاوض"
    }


@router.post("/offer/{offer_id}/accept")
def accept_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(verify_admin_token)
):

    offer = db.query(Offer).filter(
        Offer.id == offer_id
    ).first()

    if not offer:
        raise HTTPException(
            status_code=404,
            detail="العرض غير موجود"
        )

    offer.status = "ACCEPTED"

    room = db.query(MarketDeal).filter(
        MarketDeal.id == offer.room_id
    ).first()

    if room:
        room.status = "ACCEPTED"

    db.commit()

    return {
        "status": "success",
        "message": "تم قبول العرض"
    }


@router.post("/offer/{offer_id}/reject")
def reject_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(verify_admin_token)
):

    offer = db.query(Offer).filter(
        Offer.id == offer_id
    ).first()

    if not offer:
        raise HTTPException(
            status_code=404,
            detail="العرض غير موجود"
        )

    offer.status = "REJECTED"

    db.commit()

    return {
        "status": "success",
        "message": "تم رفض العرض"
    }
