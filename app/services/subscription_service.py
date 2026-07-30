from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.subscription import Subscription


class SubscriptionService:

    @staticmethod
    def get_user_subscription(db: Session, user_id: int):
        result = db.execute(
            select(Subscription)
            .where(Subscription.user_id == user_id)
            .order_by(Subscription.created_at.desc())
        )

        return result.scalars().first()


    @staticmethod
    def is_active(subscription: Subscription) -> bool:
        if not subscription:
            return False

        if subscription.status != "ACTIVE":
            return False

        if subscription.expires_at:
            return subscription.expires_at > datetime.utcnow()

        return True


    @staticmethod
    def activate(subscription: Subscription):
        subscription.status = "ACTIVE"
        return subscription


    @staticmethod
    def cancel(subscription: Subscription):
        subscription.status = "CANCELLED"
        subscription.auto_renew = False
        return subscription
