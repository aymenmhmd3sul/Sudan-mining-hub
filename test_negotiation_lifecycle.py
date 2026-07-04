import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService, NegotiationStatus
from app.domain.services.asset_state import AssetStateService

async def test_negotiation_suite():
    print("🧪 === بدء تشغيل حزمة اختبار دورة حياة التفاوض (Phase 1) ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        neg_service = NegotiationService(session, repo)
        state_service = AssetStateService(repo)
        
        # 0. تجهيز أصول تعدينية تجريبية للاختبار
        # أصل (A) سيتم ترقيته إلى APPROVED (منشور ومتاح في السوق)
        asset_a_data = {"title": "مربع امتياز منشور", "description": "متاح للتفاوض", "category_id": 1, "seller_id": 1001, "status": "DRAFT"}
        location_data = {"state": "ولاية نهر النيل", "region": "أبو حمد"}
        asset_a = await repo.create_asset_with_details(asset_a_data, location_data, [])
        
        # أصل (B) سيبقى DRAFT (غير منشور)
        asset_b_data = {"title": "مربع مسودة مخفي", "description": "غير منشور", "category_id": 1, "seller_id": 1001, "status": "DRAFT"}
        asset_b = await repo.create_asset_with_details(asset_b_data, location_data, [])
        
        await session.commit()
        
        # ترقية الأصل A إلى APPROVED ليمثل حالة PUBLISHED في السوق حالياً
        await state_service.transition_status(asset_a.id, "PENDING_REVIEW", "Seller_1001", "1001", "SELLER")
        await state_service.transition_status(asset_a.id, "APPROVED", "Admin_Inspector", "99", "ADMIN")
        await session.commit()
        
        print(f"📌 تم تجهيز الأصول: الأصل المنشور [{asset_a.id}] | الأصل المسودة [{asset_b.id}]")
        print("-" * 60)

        # -------------------------------------------------------------
        # ✅ الاختبار 1: إنشاء تفاوض صحيح على أصل منشور
        # -------------------------------------------------------------
        success_1, msg_1, neg_1 = await neg_service.start_negotiation(asset_id=asset_a.id, buyer_id="2002", role="BUYER")
        print(f"1. إنشاء تفاوض صحيح للمشتري 2002: {success_1} | الرد: {msg_1}")
        
        # ✅ الاختبار 2: رفض إنشاء تفاوض مكرر للمشتري نفسه
        success_2, msg_2, _ = await neg_service.start_negotiation(asset_id=asset_a.id, buyer_id="2002", role="BUYER")
        print(f"2. رفض التفاوض المكرر لنفس المشتري: {not success_2} | الرد: {msg_2}")
        
        # ✅ الاختبار 3: السماح لمشترٍ آخر بإنشاء تفاوض مستقل
        success_3, msg_3, neg_3 = await neg_service.start_negotiation(asset_id=asset_a.id, buyer_id="3003", role="BUYER")
        print(f"3. سماح تفاوض مستقل للمشتري 3003: {success_3} | الرد: {msg_3}")
        
        # ✅ الاختبار 4: منع التفاوض على أصل ليس PUBLISHED (أي ليس APPROVED)
        success_4, msg_4, _ = await neg_service.start_negotiation(asset_id=asset_b.id, buyer_id="2002", role="BUYER")
        print(f"4. منع التفاوض على أصل مسودة: {not success_4} | الرد: {msg_4}")
        
        # ✅ الاختبار 5: منع البائع من فتح تفاوض على أصله
        success_5, msg_5, _ = await neg_service.start_negotiation(asset_id=asset_a.id, buyer_id="1001", role="BUYER")
        print(f"5. منع البائع من شراء أصله: {not success_5} | الرد: {msg_5}")
        
        # ✅ الاختبار 6: منع الزائر (Visitor) من فتح تفاوض
        success_6, msg_6, _ = await neg_service.start_negotiation(asset_id=asset_a.id, buyer_id="4004", role="VISITOR")
        print(f"6. منع الزائر من فتح تفاوض: {not success_6} | الرد: {msg_6}")
        
        # ✅ الاختبار 7: إغلاق تفاوض مفتوح
        if neg_1:
            success_7, msg_7 = await neg_service.close_negotiation(negotiation_id=neg_1.id, close_status=NegotiationStatus.CLOSED)
            print(f"7. إغلاق التفاوض الأول المفتوح: {success_7} | الرد: {msg_7}")
            
            # ✅ الاختبار 8: منع إغلاق تفاوض مغلق مسبقًا
            success_8, msg_8 = await neg_service.close_negotiation(negotiation_id=neg_1.id, close_status=NegotiationStatus.CLOSED)
            print(f"8. منع إعادة إغلاق جلسة مغلقة: {not success_8} | الرد: {msg_8}")

        # ✅ الاختبار 9: محاولة إغلاق تفاوض غير موجود
        success_9, msg_9 = await neg_service.close_negotiation(negotiation_id=99999, close_status=NegotiationStatus.CLOSED)
        print(f"9. محاولة إغلاق جلسة وهمية (99999): {not success_9} | الرد: {msg_9}")

        print("-" * 60)
        print("🎉 اكتملت المحاكاة وفحص كافة شروط ميثاق العقد الوظيفي!")

if __name__ == "__main__":
    asyncio.run(test_negotiation_suite())
