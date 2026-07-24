from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.finance_service import FinanceService

router = APIRouter(
    prefix="/api/v1/finance",
    tags=["Finance Center"]
)

@router.get("/banks")
def get_active_banks(db: Session = Depends(get_db)):
    """جلب قائمة البنوك المفعلة للمستخدمين"""
    finance = FinanceService(db)
    banks = finance.get_active_banks()
    return {"status": "success", "count": len(banks), "data": banks}

@router.get("/rates/{currency_code}")
def get_exchange_rate(currency_code: str, db: Session = Depends(get_db)):
    """جلب سعر الصرف الحي لعملة محددة"""
    finance = FinanceService(db)
    rate = finance.get_exchange_rate(currency_code.upper())
    if not rate:
        raise HTTPException(status_code=404, detail="Currency not found or not supported")
    return {"status": "success", "currency": currency_code.upper(), "rate": rate}
