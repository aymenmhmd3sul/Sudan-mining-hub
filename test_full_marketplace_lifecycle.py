import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.asset_state import AssetStateService
from app.domain.services.negotiation import NegotiationService

async def run_full_marketplace_scenario():
    print("🌟 === بدء محاكاة سيناريو دورة الحياة الكاملة للماركت بليس (MVP E2E) ===")
    asset_id = None

    # ----------------------------------------------------
    # المشهد الأول: البائع (Seller) ينشئ أصل تعديني جديد
    # ----------------------------------------------------
    print("\n[المشهد 1] 🏪 بائع (SELLER) يقوم بإدخال مربع تعديني جديد كمستند مسودة...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        
        current_seller = {"id": 5001, "username": "Seller_Ayman", "role": "SELLER"}
        
        asset_data = {
            "title": "مربع امتياز الذهب رقم 88 - بربر",
            "description": "عرق مرو غني جداً مع مؤشرات إنتاجية عالية الجودة",
            "category_id": 1,
            "seller_id": current_seller["id"],
            "status": "DRAFT"
        }
        # مطابقة الأعمدة الفعلية للجدول: state, region, latitude, longitude
        location_data = {
            "state": "ولاية نهر النيل", 
            "region": "بربر", 
            "latitude": 18.01,
            "longitude": 33.98
        }
        specs_list = [
            {"spec_key": "نوع الخام", "spec_value": "ذهب - عروق مرو (Quartz)"},
            {"spec_key": "المساحة التقريبية", "spec_value": "2 كيلومتر مربع"}
        ]
        
        new_asset = await repo.create_asset_with_details(asset_data, location_data, specs_list)
        await session.commit()
        asset_id = new_asset.id
        print(f"   ✅ تم حفظ الأصل بنجاح وجلب المعرف الرقمي للأصل: [{asset_id}]")

    # ----------------------------------------------------
    # المشهد الثاني: البائع يرسل الطلب للمراجعة والتدقيق
    # ----------------------------------------------------
    print(f"\n[المشهد 2] 🔄 البائع [{current_seller['username']}] يطلب مراجعة الأصل ونشره...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        state_service = AssetStateService(repo)
        
        success, message = await state_service.transition_status(
            asset_id=asset_id,
            to_state="PENDING_REVIEW",
            actor=current_seller["username"],
            actor_id=str(current_seller["id"]),
            reason="تم إدخال الإحداثيات الجغرافية والمستندات الفنية"
        )
        if success:
            print(f"   ✅ حالة الأصل الآن: PENDING_REVIEW | رسالة النظام: {message}")
            await session.commit()

    # ----------------------------------------------------
    # المشهد الثالث: المشرف (Admin) يعتمد الأصل ويقدح الـ Workflow
    # ----------------------------------------------------
    print(f"\n[المشهد 3] 👑 المشرف (ADMIN) يدخل لمراجعة طلبات النشر للأصل رقم [{asset_id}]...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        state_service = AssetStateService(repo)
        
        current_admin = {"id": 9009, "username": "Admin_Inspector", "role": "ADMIN"}
        
        success, message = await state_service.transition_status(
            asset_id=asset_id,
            to_state="APPROVED",
            actor=current_admin["username"],
            actor_id=str(current_admin["id"]),
            reason="المستندات مطابقة تماماً لشروط هيئة الأبحاث الجيولوجية"
        )
        if success:
            await session.commit()
            print(f"   ✅ تم الحفظ والالتزام بالمعاملة نهائياً من المشرف.")

    # ----------------------------------------------------
    # المشهد الرابع: مشتري (Buyer) يستعلم ويقدم عرض مالي
    # ----------------------------------------------------
    print(f"\n[المشهد 4] 💰 مشتري (BUYER) يستعلم عن المربعات النشطة ويقدم أول عرض تفاوضي...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        negotiation_service = NegotiationService(repo)
        
        current_buyer = {"id": 7007, "username": "Buyer_Investor", "role": "BUYER"}
        
        rich_asset = await repo.get_rich_asset_by_id(asset_id)
        print(f"   🔍 المشتري يرى الأصل: '{rich_asset.title}' | الحالة الحالية في السوق: [{rich_asset.status}]")
        
        print(f"   📥 جاري تقديم عرض مالي بقيمة 75,000$ من المستثمر...")
        success, message = await negotiation_service.submit_offer(
            asset_id=asset_id,
            buyer_id=current_buyer["id"],
            offer_price=75000.0
        )
        if success:
            print(f"   ✅ رد محرك التفاوض: {message}")
            await session.commit()

    # ----------------------------------------------------
    # التدقيق النهائي: فحص سجل التغيرات والمفاوضات المترابطة
    # ----------------------------------------------------
    print(f"\n🔍 [التدقيق الختامي للأمان] قراءة السجل التاريخي المتراكم للأصل رقم [{asset_id}]...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        final_asset = await repo.get_rich_asset_by_id(asset_id)
        
        print(f"📊 حالة الأصل النهائية المتأصلة في النظام: {final_asset.status}")
        print(f"📜 حركات الـ Audit Trail المسجلة في الـ History ({len(final_asset.status_history)} حركات):")
        for log in final_asset.status_history:
            print(f"   - من [{log.from_state}] ➔ إلى [{log.to_state}] | بواسطة: {log.actor} | السبب: {log.reason}")
            
        print(f"💬 سجل العروض المالية المربوطة والمفتوحة حالياً ({len(final_asset.negotiations)} عروض):")
        for offer in final_asset.negotiations:
            print(f"   - المشتري رقم: {offer.buyer_id} قدم عرضاً بمبلغ: {offer.current_offer_price}$ [حالة العرض: {offer.status}]")

    print("\n🎉 === انتهت محاكاة الدورة التشغيلية الكاملة للـ MVP بنجاح ساحق ومثالي! ===")

if __name__ == "__main__":
    asyncio.run(run_full_marketplace_scenario())
