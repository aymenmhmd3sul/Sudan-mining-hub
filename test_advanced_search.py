import asyncio
import json
from app.infrastructure.database import engine, AsyncSessionLocal
from app.domain.services.search import SearchService, SearchCriteria
from app.infrastructure.repositories.asset import AssetRepository
from app.infrastructure.utils.schema_sync import sync_schema
from app.infrastructure.models.core import Category, MiningAsset

# قاموس محلي لترجمة "درجات السمعة" بلهجة السوق السوداني (المبدأ الثاني والخامس)
def get_market_reputation_badge(score: float) -> str:
    if score >= 90: return "🏆 شريك احترافي"
    if score >= 80: return "⭐ تاجر معتمد"
    if score >= 70: return "🔹 موثق"
    if score >= 60: return "🟢 معروف"
    return "🆕 جديد"

async def run_search_engine_suite():
    # 1. المزامنة الذكية لهيكل الجداول
    await sync_schema()
    
    async with AsyncSessionLocal() as session:
        asset_repo = AssetRepository(session)
        search_service = SearchService(asset_repo)
        
        print("📝 [Seed]: التحقق من وجود تصنيفات خدمات التعدين المتكاملة...")
        
        # حقن تصنيفات الرؤية المستقبلية (آليات، خام، خدمات نقل)
        categories_to_seed = [
            {"name": "معدات وآليات ثقيلة", "slug": "heavy-machinery"},
            {"name": "خام ومعادن", "slug": "raw-minerals"},
            {"name": "خدمات النقل واللوجستيات", "slug": "mining-transport"}
        ]
        
        for cat_data in categories_to_seed:
            from sqlalchemy import select
            stmt = select(Category).where(Category.slug == cat_data["slug"])
            res = await session.execute(stmt)
            if not res.scalars().first():
                cat = Category(**cat_data)
                session.add(cat)
        await session.flush()

        # جلب تصنيف الآليات لاستخدامه في أصل تجريبي
        cat_stmt = select(Category).where(Category.slug == "heavy-machinery")
        cat_res = await session.execute(cat_stmt)
        machinery_category = cat_res.scalars().first()

        print("📝 [Seed]: حقن إعلان تجريبي يجسد (الإعلان هو بطل المنصة)...")
        asset_stmt = select(MiningAsset).where(MiningAsset.title == "غرابيل ذهب ومولدات كاتربيلر مستعملة")
        asset_res = await session.execute(asset_stmt)
        existing_asset = asset_res.scalars().first()
        
        if not existing_asset and machinery_category:
            # إعلان ببيانات تواصل مباشرة وخيارات دخل واضحة
            asset_data = {
                "title": "غرابيل ذهب ومولدات كاتربيلر مستعملة",
                "description": "معدات تصفية وغرابيل بحالة ممتازة جاهزة للعمل الفوري في مناطق أبو حمد. التوصيل متوفر.",
                "price": 18500000.0,
                "currency": "SDG",
                "listing_tier": "PREMIUM", # إعلان مميز (فرصة دخل)
                "status": "APPROVED",      # النشر أولاً ثم التحسين
                "seller_id": 202,
                "category_id": machinery_category.id,
                "views_count": 420,
                "favorites_count": 55,
                "trust_score": 92.0        # يترجم إلى شريك احترافي
            }
            location_data = {
                "state": "ولاية نهر النيل",
                "region": "أبو حمد",
                "latitude": "19.53",
                "longitude": "33.31"
            }
            specs_data = [
                {"spec_key": "الحالة", "spec_value": "مستعمل نظيف"},
                {"spec_key": "خيارات التواصل", "spec_value": "📞 اتصال مباشر + 💬 واتساب"}
            ]
            
            await asset_repo.create_asset_with_details(asset_data, location_data, specs_data)
            await session.commit()
            print("✨ [Seed]: تم بنجاح حقن الإعلان النموذجي بلهجة وسلوك السوق السوداني.")
        
        # 4. إجراء استعلام البحث المتقدم بناءً على فلسفة التيسير والتنقيب الذكي
        criteria_flow = SearchCriteria(
            status="APPROVED",
            state="ولاية نهر النيل",
            sort_by="INVESTOR_VIEW" # عرض تفاعلي مبني على السمعة وحجم الطلب
        )
        
        print("🧪 === بدء تشغيل محرك البحث المحدث بناءً على الدستور التأسيسي ===")
        response_flow = await search_service.execute_advanced_search(criteria_flow)
        
        # دمج شارات السمعة السودانية المحدثة في نتائج العرض قبل الطباعة
        for item in response_flow.get("results", []):
            # محاكاة حقن الشارات التدرجية للثقة (المبدأ الثاني)
            item["market_reputation"] = get_market_reputation_badge(item.get("score_rank", 50.0) / 1.5)
            # إضافة دليل خيارات التواصل السريع (المبدأ المعزز للتواصل)
            item["quick_connect"] = ["📞 زر الاتصال", "💬 رابط الواتساب السريع", "📍 الإحداثيات التقريبية"]

        print("✅ تم تنفيذ الاستعلام بنجاح وتوليد المخرجات الصديقة للمستخدم:")
        print(json.dumps(response_flow, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    asyncio.run(run_search_engine_suite())
