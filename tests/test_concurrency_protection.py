import asyncio
from datetime import datetime
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService
from app.domain.services.asset_state import AssetStateService
from app.infrastructure.models.core import MiningAsset
from app.infrastructure.models.interactions import AssetNegotiation

async def accept_logic(negotiation_id, seller_id):
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        service = NegotiationService(session, repo)
        state_service = AssetStateService(repo)
        try:
            success, msg = await service.accept_offer(negotiation_id, state_service, str(seller_id), "SELLER")
            await session.commit()
            return success, msg
        except Exception as e:
            return False, str(e)

async def run_race_test():
    # تهيئة تلقائية للجداول لضمان وجودها بالعمود الجديد
    from app.infrastructure.database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # 1. إعداد أصل جديد مع الحقول المطلوبة
        asset = MiningAsset(title="أصل اختبار التسابق", status="APPROVED", seller_id=1001, category_id=1)
        session.add(asset)
        await session.commit()
        
        # 2. إنشاء مفاوضتين مع تحديد قيمة السعر لكي لا تفشل العملية
        n1 = AssetNegotiation(asset_id=asset.id, buyer_id=2002, status="OPEN", current_offer_price=1000.0)
        n2 = AssetNegotiation(asset_id=asset.id, buyer_id=3003, status="OPEN", current_offer_price=1500.0)
        session.add_all([n1, n2])
        await session.commit()
        
        print(f"⚡ إطلاق معركة التسابق على الأصل {asset.id}...")
        results = await asyncio.gather(accept_logic(n1.id, 1001), accept_logic(n2.id, 1001))
        
        successes = [r for r in results if r[0]]
        print(f"📊 النتائج: {len(successes)} عملية نجحت.")
        for i, res in enumerate(results):
            print(f"   العملية {i+1}: {'نجحت' if res[0] else 'فشلت'} - الرسالة: {res[1]}")

if __name__ == "__main__":
    asyncio.run(run_race_test())
