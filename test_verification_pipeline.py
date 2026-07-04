import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.asset_state import AssetStateService
from app.domain.services.document import DocumentType, DocumentStatus
from app.domain.services.verification import VerificationService

async def run_verification_pipeline_suite():
    print("🧪 === بدء تشغيل حزمة اختبار محرك الامتثال وخدمة التحقق المستقلة (Phase C2) ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        state_service = AssetStateService(repo)
        
        # إنشاء خدمة التحقق
        verification_service = VerificationService(document_service=None, asset_repo=repo)

        # 1. إنشاء أصل مسودة تجريبي
        asset_data = {"title": "منجم ذهب جبل عامر الاستراتيجي", "description": "عروق كوارتز حاملة للذهب", "category_id": 1, "seller_id": 5001, "status": "DRAFT"}
        location_data = {"state": "ولاية شمال دارفور", "region": "جبل عامر"}
        asset = await repo.create_asset_with_details(asset_data, location_data, [])
        await session.commit()

        # -------------------------------------------------------------
        # ❌ السيناريو 1: محاولة الاعتماد بمستندات ناقصة وبيانات أولية
        # -------------------------------------------------------------
        print("\n📋 [فحص 1]: طلب تقرير جاهزية لأصل فارغ من الأوراق السيادية...")
        fake_docs_empty = []
        
        success_1, msg_1, report_1 = await verification_service.verify_and_activate_asset(
            asset_id=asset.id, docs_snapshots=fake_docs_empty, asset_state_service=state_service, actor_id="99", role="ADMIN"
        )
        print(f"- هل سُمح بالنشر؟ {success_1}")
        print(f"- الأوراق المفقودة الموثقة بالتقرير: {report_1['missing_documents']}")
        print(f"- أسباب المنع القانونية الشاملة: {report_1['blocking_reasons']}")

        # -------------------------------------------------------------
        # ✅ السيناريو 2: رفع المستندات واستدعاء محرك الامتثال للاعتماد الحتمي
        # -------------------------------------------------------------
        print("\n📋 [فحص 2]: استكمال الأوراق السيادية ومحاكاة دورة انتقالات الحالات الشرعية...")
        
        # تصحيح المسار المعماري: نقل الأصل إلى PENDING_REVIEW أولاً ليصبح مؤهلاً للاعتماد قانوناً
        await state_service.transition_status(
            asset_id=asset.id, to_state="PENDING_REVIEW", actor="Seller_5001", actor_id="5001", role="SELLER", reason="طلب نشر المربع"
        )
        await session.commit()
        
        completed_docs_snapshots = [
            {"doc_type": DocumentType.MINING_LICENSE, "status": DocumentStatus.VERIFIED, "id": 101},
            {"doc_type": DocumentType.OWNERSHIP_DEED, "status": DocumentStatus.VERIFIED, "id": 102}
        ]

        success_2, msg_2, report_2 = await verification_service.verify_and_activate_asset(
            asset_id=asset.id, docs_snapshots=completed_docs_snapshots, asset_state_service=state_service, actor_id="99", role="ADMIN"
        )
        await session.commit()

        print(f"- هل سُمح بالنشر الآن؟ {success_2}")
        print(f"- التحذيرات غير المانعة بالتقرير (Warnings): {report_2['warnings']}")
        print(f"- الرد النهائي للمحرك المنسق: {msg_2}")
        
        # التأكد من حالة الأصل في قاعدة البيانات
        updated_asset = await repo.get_by_id(asset.id)
        print(f"📊 حالة الأصل النهائية في المستودع: [{updated_asset.status}]")

        if success_2 and updated_asset.status == "APPROVED":
            print("\n🎉 [انتصار معماري تلو الآخر]: تم فصل المسؤوليات بنجاح، وخرج تقرير الجاهزية لخدمة المستثمرين ولوحة التحكم!")

if __name__ == "__main__":
    asyncio.run(run_verification_pipeline_suite())
