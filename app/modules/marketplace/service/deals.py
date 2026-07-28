from app.modules.marketplace.repository.deals_repo import insert_deal, fetch_deals
from app.modules.marketplace.repository.offers_repo import fetch_offers
from app.modules.marketplace.repository.requests_repo import fetch_requests
from app.modules.marketplace.domain.commission import calculate_commission


def create_deal(request_id: str, offer_id: str, buyer_id: str, seller_id: str, price: float, category: str):

    # تحقق أن الطلب موجود
    requests = fetch_requests()
    if not any(r["id"] == request_id for r in requests):
        return {"error": "request not found"}

    # تحقق أن العرض موجود
    offers = fetch_offers(request_id)
    if not any(o["id"] == offer_id for o in offers):
        return {"error": "offer not found"}

    commission = calculate_commission(price, category)

    deal_id = insert_deal(
        request_id,
        offer_id,
        buyer_id,
        seller_id,
        price,
        commission
    )

    return {
        "deal_id": deal_id,
        "commission": commission,
        "status": "active"
    }


def get_deals():
    return fetch_deals()
