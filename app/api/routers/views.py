from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any, List
from app.api.deps import get_db_session
from app.infrastructure.models.core import MiningAsset, Category
from app.infrastructure.models.interactions import AssetReport

router = APIRouter(prefix="/web-views", tags=["MVP Web Views"])

# ----------------------------------------------------------------
# 1. الصفحة الرئيسية - سوق حقيقي (Home View)
# ----------------------------------------------------------------
@router.get("/home", response_model=Dict[str, Any])
async def get_home_page_context(db: AsyncSession = Depends(get_db_session)):
    """توليد بيانات الصفحة الرئيسية: محرك البحث، التصنيفات، وأحدث الحركة في السوق"""
    
    # جلب أحدث 6 إعلانات نشطة ومقبولة
    latest_stmt = select(MiningAsset).where(MiningAsset.status == "APPROVED").order_by(MiningAsset.created_at.desc()).limit(6)
    latest_res = await db.execute(latest_stmt)
    latest_assets = latest_res.scalars().all()
    
    # جلب الإعلانات المميزة (فرص الدخل)
    premium_stmt = select(MiningAsset).where(MiningAsset.status == "APPROVED", MiningAsset.listing_tier == "PREMIUM").limit(3)
    premium_res = await db.execute(premium_stmt)
    premium_assets = premium_res.scalars().all()
    
    return {
        "hero_section": {
            "title": "سوق التعدين السوداني المفتوح",
            "search_placeholder": "ابحث عن: بوكلين، غرابيل، خام ذهب، أو خدمات نقل..."
        },
        "premium_listings": [
            {"id": a.id, "title": a.title, "price": a.price, "currency": a.currency} for a in premium_assets
        ],
        "latest_market_listings": [
            {"id": a.id, "title": a.title, "price": a.price, "currency": a.currency, "created_at": a.created_at.isoformat()} for a in latest_assets
        ],
        "active_hubs": [
            {"state": "ولاية نهر النيل", "listings_count": len(latest_assets)},
            {"state": "الولاية الشمالية", "listings_count": 0}
        ],
        "primary_action": "أضف إعلانك الآن في دقيقة"
    }

# ----------------------------------------------------------------
# 2. صفحة تفاصيل الإعلان (Asset Detail View)
# ----------------------------------------------------------------
@router.get("/asset/{asset_id}", response_model=Dict[str, Any])
async def get_asset_detail_page(asset_id: int, db: AsyncSession = Depends(get_db_session)):
    """أهم صفحة في المشروع: تجمع كل تفاصيل التاجر وخيارات التواصل الفوري"""
    stmt = select(MiningAsset).where(MiningAsset.id == asset_id)
    res = await db.execute(stmt)
    asset = res.scalars().first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="الإعلان المطلوب غير موجود أو تم نقله.")
        
    asset.views_count += 1
    await db.commit()
    
    reputation_badge = "🏆 شريك احترافي" if asset.trust_score >= 90 else "⭐ تاجر معتمد" if asset.trust_score >= 70 else "🆕 جديد في السوق"
    
    return {
        "asset_details": {
            "id": asset.id,
            "title": asset.title,
            "description": asset.description,
            "price": asset.price or "على السوم / الاتصال",
            "currency": asset.currency,
            "status": asset.status,
            "views": asset.views_count,
            "reputation": reputation_badge
        },
        "quick_connect_actions": {
            "phone_call": "اضغط للاتصال المباشر",
            "whatsapp_chat": "فتح محادثة واتساب فورية",
            "negotiation_trigger": "بدء تفاوض رسمي عبر المنصة"
        }
    }

# ----------------------------------------------------------------
# 3. لوحة الإدارة: مركز القيادة والتشغيل (Control Center Dashboard)
# ----------------------------------------------------------------
@router.get("/admin/control-center", response_model=Dict[str, Any])
async def get_admin_control_center(db: AsyncSession = Depends(get_db_session)):
    """لوحة التحكم الشاملة للمشرف كأداة تشغيل وإدارة للأعمال"""
    
    total_assets = await db.scalar(select(func.count(MiningAsset.id)))
    under_review_assets = await db.scalar(select(func.count(MiningAsset.id)).where(MiningAsset.status == "UNDER_REVIEW"))
    pending_reports = await db.scalar(select(func.count(AssetReport.id)).where(AssetReport.status == "PENDING"))
    
    return {
        "overview_cards": {
            "active_listings_count": total_assets - under_review_assets,
            "under_review_count": under_review_assets,
            "pending_reports_count": pending_reports
        },
        "modules": {
            "subscriptions_management": ["باقة مجانية", "باقة تاجر معتمد", "باقة شركات التعدين الذهبية"],
            "commission_ledger": {
                "status": "متاح للتعديل الذكي بحسب نوع الأصل وحجم الصفقة",
                "summary": {"صفقات مكتملة": 0, "عمولات مستحقة": "0 SDG", "عمولات محصلة": "0 SDG"}
            },
            "reports_pipeline": "نظام الإدارة بالاستثناء نشط ويرسل التنبيهات تلقائياً"
        }
    }
