from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, List
from app.api.deps import get_db_session
from app.infrastructure.models.core import MiningAsset

router = APIRouter(prefix="/commercial", tags=["Commercial MVP Engine"])

# ----------------------------------------------------------------
# القواعد التجارية الحية (تتحول إلى متغيرات قابلة للتعديل ديناميكياً)
# ----------------------------------------------------------------
TIER_RULES = {
    "FREE": {"max_listings": 5, "badge": "🆕 جديد", "boost": 1.0, "analytics": "أساسية", "price": 0},
    "TRADER": {"max_listings": 30, "badge": "⭐ معروف", "boost": 2.0, "analytics": "متوسطة", "price": 50000},
    "VERIFIED": {"max_listings": 999, "badge": "👑 معتمد", "boost": 3.5, "analytics": "متقدمة", "price": 150000},
    "COMPANY": {"max_listings": 9999, "badge": "🏢 مؤسسة", "boost": 5.0, "analytics": "شاملة", "price": 400000}
}

COMMISSION_POLICY = {
    "heavy-machinery": {"type": "FIXED", "value": 50000, "label": "عمولة ثابتة للمعدات الثقيلة"},
    "raw-materials": {"type": "PERCENTAGE", "value": 0.015, "label": "1.5% من إجمالي صفقة الخام"},
    "services": {"type": "FREE", "value": 0, "label": "خدمات التعدين مجانية تماماً لتشغيل السوق"},
    "default": {"type": "PERCENTAGE", "value": 0.01, "label": "1% عمولة افتراضية"}
}

PAID_PROMOTIONS = {
    "FEATURED_7_DAYS": {"price": 15000, "description": "إعلان مميز لمدة 7 أيام"},
    "URGENT": {"price": 10000, "description": "إشارة عاجل لسرعة البيع"},
    "TOP_BOOST": {"price": 25000, "description": "تثبيت الإعلان أعلى نتائج البحث"}
}

# ----------------------------------------------------------------
# نماذج الطلبات الخاصة بـ "لوحة تحكم المشرف" لتعديل السياسات
# ----------------------------------------------------------------
class UpdateTierPricePayload(BaseModel):
    tier_name: str = Field(..., description="FREE, TRADER, VERIFIED, COMPANY")
    new_price: float
    max_listings: int

class UpdateCommissionPayload(BaseModel):
    category_slug: str = Field(..., description="heavy-machinery, raw-materials, services, default")
    policy_type: str = Field(..., description="FIXED, PERCENTAGE, FREE")
    value: float
    label: str

# ----------------------------------------------------------------
# مسارات تحكم المشرف (Admin Control Endpoints)
# ----------------------------------------------------------------
@router.post("/admin/settings/tier")
async def admin_update_tier_settings(payload: UpdateTierPricePayload):
    """تحديث أسعار ومميزات الباقات فوراً من لوحة التحكم"""
    if payload.tier_name not in TIER_RULES:
        raise HTTPException(status_code=400, detail="الباقة المستهدفة غير موجودة.")
    
    TIER_RULES[payload.tier_name]["price"] = payload.new_price
    TIER_RULES[payload.tier_name]["max_listings"] = payload.max_listings
    
    return {
        "status": "success",
        "message": f"⚙️ تم تحديث إعدادات باقة ({payload.tier_name}) بنجاح وتطبيقها في السوق",
        "current_rule": TIER_RULES[payload.tier_name]
    }

@router.post("/admin/settings/commission")
async def admin_update_commission_policy(payload: UpdateCommissionPayload):
    """تعديل سياسة العمولات والنسب لأي تصنيف فوراً من لوحة التحكم"""
    if payload.policy_type not in ["FIXED", "PERCENTAGE", "FREE"]:
        raise HTTPException(status_code=400, detail="نوع السياسة المالي غير مدعوم.")
        
    COMMISSION_POLICY[payload.category_slug] = {
        "type": payload.policy_type,
        "value": payload.value,
        "label": payload.label
    }
    return {
        "status": "success",
        "message": f"📈 تم تعديل سياسة عمولة التصنيف ({payload.category_slug}) فوراً بنجاح",
        "current_policy": COMMISSION_POLICY[payload.category_slug]
    }

# ----------------------------------------------------------------
# المسارات التشغيلية والتجارية (تعتمد على المتغيرات الحية المحمية)
# ----------------------------------------------------------------
class UpgradePayload(BaseModel):
    trader_id: int
    target_tier: str

class PromoteAssetPayload(BaseModel):
    asset_id: int
    promotion_type: str

@router.post("/trader/upgrade")
async def upgrade_trader_tier(payload: UpgradePayload):
    if payload.target_tier not in TIER_RULES:
        raise HTTPException(status_code=400, detail="الباقة المطلوبة غير مدعومة.")
    rule = TIER_RULES[payload.target_tier]
    return {
        "status": "success",
        "message": f"🎉 تم ترقية حسابك إلى باقة ({payload.target_tier})",
        "features": {
            "شارة الحساب": rule["badge"],
            "حد الإعلانات المتاحة": rule["max_listings"],
            "تكلفة الاشتراك الحالية": f"{rule['price']:,} SDG",
            "مستوى ظهور الإعلانات": f"مضاعف بمقدار x{rule['boost']}"
        }
    }

@router.post("/asset/promote")
async def apply_paid_promotion(payload: PromoteAssetPayload, db: AsyncSession = Depends(get_db_session)):
    if payload.promotion_type not in PAID_PROMOTIONS:
        raise HTTPException(status_code=400, detail="نوع الترويج غير صحيح.")
    stmt = select(MiningAsset).where(MiningAsset.id == payload.asset_id)
    res = await db.execute(stmt)
    asset = res.scalars().first()
    if not asset:
        raise HTTPException(status_code=404, detail="الإعلان غير موجود.")
    asset.listing_tier = "PREMIUM"
    await db.commit()
    promo = PAID_PROMOTIONS[payload.promotion_type]
    return { "status": "success", "invoice_amount": f"{promo['price']} SDG" }

@router.get("/calculate-commission/{category_slug}")
async def get_calculated_commission(category_slug: str, deal_value: float):
    policy = COMMISSION_POLICY.get(category_slug, COMMISSION_POLICY["default"])
    calculated_fee = 0.0
    if policy["type"] == "FIXED":
        calculated_fee = float(policy["value"])
    elif policy["type"] == "PERCENTAGE":
        calculated_fee = deal_value * policy["value"]
    return {
        "category": category_slug,
        "policy_applied": policy["label"],
        "deal_value": f"{deal_value:,.2f} SDG",
        "estimated_commission": f"{calculated_fee:,.2f} SDG"
    }

@router.get("/admin/revenues", response_model=Dict[str, Any])
async def get_admin_revenue_dashboard(db: AsyncSession = Depends(get_db_session)):
    return {
        "financial_snapshot": { "daily_revenues": "120,000 SDG", "monthly_revenues": "3,450,000 SDG", "pending_commissions": "850,000 SDG" },
        "current_system_controls": {
            "active_subscriptions_pricing": {k: f"{v['price']:,} SDG (حد الإعلانات: {v['max_listings']})" for k, v in TIER_RULES.items()},
            "active_commission_policies": {k: v["label"] for k, v in COMMISSION_POLICY.items()}
        },
        "revenue_streams_breakdown": { "subscriptions": "60%", "paid_promotions": "30%", "transaction_commissions": "10%" },
        "top_customers": [
            {"trader_id": 1024, "business_name": "مجموعة وادي السليك للتعدين", "tier": "COMPANY", "total_spent": "750,000 SDG"}
        ]
    }

@router.get("/trader/dashboard/{asset_id}", response_model=Dict[str, Any])
async def get_trader_asset_dashboard(asset_id: int, db: AsyncSession = Depends(get_db_session)):
    stmt = select(MiningAsset).where(MiningAsset.id == asset_id)
    res = await db.execute(stmt)
    asset = res.scalars().first()
    if not asset: raise HTTPException(status_code=404, detail="الإعلان غير موجود.")
    views = asset.views_count
    growth_tips = []
    if views < 50: growth_tips.append("💡 إعلانك يحتاج لظهور أوسع. رقّ إعلانك إلى باقة (عاجل).")
    return {
        "asset_summary": {"id": asset.id, "title": asset.title, "current_tier": asset.listing_tier},
        "interaction_analytics": { "views_count": views, "estimated_phone_clicks": int(views * 0.15), "estimated_whatsapp_clicks": int(views * 0.25) },
        "tailored_recommendations": growth_tips if growth_tips else ["✅ أداء مثالي!"]
    }
