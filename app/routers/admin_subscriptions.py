from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import verify_admin_token
from app.models.user import User
from app.models.subscription import Subscription


router = APIRouter(
    prefix="/api/v1/admin/subscriptions",
    tags=["Admin Subscriptions"]
)


def get_current_admin(current_user: User = Depends(verify_admin_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": "admin"
    }


@router.get("")
def list_subscriptions(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    subscriptions = (
        db.query(Subscription)
        .order_by(Subscription.created_at.desc())
        .all()
    )

    return {
        "status": "success",
        "count": len(subscriptions),
        "data": subscriptions
    }


@router.get("/stats")
def subscription_stats(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    total = db.query(Subscription).count()

    active = (
        db.query(Subscription)
        .filter(Subscription.status == "ACTIVE")
        .count()
    )

    return {
        "status": "success",
        "data": {
            "total": total,
            "active": active
        }
    }
