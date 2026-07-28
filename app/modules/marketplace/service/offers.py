from app.modules.marketplace.repository.offers_repo import insert_offer, fetch_offers


def create_offer(user_id: str, request_id: str, price: float):
    return insert_offer(user_id, request_id, price)


def get_offers(request_id: str = None):
    return fetch_offers(request_id)
