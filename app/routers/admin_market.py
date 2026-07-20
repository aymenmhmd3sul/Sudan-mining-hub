from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.market_service import MarketService
from app.schemas.market import PriceUpdateRequest

router = APIRouter(
    prefix="/api/v1/admin/market",
    tags=["Admin Market Control"]
)

from app.core.dependencies import verify_admin_token
from app.models.user import User

def get_current_admin(current_user: User = Depends(verify_admin_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": "admin"
    }

@router.patch("/gold-price")
def update_gold_price(
    request: PriceUpdateRequest,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """تحديث السعر المحلي وتسجيل العملية في سجل التدقيق"""
    market_service = MarketService(db)
    audit_record = market_service.update_local_price(
        new_price=request.price,
        reason=request.reason,
        admin_id=admin["id"]
    )
    return {
        "status": "updated",
        "old_price": audit_record.old_price,
        "new_price": audit_record.new_price,
        "audit_id": f"AUD-{audit_record.id}"
    }
