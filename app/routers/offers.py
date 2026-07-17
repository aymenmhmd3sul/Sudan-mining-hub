from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.negotiation_service import NegotiationService
from app.schemas.negotiation import OfferCreate, OfferResponse


router = APIRouter(
    prefix="/negotiation",
    tags=["Negotiation Offers"]
)


@router.post("/rooms/{room_id}/offers",
             response_model=OfferResponse,
             status_code=status.HTTP_201_CREATED)
async def create_offer(
    room_id: int,
    offer_data: OfferCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return NegotiationService.create_offer(
        db=db,
        room_id=room_id,
        seller_id=current_user.id,
        amount=offer_data.amount,
        currency=offer_data.currency
    )


@router.get("/rooms/{room_id}/offers",
            response_model=list[OfferResponse])
async def get_offers(
    room_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return NegotiationService.get_offers(
        db=db,
        room_id=room_id,
        user_id=current_user.id
    )


@router.post("/offers/{offer_id}/accept",
             response_model=OfferResponse)
async def accept_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return NegotiationService.accept_offer(
        db=db,
        offer_id=offer_id,
        user_id=current_user.id
    )
