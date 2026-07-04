from typing import Tuple, List, Dict, Any, Optional
from datetime import datetime
from app.domain.services.security import SecurityGuard
from app.infrastructure.models.interactions import AssetEvent

class DocumentType:
    MINING_LICENSE = "MINING_LICENSE"          # رخصة التعدين
    OWNERSHIP_DEED = "OWNERSHIP_DEED"          # عقد الملكية / شهادة البحث
    TECHNICAL_REPORT = "TECHNICAL_REPORT"      # التقرير الفني الجيولوجي
    ENVIRONMENTAL_CLEARANCE = "ENVIRONMENTAL"  # خلو النزاع والبيئة

class DocumentStatus:
    UPLOADED = "UPLOADED"
    UNDER_REVIEW = "UNDER_REVIEW"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class DocumentService:
    def __init__(self, db_session, asset_repo):
        self.db = db_session
        self.asset_repo = asset_repo

    async def upload_asset_document(
        self, asset_id: int, doc_type: str, file_path: str, actor_id: str, role: str
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """ 1. رفع وثيقة جديدة للأصل وتعيين حالتها تلقائياً كـ UPLOADED """
        # التحقق من وجود الأصل
        asset = await self.asset_repo.get_by_id(asset_id)
        if not asset:
            return False, "الأصل التعديني المستهدف غير موجود.", None

        # التحقق من الصلاحية: البائع مالك الأصل هو الوحيد المخول بالرفع
        if role != "ADMIN" and asset.seller_id != int(actor_id):
            return False, "خطأ أمني: لا تملك صلاحية رفع مستندات لهذا الأصل.", None

        valid_types = [DocumentType.MINING_LICENSE, DocumentType.OWNERSHIP_DEED, DocumentType.TECHNICAL_REPORT, DocumentType.ENVIRONMENTAL_CLEARANCE]
        if doc_type not in valid_types:
            return False, f"نوع المستند [{doc_type}] غير معتمد في النظام.", None

        # محاكاة كيان المستند (Database Model Placeholder)
        # في بيئة الإنتاج سيتم الحفظ في جدول asset_documents
        doc_id = 100 + asset_id  # توليد معرف تجريبي
        document_snapshot = {
            "id": doc_id,
            "asset_id": asset_id,
            "doc_type": doc_type,
            "file_path": file_path,
            "status": DocumentStatus.UPLOADED,
            "created_at": datetime.utcnow().isoformat()
        }

        # تسجيل الحدث في سجل أحداث الأصل لعام 2026
        event = AssetEvent(
            asset_id=asset_id,
            event_type="DOCUMENT_UPLOADED",
            payload=f"تم رفع مستند جديد من النوع [{doc_type}] بنجاح.",
            actor=f"{role}_{actor_id}",
            actor_id=actor_id
        )
        self.db.add(event)
        await self.db.flush()

        return True, f"تم رفع المستند [{doc_type}] بنجاح وهو قيد الانتظار حالياً.", document_snapshot

    async def review_document(
        self, doc_snapshot: Dict[str, Any], inspector_id: str, role: str, to_status: str, rejection_reason: str = ""
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """ 2. مراجعة المستند من قبل المفتش الإداري وتغيير حالته (VERIFIED / REJECTED) """
        if role != "ADMIN":
            return False, "خطأ أمني: عذراً، مراجعة واعتماد المستندات صلاحية حصرية للمفتش الإداري.", doc_snapshot

        valid_review_statuses = [DocumentStatus.UNDER_REVIEW, DocumentStatus.VERIFIED, DocumentStatus.REJECTED, DocumentStatus.EXPIRED]
        if to_status not in valid_review_statuses:
            return False, f"الحالة المستهدفة [{to_status}] غير صحيحة لمسار المراجعة.", doc_snapshot

        # تحديث حالة السجل
        doc_snapshot["status"] = to_status
        doc_snapshot["updated_at"] = datetime.utcnow().isoformat()
        if to_status == DocumentStatus.REJECTED:
            doc_snapshot["rejection_reason"] = rejection_reason

        # توثيق المراجعة الإدارية في الـ Audit Trail
        event = AssetEvent(
            asset_id=doc_snapshot["asset_id"],
            event_type=f"DOCUMENT_{to_status}",
            payload=f"قام المفتش بتحديث حالة المستند رقم [{doc_snapshot['id']}] إلى [{to_status}]. السبب: {rejection_reason or 'اعتماد رسمي'}",
            actor=f"Admin_{inspector_id}",
            actor_id=inspector_id
        )
        self.db.add(event)
        await self.db.flush()

        return True, f"تم تحديث حالة المستند بنجاح إلى [{to_status}].", doc_snapshot

    async def check_asset_legal_readiness(self, verified_docs: List[str]) -> Tuple[bool, str]:
        """ 3. دالة استعلامية ذكية تفحص استيفاء الحد الأدنى من الأوراق القانونية الحرج """
        # الشرط الصارم: يجب وجود رخصة التعدين (MINING_LICENSE) وعقد الملكية (OWNERSHIP_DEED) معتمدين معاً
        has_license = DocumentType.MINING_LICENSE in verified_docs
        has_deed = DocumentType.OWNERSHIP_DEED in verified_docs

        if has_license and has_deed:
            return True, "الأصل مستوفٍ للحد الأدنى من الشروط القانونية وجاهز للنشر في السوق."
        
        missing = []
        if not has_license: missing.append("رخصة التعدين الرسمية")
        if not has_deed: missing.append("شهادة البحث أو عقد الملكية")
        
        return False, f"الأصل غير جاهز قانونياً. المستندات المفقودة أو غير المعتمدة: {', '.join(missing)}."
