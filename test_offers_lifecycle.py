import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService, NegotiationStatus
from app.domain.services.asset_state import AssetStateService
# الاستيراد المفقود الذي تسبب في الـ NameError
from app.infrastructure.models.interactions import AssetNegotiation

async def run_offers_cascade_test():
    print("🧪 === بدء اختبار محرك العروض المالية وقاعدة الإغلاق المتتالي الموحدة ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        neg_service = NegotiationService(session, repo)
        state_service = AssetStateService(repo)
        
        # 1. إنشاء مربع ذهب منشور ومتاح في السوق (APPROVED) يملكه البائع 5001
        asset_data = {"title": "مربع امتياز الذهب 88 - بربر", "description": "مربع غني بالخامات متاح للاستثمار", "category_id": 1, "seller_id": 5001, "status": "DRAFT"}
        location_data = {"state": "ولاية نهر النيل", "region": "بربر"}
        asset = await repo.create_asset_with_details(asset_data, location_data, [])
        await session.commit()
        
        await state_service.transition_status(asset.id, "PENDING_REVIEW", "Seller_5001", "5001", "SELLER")
        await state_service.transition_status(asset.id, "APPROVED", "Admin_Inspector", "99", "ADMIN")
        await session.commit()
        
        print(f"\n📢 الأصل التعديني [{asset.id}] معتمد الآن في الماركت بليس.")

        # 2. دخول المستثمر الأول (2002) وفتح جلسة تفاوض مع تقديم عرض بقيمة 75,000$
        _, _, neg_1 = await neg_service.start_negotiation(asset.id, buyer_id="2002", role="BUYER")
        await neg_service.create_offer(neg_1.id, amount=75000.0, actor_id="2002", role="BUYER")
        print(f"📥 المستثمر الأول [2002] قدّم عرض سعر بقيمة: 75,000$")

        # 3. دخول المستثمر الثاني (3003) وفتح جلسة تفاوض موازية وتقديم عرض بقيمة 85,000$
        _, _, neg_2 = await neg_service.start_negotiation(asset.id, buyer_id="3003", role="BUYER")
        await neg_service.create_offer(neg_2.id, amount=85000.0, actor_id="3003", role="BUYER")
        print(f"📥 المستثمر الثاني [3003] قدّم عرض سعر منافس بقيمة: 85,000$")

        # 4. البائع (5001) يقرر قبول عرض المستثمر الأول (75,000$) لأسباب تشغيلية أو موثوقية
        print(f"\n💰 البائع [5001] يتخذ قراراً بقبول عرض المستثمر الأول (رقم الجلسة: {neg_1.id})...")
        success, message = await neg_service.accept_offer(
            negotiation_id=neg_1.id, asset_state_service=state_service, actor_id="5001", role="SELLER"
        )
        print(f"📌 رد المحرك: {message}")
        await session.commit()

        # 5. التدقيق الختامي للأمان: التحقق من تفعيل قاعدة الحظر المتتالي والإغلاق التلقائي للمنافسين
        print("\n🔍 [تدقيق نزاهة النظام]: جاري فحص حالة المفاوضات المنافسة في قاعدة البيانات...")
        
        from sqlalchemy import select
        # إعادة قراءة حالة جلسة المستثمر الثاني
        stmt_2 = select(AssetNegotiation).where(AssetNegotiation.id == neg_2.id)
        res_2 = await session.execute(stmt_2)
        fresh_neg_2 = res_2.scalar_one()
        
        print(f"📊 حالة جلسة المستثمر الثاني [3003] الحالية: [{fresh_neg_2.status}]")
        
        # جلب حالة الأصل النهائية المتأصلة في النظام
        updated_asset = await repo.get_by_id(asset.id)
        print(f"📊 حالة الأصل النهائية في النظام: [{updated_asset.status}]")

        if fresh_neg_2.status == NegotiationStatus.CLOSED and updated_asset.status == "RESERVED":
            print("\n🎉 [نجاح هندسي تام]: تم حجز الأصل، وتحصين النظام وإلغاء عروض المنافسين تلقائياً وبأمان كامل!")
        else:
            print("\n❌ [خطأ في قاعدة العمل]: النظام ترك النوافذ مفتوحة للمنافسين المتزامنين!")

if __name__ == "__main__":
    asyncio.run(run_offers_cascade_test())
