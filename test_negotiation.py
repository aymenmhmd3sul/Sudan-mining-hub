import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService
from app.infrastructure.models.core import MiningAsset

async def test_negotiation_flow():
    print("💰 بدء اختبار نظام التفاوض وعروض الأسعار على الأصل رقم 1...")

    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        negotiation_service = NegotiationService(session, repo)

        # 1. التحقق من وجود الأصل وحقنه أو تحديث حالته إلى APPROVED ليتوافق مع الـ SecurityGuard
        asset = await repo.get_by_id(1)
        if not asset:
            print("   📝 لم يتم العثور على أصل تعديني برقم 1. جاري حقن أصل تجريبي نشط...")
            new_asset = MiningAsset(
                id=1,
                title="مطحنة ذهب تجريبية - أبو حمد",
                description="مطحنة رطبة لمعالجة مخلفات التعدين بحالة ممتازة",
                price=120000.0,
                currency="USD",
                listing_tier="PREMIUM",
                status="APPROVED",  # القيمة السحرية المطلوبة للحالة النشطة ✅
                seller_id=1001,
                category_id=2
            )
            session.add(new_asset)
            await session.commit()
            print("   ✅ تم حقن الأصل التعديني المعتمد [APPROVED] رقم 1 بنجاح!")
        else:
            if asset.status != "APPROVED":
                print(f"   🔄 حالة الأصل الحالية هي ({asset.status}). جاري تحويلها إلى (APPROVED)...")
                asset.status = "APPROVED"
                await session.commit()
                print("   ✅ تم تحديث حالة الأصل إلى [APPROVED] بنجاح!")

        # 2. محاولة فتح جلسة تفاوض رسمية
        print("\n🤝 جاري فتح جلسة تفاوض جديدة للمشتري رقم 2002 على الأصل 1...")
        success, message, negotiation = await negotiation_service.start_negotiation(
            asset_id=1, buyer_id="2002", role="BUYER"
        )

        if not success:
            print(f"   ⚠️ لم يتم فتح تفاوض جديد: {message}")
            if "بالفعل" in message:
                print("   ℹ️ سنحاول متابعة الفحص باستخدام الجلسة النشطة مسبقاً...")
                from sqlalchemy import select
                from app.infrastructure.models.interactions import AssetNegotiation
                stmt = select(AssetNegotiation).where(
                    AssetNegotiation.asset_id == 1, 
                    AssetNegotiation.buyer_id == 2002, 
                    AssetNegotiation.status == "OPEN"
                )
                res = await session.execute(stmt)
                negotiation = res.scalar_one_or_none()
                if negotiation:
                    success = True
                else:
                    print("   ❌ لم يتم العثور على الجلسة النشطة في قاعدة البيانات.")
                    return
            else:
                return

        neg_id = negotiation.id
        print(f"   ✅ الجلسة جاهزة. رقم جلسة التفاوض النشطة: {neg_id}")

        # 3. تقديم العرض المالي الحقيقي داخل الجلسة المفتوحة
        print(f"\n📥 جاري تقديم عرض مالي بقيمة 55,000$ داخل الجلسة رقم {neg_id}...")
        success_offer, msg_offer = await negotiation_service.create_offer(
            negotiation_id=neg_id, amount=55000.0, actor_id="2002", role="BUYER"
        )

        if success_offer:
            print(f"   ✅ نجاح: {msg_offer}")
            await session.commit()
            print("💾 تم حفظ وحقن عرض السعر بنجاح في قاعدة البيانات الموحدة local.db!")
        else:
            print(f"   ❌ فشل تقديم العرض: {msg_offer}")

if __name__ == '__main__':
    asyncio.run(test_negotiation_flow())
