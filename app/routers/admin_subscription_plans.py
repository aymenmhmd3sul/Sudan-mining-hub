from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import verify_admin_token
from app.models.operations import SubscriptionPlan
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/admin/subscription-plans",
    tags=["Admin Subscription Plans"]
)


def get_current_admin(
    current_user: User = Depends(verify_admin_token)
):
    return current_user


@router.get("")
def list_plans(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    plans = (
        db.query(SubscriptionPlan)
        .order_by(SubscriptionPlan.id.asc())
        .all()
    )

    return {
        "status": "success",
        "count": len(plans),
        "data": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "duration_days": p.duration_days,
                "listing_limit": p.listing_limit,
                "commission_rate": p.commission_rate
            }
            for p in plans
        ]
    }
