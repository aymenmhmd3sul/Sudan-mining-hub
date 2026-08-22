from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.models.operations import SubscriptionPlan
from app.models.marketplace import MiningAsset


class PlanAccessService:

    @staticmethod
    def get_user_plan(db: Session, user_id: int):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "ACTIVE"
            )
            .order_by(Subscription.created_at.desc())
            .first()
        )

        if not subscription:
            return None

        plan = (
            db.query(SubscriptionPlan)
            .filter(
                SubscriptionPlan.name == subscription.plan_name
            )
            .first()
        )

        return plan


    @staticmethod
    def can_create_listing(db: Session, user_id: int):

        plan = PlanAccessService.get_user_plan(db, user_id)

        if not plan:
            return False, "لا يوجد اشتراك فعال"

        current_count = (
            db.query(MiningAsset)
            .filter(
                MiningAsset.owner_id == user_id
            )
            .count()
        )

        if current_count >= plan.listing_limit:
            return False, f"تم تجاوز الحد المسموح ({plan.listing_limit})"

        return True, plan
