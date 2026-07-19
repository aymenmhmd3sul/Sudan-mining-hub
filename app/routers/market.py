from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.market_service import MarketService
from app.schemas.market import MarketStatsResponse

router = APIRouter(
    prefix="/api/v1/market",
    tags=["Market Engine"]
)

@router.get("/stats", response_model=MarketStatsResponse)
def get_market_statistics(db: Session = Depends(get_db)):
    """جلب بيانات السوق الحية (السعر العالمي، المحلي، النشاط)"""
    market_service = MarketService(db)
    return market_service.get_market_stats()
