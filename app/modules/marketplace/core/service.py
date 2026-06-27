from typing import List
from .models import BuyerRequest, Offer, Deal


class MarketplaceService:

    def __init__(self):
        self.requests: List[BuyerRequest] = []
        self.offers: List[Offer] = []
        self.deals: List[Deal] = []

    # Buyer creates request
    def create_request(self, request: BuyerRequest):
        self.requests.append(request)
        return request

    # Trader sends offer
    def create_offer(self, offer: Offer):
        self.offers.append(offer)
        return offer

    # Accept deal
    def accept_offer(self, offer_id: str):
        offer = next((o for o in self.offers if o.id == offer_id), None)
        if not offer:
            return None

        deal = Deal(
            id=f"deal_{offer_id}",
            offer_id=offer_id,
            status="accepted",
            commission=offer.price * 0.02
        )

        self.deals.append(deal)
        return deal
