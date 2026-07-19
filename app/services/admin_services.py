from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.finance import Invoice
from app.models.financial import PaymentTransaction
from app.models.marketplace import MiningAsset
from app.models.market_core import MarketOrder
from app.models.negotiation import Offer


class AdminOperationsService:

    @staticmethod
    def get_live_dashboard_stats(db: Session):
        try:
            total_users = db.query(func.count(User.id)).scalar() or 0

            active_users = (
                db.query(func.count(User.id))
                .filter(User.is_active == True)
                .scalar()
                or 0
            )

            total_assets = db.query(func.count(MiningAsset.id)).scalar() or 0
            total_orders = db.query(func.count(MarketOrder.id)).scalar() or 0
            total_offers = db.query(func.count(Offer.id)).scalar() or 0
            total_invoices = db.query(func.count(Invoice.id)).scalar() or 0

            invoice_volume = (
                db.query(func.sum(Invoice.total_amount))
                .scalar()
                or 0
            )

            pending_payments = (
                db.query(func.count(PaymentTransaction.id))
                .filter(PaymentTransaction.status == "PENDING")
                .scalar()
                or 0
            )

            return {
                "status": "success",
                "users": {
                    "total": total_users,
                    "active": active_users
                },
                "market": {
                    "assets": total_assets,
                    "orders": total_orders,
                    "offers": total_offers
                },
                "finance": {
                    "invoices": total_invoices,
                    "invoice_volume": float(invoice_volume),
                    "pending_payments": pending_payments
                },
                "system_status": "Healthy"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "system_status": "Degraded"
            }


    @staticmethod
    def update_financial_settings(db: Session, bankak: str, wallets: str, foreign_acc: str, fee: float, sub_price: float):
        return True


    @staticmethod
    def update_system_content(db: Session, gold_price: str, announcement: str, banner_url: str):
        return True


    @staticmethod
    def toggle_user_capability(db: Session, user_id: int, capability: str, action: str):
        return {"id": user_id, "status": "updated"}


    @staticmethod
    def get_all_reported_ads(db: Session):
        return []
