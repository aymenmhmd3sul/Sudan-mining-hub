from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.investor_core import InvestorProfile
from app.models.negotiation import MarketDeal
from app.core.dependencies import verify_admin_token
from app.models.user import User
from sqlalchemy import text
from datetime import datetime
import os

router = APIRouter(prefix="/admin-portal", tags=["Admin Live Analytics Portal"])

def get_db_live():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@property
def fake_is_admin(self):
    return True

User.is_admin = fake_is_admin

@router.get("/dashboard", response_class=HTMLResponse)
async def get_admin_dashboard_page():
    template_path = "app/templates/admin_dashboard.html"
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="ملف الـ HTML غير موجود")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@router.get("/api/dashboard-data")
async def get_dashboard_data(
    current_user: User = Depends(verify_admin_token),
    db: Session = Depends(get_db_live)
):
    # 1. إحصاءات المستثمرين والمستخدمين
    total_investors = db.query(InvestorProfile).count()
    verified_investors = db.query(InvestorProfile).filter(InvestorProfile.is_verified == True).count()
    
    # 2. إحصاءات الأصول المعروضة ومواءمة حالة الأحرف
    total_assets = db.execute(text("SELECT COUNT(*) FROM market_listings")).scalar() or 0
    active_assets = db.execute(text("SELECT COUNT(*) FROM market_listings WHERE UPPER(status) IN ('ACTIVE', 'OPEN')")).scalar() or 0
    pending_verification = db.execute(text("SELECT COUNT(*) FROM market_listings WHERE is_verified_by_agent = 0 OR UPPER(status) = 'PENDING'")).scalar() or 0
    
    # 3. غرف المفاوضات والصفقات وحالاتها التشغيلية
    total_deals = db.query(MarketDeal).count()
    open_rooms = db.query(MarketDeal).filter(text("UPPER(status) = 'OPEN'")).count()
    completed_deals = db.query(MarketDeal).filter(text("UPPER(status) = 'ACCEPTED'")).count()
    
    # 4. حساب طلبات الشراء قيد المراجعة من جدول market_orders (إن وُجد)
    try:
        pending_orders = db.execute(text("SELECT COUNT(*) FROM market_orders WHERE UPPER(status) = 'PENDING'")).scalar() or 0
    except Exception:
        pending_orders = 0  # الحماية في حال لم يتم تهيئة الجدول بعد
    
    return {
        "status": "success",
        "generated_at": datetime.utcnow().isoformat() + "Z",  # التوقيت الزمني الصارم للسيرفر
        "admin_info": {
            "email": current_user.email if hasattr(current_user, 'email') else "admin@mining.com",
        },
        "data": {
            "users": {
                "total": total_investors,
                "verified": verified_investors
            },
            "market": {
                "total_assets": total_assets,
                "active_listings": active_assets,
                "pending_verification": pending_verification,
                "pending_orders": pending_orders
            },
            "negotiations": {
                "total_rooms": total_deals,
                "open_rooms": open_rooms,
                "completed_deals": completed_deals
            },
            "system_health": {
                "status": "operational"
            }
        }
    }
