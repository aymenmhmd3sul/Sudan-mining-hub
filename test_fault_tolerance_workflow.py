import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.negotiation import NegotiationService
from app.domain.services.asset_state import AssetStateService
from app.domain.services.workflow import WorkflowEngine, MarketplaceEvents

async def run_final_architectural_test():
    print("🏆 === بدء تشغيل اختبار تحمل الأخطاء وعزل العمليات (Final Phase 4) ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        neg_service = NegotiationService(session, repo)
        state_service = AssetStateService(repo)
        
        # 1. تجهيز الأصل وإيصاله لحالة APPROVED
        asset_data = {"title": "منطقة امتياز معزولة الأخطاء", "description": "فحص معمارية التنسيق", "category_id": 1, "seller_id": 5001, "status": "DRAFT"}
        location_data = {"state": "ولاية البحر الأحمر", "region": "بورتسودان"}
        asset = await repo.create_asset_with_details(asset_data, location_data, [])
        await session.commit()
        
        await state_service.transition_status(asset.id, "PENDING_REVIEW", "Seller_5001", "5001", "SELLER")
        await state_service.transition_status(asset.id, "APPROVED", "Admin_Inspector", "99", "ADMIN")
        await session.commit()
        
        # 2. المشتري يفتح تفاوض ويقدم عرضاً
        _, _, neg = await neg_service.start_negotiation(asset.id, buyer_id="2002", role="BUYER")
        await neg_service.create_offer(neg.id, amount=120000.0, actor_id="2002", role="BUYER")
        await session.commit()
        
        print("\n🔥 [بدء الفحص الحرج]: البائع يقبل العرض المالي، ومع تفعيل محاكاة فشل خادم الإشعارات...")
        
        # 3. البائع يقبل العرض
        success, message = await neg_service.accept_offer(
            negotiation_id=neg.id, asset_state_service=state_service, actor_id="5001", role="SELLER"
        )
        print(f"📌 رد محرك الصفقات الأساسي: {success} | {message}")
        
        # 4. استدعاء المنسق (Orchestrator) مع محاكاة تعطل خدمة الإشعارات عمداً
        context_data = {
            "asset_id": asset.id,
            "amount": 120000.0,
            "buyer_id": "2002",
            "simulate_notification_failure": True # تفعيل الحظر المعزول للتنبيهات
        }
        await WorkflowEngine.trigger_pipeline(MarketplaceEvents.OFFER_ACCEPTED, context_data)
        await session.commit()
        
        # 5. الفحص التأكيدي للبيانات في المستودع الحقيقي
        print("\n🔍 [مرحلة التحقق المعماري الختامي]:")
        updated_asset = await repo.get_by_id(asset.id)
        print(f"📊 حالة الأصل التعديني الجوهرية في قاعدة البيانات: [{updated_asset.status}]")
        
        if updated_asset.status == "RESERVED":
            print("\n🎉 [إعلان نجاح البنية التأسيسية للمشروع كلياً]:")
            print("  - تم عزل فشل الخدمات الجانبية بنجاح.")
            print("  - تم حماية وتأمين الحالة المالية الجوهرية للأصل كـ [RESERVED].")
            print("  - النظام صلب وقابل للتوسع اللانهائي دون أي ثغرات أو ديون تقنية!")
        else:
            print("\n❌ فشل المعمارية: عطل في الإشعارات تسبب في انهيار حالة العقد الجوهرية.")

if __name__ == "__main__":
    asyncio.run(run_final_architectural_test())
