from fastapi import APIRouter
from app.modules.marketplace.service.requests import create_request, get_requests
from app.modules.marketplace.service.offers import create_offer, get_offers
from app.modules.marketplace.service.deals import create_deal, get_deals

router = APIRouter(prefix="/market", tags=["marketplace"])


# ------------------------
# REQUESTS
# ------------------------
@router.get("/requests")
def list_requests():
    return get_requests()


@router.post("/request")
def add_request(user_id: str, title: str, category: str):
    return create_request(user_id, title, category)


# ------------------------
# OFFERS
# ------------------------
@router.get("/offers")
def list_offers(request_id: str = None):
    return get_offers(request_id)


@router.post("/offer")
def add_offer(user_id: str, request_id: str, price: float):
    return create_offer(user_id, request_id, price)


# ------------------------
# DEALS
# ------------------------
@router.get("/deals")
def list_deals():
    return get_deals()


@router.post("/deal")
def add_deal(
    request_id: str,
    offer_id: str,
    buyer_id: str,
    seller_id: str,
    price: float,
    category: str
):
    return create_deal(
        request_id,
        offer_id,
        buyer_id,
        seller_id,
        price,
        category
    )
