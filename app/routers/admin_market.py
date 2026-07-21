from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.services.market_service import MarketService
from app.schemas.market import PriceUpdateRequest
from app.core.dependencies import verify_admin_token
from app.models.user import User
from app.models.market_core import MarketListing, MarketOrder, AssetItem
from app.models.marketplace import MiningAsset

router = APIRouter(
    prefix="/api/v1/admin/market",
    tags=["Admin Market Control"]
)

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

@router.get("/stats")
def get_market_stats(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """جلب إحصائيات السوق الحية للوحة التحكم"""
    total_assets = db.query(MiningAsset).count() if hasattr(MiningAsset, 'id') else 0
    total_listings = db.query(MarketListing).count() if hasattr(MarketListing, 'id') else 0
    total_orders = db.query(MarketOrder).count() if hasattr(MarketOrder, 'id') else 0

    return {
        "status": "success",
        "data": {
            "total_assets": total_assets,
            "total_listings": total_listings,
            "total_orders": total_orders
        }
    }

@router.get("/listings")
def list_market_listings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """استعراض قائمة الأصول والعروض المعروضة في السوق"""
    listings = db.query(MarketListing).offset(skip).limit(limit).all()
    return {
        "status": "success",
        "count": len(listings),
        "data": listings
    }

@router.get("/orders")
def list_market_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """متابعة طلبات الشراء والبيع في السوق"""
    orders = db.query(MarketOrder).offset(skip).limit(limit).all()
    return {
        "status": "success",
        "count": len(orders),
        "data": orders
    }
