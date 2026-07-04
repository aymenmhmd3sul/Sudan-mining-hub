import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.asset_state import AssetStateService

async def test_asset_lifecycle():
    print("🚦 بدء اختبار الـ State Machine على الأصل رقم 1...")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        state_service = AssetStateService(repo)
        
        # --- الاختبار الأول: محاولة اختراق غير قانونية للحالات ---
        print("\n❌ محاولة نقل الحالة بشكل غير قانوني (DRAFT -> APPROVED)...")
        success, message = await state_service.transition_status(
            asset_id=1, to_state="APPROVED", actor="Seller_User", actor_id="1001", reason="محاولة نشر مباشرة"
        )
        print(f"   النتيجة المتوقعة (فشل): {message if not success else '⚠️ نجح بشكل خاطئ!'}")
        
        # --- الاختبار الثاني: الانتقال القانوني الأول (تقديم للمراجعة) ---
        print("\n🔄 محاولة نقل الحالة بشكل قانوني (DRAFT -> PENDING_REVIEW)...")
        success, message = await state_service.transition_status(
            asset_id=1, to_state="PENDING_REVIEW", actor="Seller_User", actor_id="1001", reason="يرجى مراجعة المربع ونشره"
        )
        if success:
            print(f"   ✅ نجاح: {message}")
            
        # --- الاختبار الثالث: الانتقال القانوني الثاني (اعتماد المشرف) ---
        print("\n👑 محاولة موافقة المشرف ونشر الأصل (PENDING_REVIEW -> APPROVED)...")
        success, message = await state_service.transition_status(
            asset_id=1, to_state="APPROVED", actor="Admin_Inspector", actor_id="9009", reason="المستندات سليمة والمربع مطابق للمواصفات"
        )
        if success:
            print(f"   ✅ نجاح: {message}")
            
        # حفظ كل التغييرات وسجلات التاريخ نهائياً في هذه المعاملة
        await session.commit()
        print("\n💾 تم حفظ دورتي الحالات وسجلات التاريخ بنجاح في dev.db.")

    # --- الاختبار العكسي: قراءة السجل التاريخي الشامل (Audit Trail) ---
    print("\n🔍 جاري التحقق من سجل التغيرات التاريخي للأصل...")
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        rich_asset = await repo.get_rich_asset_by_id(1)
        
        if rich_asset:
            print(f"📋 الحالة الحالية للأصل في قاعدة البيانات: {rich_asset.status}")
            print(f"📜 تاريخ التنقلات المكتشف في الجدول الملحق ({len(rich_asset.status_history)} حركات):")
            for record in rich_asset.status_history:
                print(f"   - من [{record.from_state}] إلى [{record.to_state}] | بواسطة: {record.actor} (ID: {record.actor_id}) | السبب: {record.reason}")
        else:
            print("❌ فشل جلب الأصل.")

if __name__ == "__main__":
    asyncio.run(test_asset_lifecycle())
