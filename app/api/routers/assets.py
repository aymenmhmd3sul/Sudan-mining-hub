from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session  # اعتماداً على بنية deps المتوفرة لديك
from app.infrastructure.repositories.asset import AssetRepository

router = APIRouter(prefix="/assets", tags=["Assets"])

# 1. شحن المخطط البرمجي (Schema) بأقل قيود ممكنة - المبدأ الأول: انشر في دقيقة
class AssetCreateFlexible(BaseModel):
    title: str = Field(..., max_length=255, description="عنوان الإعلان")
    category_slug: str = Field(..., description="نوع الأصل مثلاً heavy-machinery")
    state: str = Field(..., description="الولاية")
    phone_number: str = Field(..., description="رقم التواصل المباشر (مفتاح العبور والسوق)")
    primary_image_url: str = Field(..., description="صورة واحدة على الأقل لإطلاق الإعلان")
    
    # حقول اختيارية تماماً لا تعيق النشر
    price: Optional[float] = None
    currency: Optional[str] = "SDG"
    description: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    license_type: Optional[str] = None

@router.post("/create-flexible", status_code=status.HTTP_201_CREATED)
async def create_asset_flexible(payload: AssetCreateFlexible, db: AsyncSession = Depends(get_db_session)):
    """
    مسار استقبال الإعلانات المرن لعام 2026:
    يستقبل الحد الأدنى، ينشر فوراً، ثم يقدم اقتراحات ذكية تخدم مصلحة البائع.
    """
    asset_repo = AssetRepository(db)
    
    # جلب التصنيف برفق للتأكد من ربطه
    from sqlalchemy import select
    from app.infrastructure.models.core import Category
    cat_stmt = select(Category).where(Category.slug == payload.category_slug)
    cat_res = await db.execute(cat_stmt)
    category = cat_res.scalars().first()
    
    if not category:
        raise HTTPException(status_code=400, detail="نوع الأصل المختار غير مدرج في المنظومة حالياً.")

    # صياغة بيانات الأصل الأساسية بحالة معتمدة مباشرة (النشر أولاً)
    asset_data = {
        "title": payload.title,
        "description": payload.description or "لا يوجد وصف تفصيلي حالياً.",
        "price": payload.price,
        "currency": payload.currency,
        "listing_tier": "REGULAR", 
        "status": "APPROVED",  # معتمد وتلقائي ليبقى السوق نشطاً
        "seller_id": 999,      # معرف افتراضي للبائع يتم استبداله من الـ Token لاحقاً
        "category_id": category.id,
        "views_count": 0,
        "favorites_count": 0,
        "trust_score": 50.0    # يبدأ كـ (🆕 جديد) لتبدأ السمعة بالتدريج
    }
    
    location_data = {
        "state": payload.state,
        "region": payload.region,
        "latitude": payload.latitude,
        "longitude": payload.longitude
    }
    
    # حصر الخصائص الفنية المتاحة
    specs_data = []
    if payload.license_type:
        specs_data.append({"spec_key": "نوع الترخيص", "spec_value": payload.license_type})
    specs_data.append({"spec_key": "الهاتف المعتمد", "spec_value": payload.phone_number})
    
    # الحفظ الفوري في قاعدة البيانات
    new_asset = await asset_repo.create_asset_with_details(asset_data, location_data, specs_data)
    await db.commit()

    # 2. توليد البطاقات التشجيعية الذكية بناءً على الحقول الغائبة (المبدأ الأول والثالث)
    tips_and_nudges = []
    if not payload.price:
        tips_and_nudges.append("⭐ أضف السعر المتوقع لتوفير كثرة الاتصالات والاستفسارات الجانبية عليك.")
    if not payload.description or len(payload.description) < 20:
        tips_and_nudges.append("📝 إضافة تفاصيل حالة المعدة أو موقع الخام تزيد من رغبة المستثمرين بالدخول في صفقات فورية.")
    if not payload.latitude or not payload.longitude:
        tips_and_nudges.append("📍 تحديد الموقع التقريبي عبر الخريطة يرفع نسبة ظهور الإعلان للباحثين القريبين منك.")
    if not payload.license_type:
        tips_and_nudges.append("🛡️ إرفاق نوع الترخيص والمستندات يمنحك شارة 'موثق' لتبني سمعة أسرع في السوق.")

    # 3. صياغة روابط التواصل الفورية لتسهيل الحركة والتبادل (فلسفة التواصل)
    # تنظيف رقم الهاتف وصياغة رابط واتساب مباشر وبنص مخصص
    clean_phone = payload.phone_number.replace("+", "").strip()
    whatsapp_text = f"السلام عليكم، مستفسر بخصوص إعلانك على المنصة: ({payload.title})"
    import urllib.parse
    encoded_text = urllib.parse.quote(whatsapp_text)
    whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_text}"

    return {
        "message": "🎉 تم نشر إعلانك بنجاح وهو متاح في السوق الآن!",
        "asset_id": new_asset.id,
        "status": "APPROVED",
        "market_action_buttons": {
            "call_action": f"tel:{payload.phone_number}",
            "whatsapp_action": whatsapp_url,
            "save_action": True
        },
        "growth_cards": tips_and_nudges if tips_and_nudges else ["✅ إعلانك مكتمل ومثالي لجذب أقوى الصفقات!"]
    }
