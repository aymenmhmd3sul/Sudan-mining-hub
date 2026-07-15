import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService
from app.infrastructure.models.interactions import AssetNegotiation

# محاكاة لخدمة حالات الأصول (Asset State Service) المطلوبة لتغيير الحالات
class MockAssetStateService:
    async def transition_status(self, asset_id, to_state, actor, actor_id, role, reason):
        print(f"   🔄 [Mock State Service] جاري نقل حالة الأصل {asset_id} إلى [{to_state}] بواسطة {actor}...")
        return True, "تم الانتقال بنجاح"

async def test_accept_flow():
    print("🚀 بدء اختبار قبول العرض المالي وحجز الأصل...")

    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        negotiation_service = NegotiationService(session, repo)
        mock_state_service = MockAssetStateService()

        # 1. فتح جلسة تفاوض منافسة ثانية للمشتري 3003 لتجربة الإغلاق التلقائي (Auto-close)
        print("\n👥 محاولة فتح تفاوض منافس ثانٍ للمشتري رقم 3003 على الأصل 1...")
        success, msg, negotiation_2 = await negotiation_service.start_negotiation(
            asset_id=1, buyer_id="3003", role="BUYER"
        )
        if success:
            print(f"   ✅ تم فتح التفاوض المنافس رقم: {negotiation_2.id}")
            # تقديم عرض منافس بقيمة 52,000$
            await negotiation_service.create_offer(
                negotiation_id=negotiation_2.id, amount=52000.0, actor_id="3003", role="BUYER"
            )
        else:
            print(f"   ℹ️ تنبيه/تخطي: {msg}")

        await session.commit()

        # 2. الآن البائع (seller_id = 1001) يقرر قبول عرض المشتري الأول (جلسة التفاوض رقم 1) بقيمة 55,000$
        print("\n🤝 البائع (1001) يقوم بقبول العرض المالي في جلسة التفاوض رقم 1...")
        
        # البائع هو المالك للأصل رقم 1 (seller_id = 1001)
        success_accept, msg_accept = await negotiation_service.accept_offer(
            negotiation_id=1,
            asset_state_service=mock_state_service,
            actor_id="1001",
            role="SELLER"
        )

        if success_accept:
            print(f"\n🎉 {msg_accept}")
            await session.commit()
            print("💾 تم حفظ التغييرات وإغلاق الجلسات المنافسة في قاعدة البيانات الموحدة local.db!")
            
            # التحقق من تحديث حالة الجلسة المنافسة
            from sqlalchemy import select
            stmt = select(AssetNegotiation).where(AssetNegotiation.buyer_id == 3003)
            res = await session.execute(stmt)
            neg_3003 = res.scalar_one_or_none()
            if neg_3003:
                print(f"   📌 حالة تفاوض المشتري المنافس (3003) الحالية هي: [{neg_3003.status}]")
        else:
            print(f"   ❌ فشل قبول العرض: {msg_accept}")

if __name__ == '__main__':
    asyncio.run(test_accept_flow())
