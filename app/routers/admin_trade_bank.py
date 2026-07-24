from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.database import get_db
from app.core.dependencies import verify_admin_token
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/admin/operations",
    tags=["Admin Trade Desk, Investor & Banking Control"]
)

def get_current_admin(current_user: User = Depends(verify_admin_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": "admin"
    }

# --- Trade Desk Operations ---
@router.get("/trade-desk/summary")
def get_trade_desk_summary(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """إحصائيات حية لغرفة التداول والتفاوض Commercial Operations"""
    try:
        total_trades = db.execute(text("SELECT COUNT(*) FROM trade_desk")).scalar() if db.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'trade_desk')")).scalar() else 0
        total_negotiations = db.execute(text("SELECT COUNT(*) FROM negotiations")).scalar() if db.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'negotiations')")).scalar() else 0
    except Exception:
        total_trades, total_negotiations = 0, 0

    return {
        "status": "success",
        "data": {
            "active_trade_offers": total_trades,
            "ongoing_negotiations": total_negotiations,
            "status": "Live Operational"
        }
    }

# --- Investor Center Operations ---
@router.get("/investor-center/summary")
def get_investor_center_summary(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """ملخص فرص الاستثمار وطلبات الشركاء"""
    try:
        opportunities_count = db.execute(text("SELECT COUNT(*) FROM opportunities")).scalar() if db.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'opportunities')")).scalar() else 0
    except Exception:
        opportunities_count = 0

    return {
        "status": "success",
        "data": {
            "active_investment_opportunities": opportunities_count,
            "investor_portal_status": "Active"
        }
    }

# --- Banking & Settlements ---
@router.get("/banking/summary")
def get_banking_summary(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """إحصائيات الحسابات المصرفية والتسويات المالية"""
    try:
        bank_accounts_count = db.execute(text("SELECT COUNT(*) FROM bank_accounts")).scalar() if db.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'bank_accounts')")).scalar() else 0
    except Exception:
        bank_accounts_count = 0

    return {
        "status": "success",
        "data": {
            "registered_bank_accounts": bank_accounts_count,
            "settlement_gateway": "Connected"
        }
    }
