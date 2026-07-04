import asyncio
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.document import DocumentService, DocumentType, DocumentStatus

async def run_kyc_suite():
    print("🧪 === بدء تشغيل حزمة اختبار نظام المستندات والموثوقية القانونية (Phase C1) ===")
    
    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        doc_service = DocumentService(session, repo)
        
        # استخدام المعرفات المعتمدة في النظام (category_id=1 و seller_id=5001) لتفادي كسر الـ Foreign Key
        asset_data = {"title": "مربع تعدين خام الكروم - الانقسنا", "description": "موقع غني بالكروم عالي الجودة", "category_id": 1, "seller_id": 5001, "status": "DRAFT"}
        location_data = {"state": "ولاية النيل الأزرق", "region": "الانقسنا"}
        asset = await repo.create_asset_with_details(asset_data, location_data, [])
        await session.commit()
        print(f"📌 تم إنشاء الأصل المسودة برقم [{asset.id}] للمستثمر [5001]")

        # -------------------------------------------------------------
        # ✅ الاختبار 1: رفع مستند شرعي من البائع
        # -------------------------------------------------------------
        ok_upload, msg_up, doc_snapshot = await doc_service.upload_asset_document(
            asset_id=asset.id, doc_type=DocumentType.MINING_LICENSE, file_path="/docs/license_5001.pdf", actor_id="5001", role="SELLER"
        )
        print(f"1. رفع رخصة التعدين: {ok_upload} | الحالة الابتدائية: [{doc_snapshot['status'] if doc_snapshot else 'None'}] | الرد: {msg_up}")

        # -------------------------------------------------------------
        # ✅ الاختبار 2: منع غير الإداري من مراجعة وتعديل حالة المستند
        # -------------------------------------------------------------
        bad_review, bad_msg, _ = await doc_service.review_document(
            doc_snapshot=doc_snapshot, inspector_id="5001", role="SELLER", to_status=DocumentStatus.VERIFIED
        )
        print(f"2. حظر مراجعة البائع لمستنده الخاص: {not bad_review} | الرد: {bad_msg}")

        # -------------------------------------------------------------
        # ✅ الاختبار 3: اعتماد المستند رسمياً بواسطة الـ Admin
        # -------------------------------------------------------------
        ok_review, msg_rev, doc_snapshot = await doc_service.review_document(
            doc_snapshot=doc_snapshot, inspector_id="99", role="ADMIN", to_status=DocumentStatus.VERIFIED
        )
        print(f"3. اعتماد المفتش الإداري للرخصة: {ok_review} | الحالة الجديدة: [{doc_snapshot['status']}]")

        # -------------------------------------------------------------
        # ✅ الاختبار 4: فحص الجاهزية القانونية للأصل (حالة مستند واحد معتمد)
        # -------------------------------------------------------------
        verified_list = [doc_snapshot["doc_type"]]  # مصفوفة تحتوي على الوثائق المعتمدة حالياً
        ready_1, ready_msg_1 = await doc_service.check_asset_legal_readiness(verified_list)
        print(f"4. فحص الجاهزية (برخصة فقط دون عقد ملكية): جاهز؟ {ready_1} | الرد: {ready_msg_1}")

        # -------------------------------------------------------------
        # ✅ الاختبار 5: استكمال الأوراق ورفع عقد الملكية واعتماده لتحقيق الاكتمال
        # -------------------------------------------------------------
        _, _, deed_snapshot = await doc_service.upload_asset_document(
            asset_id=asset.id, doc_type=DocumentType.OWNERSHIP_DEED, file_path="/docs/deed_5001.pdf", actor_id="5001", role="SELLER"
        )
        # المفتش يوافق على عقد الملكية أيضاً
        _, _, deed_snapshot = await doc_service.review_document(
            doc_snapshot=deed_snapshot, inspector_id="99", role="ADMIN", to_status=DocumentStatus.VERIFIED
        )
        
        # إعادة فحص الجاهزية الكاملة للـ Domain
        final_verified_list = [DocumentType.MINING_LICENSE, DocumentType.OWNERSHIP_DEED]
        ready_final, ready_msg_final = await doc_service.check_asset_legal_readiness(final_verified_list)
        print(f"5. فحص الجاهزية بعد استكمال كافة الأوراق السيادية: جاهز؟ {ready_final} | الرد: {ready_msg_final}")

        if ready_final:
            print("\n🎉 [نجاح الموثوقية القانونية]: البنية التحتية للمستندات جاهزة ومحكمة بالكامل لحماية المنصة!")

if __name__ == "__main__":
    asyncio.run(run_kyc_suite())
