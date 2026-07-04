import asyncio
from app.infrastructure.database import AsyncSessionLocal, async_engine, Base
from app.infrastructure.repositories.asset import AssetRepository
from app.infrastructure.models.core import Category

async def seed_first_mining_asset():
    print("⏳ جاري تهيئة الجداول وبناء قاعدة البيانات المحلية...")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        async with session.begin():
            category = await session.get(Category, 1)
            if not category:
                print("📦 حقن القسم الافتراضي (مربعات الذهب التعدينية)...")
                new_category = Category(id=1, name="مربعات تعدين الذهب", slug="gold-mining-blocks")
                session.add(new_category)
                await session.flush()

            repo = AssetRepository(session)
            
            asset_data = {
                "title": "مربع تعديني رقم 45 - ولاية نهر النيل",
                "description": "مربع تعديني غني بعروق المرو الحاملة للذهب، يحتوي على آبار حفر تقليدي جاهزة للتطوير.",
                "seller_id": 1001,
                "category_id": 1,
                "status": "DRAFT"
            }
            
            # تم تصحيح الحقل هنا من locality إلى region
            location_data = {
                "state": "نهر النيل",
                "region": "بربر",
                "latitude": 18.0123,
                "longitude": 33.9876
            }
            
            specs_list = [
                {"spec_key": "نوع الترخيص", "spec_value": "امتياز استكشاف عام"},
                {"spec_key": "المساحة", "spec_value": "4 كيلومتر مربع"}
            ]
            
            new_asset = await repo.create_asset_with_details(asset_data, location_data, specs_list)
            print(f"✅ تم إنشاء الأصل في الذاكرة المؤقتة بنجاح، المعرف: {new_asset.id}")
            
        print("💾 تم حفظ المعاملة (Commit) بالكامل داخل قاعدة البيانات بنجاح.")

    print("\n🔍 جاري اختبار الاسترجاع الذكي (Eager Loading)...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        rich_asset = await repo.get_rich_asset_by_id(1)
        
        if rich_asset:
            print(f"📋 اسم الأصل المسترجع: {rich_asset.title}")
            print(f"📍 الموقع: ولاية {rich_asset.locations[0].state} - المحلية/المنطقة: {rich_asset.locations[0].region}")
            print(f"🔬 عدد المواصفات المرتبطة: {len(rich_asset.specs)}")
            for spec in rich_asset.specs:
                print(f"   - {spec.spec_key}: {spec.spec_value}")
        else:
            print("❌ فشل استرجاع الأصل.")

if __name__ == "__main__":
    asyncio.run(seed_first_mining_asset())
