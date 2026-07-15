import asyncio
from app.infrastructure.database import engine, Base

# استيراد الموديلات صراحة ليتعرف عليها الـ Metadata الخاص بالـ Base
from app.infrastructure.models.core import MiningAsset
from app.infrastructure.models.extensions import AssetLocation, AssetSpec, AssetImage, AssetDocument
from app.infrastructure.models.interactions import AssetNegotiation, AssetEvent

async def init_db():
    print("🚀 جاري تهيئة قاعدة البيانات وبناء الجداول الـ 18 للأقسام...")
    async with engine.begin() as conn:
        # إنشاء الجداول إذا لم تكن موجودة مسبقاً
        await conn.run_sync(Base.metadata.create_all)
    print("✅ تم بناء وتحديث كافة الجداول بنجاح في local.db!")

if __name__ == "__main__":
    asyncio.run(init_db())
