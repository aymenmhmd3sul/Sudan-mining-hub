from typing import List, Dict, Any, Tuple
from app.domain.services.document import DocumentStatus, DocumentType

class VerificationResult:
    """ كيان منظم يحمل تقرير الجاهزية الشامل لأصل التعدين قبل اعتماده """
    def __init__(self):
        self.ready_for_approval: bool = True
        self.missing_documents: List[str] = []
        self.invalid_documents: List[str] = []
        self.blocking_reasons: List[str] = []
        self.warnings: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ready_for_approval": self.ready_for_approval,
            "missing_documents": self.missing_documents,
            "invalid_documents": self.invalid_documents,
            "blocking_reasons": self.blocking_reasons,
            "warnings": self.warnings
        }

class VerificationService:
    def __init__(self, document_service, asset_repo):
        self.document_service = document_service
        self.asset_repo = asset_repo

    async def generate_readiness_report(
        self, asset_id: int, verified_docs_snapshots: List[Dict[str, Any]]
    ) -> VerificationResult:
        """
        فحص الأصول بناءً على المجموعات الأربع: المستندات، البيانات، قواعد العمل، والامتثال.
        """
        result = VerificationResult()
        
        # جلب بيانات الأصل من المستودع للتحقق من بياناته الأساسية
        asset = await self.asset_repo.get_by_id(asset_id)
        if not asset:
            result.ready_for_approval = False
            result.blocking_reasons.append("الأصل التعديني غير موجود في النظام كلياً.")
            return result

        # -------------------------------------------------------------
        # 1. Document Rules (قواعد المستندات السيادية)
        # -------------------------------------------------------------
        uploaded_types = {doc["doc_type"]: doc["status"] for doc in verified_docs_snapshots}
        
        # المستندات الإلزامية المطلوبة قانونياً لمربعات الذهب والمعادن في السودان لعام 2026
        mandatory_docs = [DocumentType.MINING_LICENSE, DocumentType.OWNERSHIP_DEED]
        
        for doc_type in mandatory_docs:
            if doc_type not in uploaded_types:
                result.missing_documents.append(doc_type)
                result.ready_for_approval = False
                result.blocking_reasons.append(f"غياب المستند الإلزامي السيادي: [{doc_type}].")
            elif uploaded_types[doc_type] != DocumentStatus.VERIFIED:
                result.invalid_documents.append(doc_type)
                result.ready_for_approval = False
                result.blocking_reasons.append(f"المستند [{doc_type}] موجود ولكنه ليس في حالة VERIFIED (الحالة الحالية: {uploaded_types[doc_type]}).")

        # -------------------------------------------------------------
        # 2. Asset Rules (اكتمال هيكل البيانات)
        # -------------------------------------------------------------
        if not asset.title or len(asset.title.strip()) < 5:
            result.ready_for_approval = False
            result.blocking_reasons.append("عنوان الأصل ناقص أو قصير جداً ولا يفي بالمتطلبات الاستثمارية.")
            
        # فحص الموقع الجغرافي المربوط عبر تفاصيل الأصل
        if not hasattr(asset, 'locations') or not asset.locations:
            result.ready_for_approval = False
            result.blocking_reasons.append("الموقع الجغرافي والولاية لم يتم تحديدهم للأصل.")

        # -------------------------------------------------------------
        # 3. Business & Compliance Rules (بلاغات، تعليق، أو مستندات اختيارية غائبة)
        # -------------------------------------------------------------
        # التقرير الفني الجيولوجي (خيار مفضل للمستثمرين، غيابه يطلق Warning ولا يمنع البيع)
        if DocumentType.TECHNICAL_REPORT not in uploaded_types:
            result.warnings.append("التقرير الفني الجيولوجي لخامات المربع غائب؛ يفضل رفعه لتعزيز جاذبية الاستثمار.")

        return result

    async def verify_and_activate_asset(
        self, asset_id: int, docs_snapshots: List[Dict[str, Any]], asset_state_service, actor_id: str, role: str
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        المايسترو القانوني: يفحص التقرير أولاً، وإذا نجح، يستدعي آلة الحالات للتنفيذ الحتمي.
        """
        # توليد تقرير الجاهزية
        report = await self.generate_readiness_report(asset_id, docs_snapshots)
        
        if not report.ready_for_approval:
            return False, "فشل الاعتماد: الأصل غير مستوفٍ للشروط القانونية والفنية.", report.to_dict()

        # إذا نجح الفحص كلياً، نمرر الأمر لآلة الحالات للتنفيذ فقط
        success, state_msg = await asset_state_service.transition_status(
            asset_id=asset_id,
            to_state="APPROVED",
            actor=f"Admin_Inspector_{actor_id}",
            actor_id=actor_id,
            role=role,
            reason="اعتماد رسمي بعد اجتياز فحص تقرير الجاهزية والامتثال القانوني الشامل."
        )

        if not success:
            report.ready_for_approval = False
            report.blocking_reasons.append(f"فشل انتقال الحالة في لولب النظام: {state_msg}")
            return False, "فشل انتقال الحالة الهيكلية للأصل.", report.to_dict()

        return True, "🎉 تم اعتماد الأصل ونشره بنجاح بعد اجتياز كافة الفحوصات القانونية والامتثال المعماري الموحد!", report.to_dict()
