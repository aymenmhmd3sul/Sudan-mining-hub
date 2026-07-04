import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService

async def test_negotiation_flow():
    print("💰 بدء اختبار نظام التفاوض وعروض الأسعار على الأصل رقم 1...")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        negotiation_service = NegotiationService(repo)
        
        # تقديم عرض سعر إضافي للتأكد من التراكم الصحيح للبيانات
        print("\n📥 جاري تقديم عرض مالي بقيمة 55,000$ من المشتري رقم 2002...")
        success, message = await negotiation_service.submit_offer(
            asset_id=1, buyer_id=2002, offer_price=55000.0
        )
        
        if success:
            print(f"   ✅ نجاح: {message}")
            await session.commit()
            print("💾 تم حفظ عرض السعر بنجاح في قاعدة البيانات.")
        else:
            print(f"   ❌ فشل: {message}")

    # الاختبار العكسي الصحيح: جلب الأصل ومراجعة العلاقة الصحيحة (negotiations)
    print("\n🔍 جاري الاستعلام عن الأصل عبر العلاقة الصحيحة (negotiations)...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        rich_asset = await repo.get_rich_asset_by_id(1)
        
        if rich_asset:
            print(f"📋 اسم الأصل المستهدف: {rich_asset.title}")
            print(f"⚖️ حالة الأصل الحالية: {rich_asset.status}")
            print(f"💬 إجمالي العروض والمفاوضات النشطة: {len(rich_asset.negotiations)} عرض")
            
            # قراءة سجل المفاوضات الفعلي
            for offer in rich_asset.negotiations:
                print(f"   - عرض سعر بقيمة: {offer.current_offer_price}$ | بواسطة المشتري: {offer.buyer_id} | حالة العرض: {offer.status}")
        else:
            print("❌ فشل استرجاع الأصل.")

if __name__ == "__main__":
    asyncio.run(test_negotiation_flow())
