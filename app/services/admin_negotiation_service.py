from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.negotiation import MarketDeal, NegotiationMessage, Offer


class AdminNegotiationService:

    @staticmethod
    def get_dashboard(db: Session):

        total_rooms = db.query(
            func.count(MarketDeal.id)
        ).scalar() or 0

        open_rooms = db.query(
            func.count(MarketDeal.id)
        ).filter(
            MarketDeal.status == "OPEN"
        ).scalar() or 0

        accepted_rooms = db.query(
            func.count(MarketDeal.id)
        ).filter(
            MarketDeal.status == "ACCEPTED"
        ).scalar() or 0

        total_messages = db.query(
            func.count(NegotiationMessage.id)
        ).scalar() or 0

        total_offers = db.query(
            func.count(Offer.id)
        ).scalar() or 0

        latest_rooms = db.query(
            MarketDeal
        ).order_by(
            MarketDeal.updated_at.desc()
        ).limit(10).all()

        return {
            "status": "success",
            "statistics": {
                "total_rooms": total_rooms,
                "open_rooms": open_rooms,
                "accepted_rooms": accepted_rooms,
                "messages": total_messages,
                "offers": total_offers
            },
            "latest_rooms": [
                {
                    "id": room.id,
                    "asset_id": room.asset_id,
                    "buyer_id": room.buyer_id,
                    "seller_id": room.seller_id,
                    "status": room.status,
                    "created_at": room.created_at,
                    "updated_at": room.updated_at
                }
                for room in latest_rooms
            ]
        }
