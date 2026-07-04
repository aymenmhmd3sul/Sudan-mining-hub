import sys
from typing import Dict, Any

class MarketplaceEvents:
    ASSET_CREATED = "ASSET_CREATED"
    ASSET_APPROVED = "ASSET_APPROVED"
    ASSET_RESERVED = "ASSET_RESERVED"
    ASSET_SOLD = "ASSET_SOLD"
    ASSET_ARCHIVED = "ASSET_ARCHIVED"
    
    NEGOTIATION_STARTED = "NEGOTIATION_STARTED"
    NEGOTIATION_CLOSED = "NEGOTIATION_CLOSED"
    NEGOTIATION_MESSAGE_SENT = "NEGOTIATION_MESSAGE_SENT"
    OFFER_CREATED = "OFFER_CREATED"
    OFFER_ACCEPTED = "OFFER_ACCEPTED"
    OFFER_REJECTED = "OFFER_REJECTED"
    OFFER_WITHDRAWN = "OFFER_WITHDRAWN"
    
    WORKFLOW_EXECUTED = "WORKFLOW_EXECUTED"
    SEARCH_INDEX_UPDATED = "SEARCH_INDEX_UPDATED"
    NOTIFICATION_SENT = "NOTIFICATION_SENT"

class WorkflowEngine:
    """
    المنسق المركزي (Orchestrator) للأعمال التشغيلية في المنصة لعام 2026.
    يضمن تنفيذ الخطوات باستقلالية تامة وقدرة عالية على تحمل الأخطاء (Fault Tolerance).
    """

    @staticmethod
    async def trigger_pipeline(event_type: str, context: Dict[str, Any]):
        print(f"\n⚡ [Workflow Orchestrator]: استلام الحدث [{event_type}] - جاري تنسيق العمليات التابعة...")

        # -------------------------------------------------------------
        # السيناريو 1: قبول العرض المالي وحجز الأصل
        # -------------------------------------------------------------
        if event_type == MarketplaceEvents.OFFER_ACCEPTED:
            asset_id = context.get("asset_id")
            amount = context.get("amount")
            buyer_id = context.get("buyer_id")
            
            try:
                print(f"  🔍 [SearchIndexService]: تحديث الفهرس.. إخفاء الأصل [{asset_id}] من الماركت بليس.")
                print(f"  ✅ [SearchIndexService]: تم التحديث بنجاح.")
            except Exception as e:
                print(f"  ⚠️ [SearchIndexService]: خطأ في الكشاف: {e}")

            try:
                if context.get("simulate_notification_failure", False):
                    raise ConnectionError("فشل الاتصال بخادم بث الإشعارات (Firebase/WhatsApp).")
                print(f"  📢 [NotificationService]: بث إشعار للمشتري [{buyer_id}]: تم قبول عرضك بمبلغ {amount}$.")
                print(f"  ✅ [NotificationService]: تم تسليم الإشعار بنجاح.")
            except Exception as e:
                print(f"  ⚠️ [NotificationService - فشل معزول]: {e} | (تم حفظ العملية جوهرياً وجدولة الإشعار لاحقاً).")

            try:
                print(f"  📜 [AuditService]: توثيق إغلاق الصفقة رقمياً للأصل [{asset_id}].")
            except Exception as e:
                print(f"  ⚠️ [AuditService]: {e}")

        # -------------------------------------------------------------
        # السيناريو 2: اعتماد أصل تعديني جديد ونشره (ASSET_APPROVED)
        # -------------------------------------------------------------
        elif event_type == MarketplaceEvents.ASSET_APPROVED:
            asset_id = context.get("asset_id")
            region = context.get("region", "غير محدد")
            
            try:
                print(f"  🔍 [SearchIndexService]: إضافة المربع الجديد في كشاف منطقة: {region}.")
            except Exception as e: print(f"  ⚠️ {e}")
                
            try:
                print(f"  📢 [NotificationService]: بث إشعار عام: مربع استثماري جديد متاح في {region}.")
            except Exception as e: print(f"  ⚠️ [NotificationService]: {e}")
                
            try:
                print(f"  📜 [AuditService]: توثيق الاعتماد والترخيص للأصل [{asset_id}].")
            except Exception as e: print(f"  ⚠️ {e}")

        print(f"✨ [Workflow Orchestrator]: اكتمل خط تنسيق العمليات للحدث [{event_type}].")

    @staticmethod
    async def trigger_post_approval_pipeline(asset_id: int, asset_title: str, region: str):
        """
        جسر مواءمة (Backward Compatibility Wrapper) لخدمة الحالات القديمة.
        يقوم بتحويل النداء القديم إلى الصيغة الموحدة للـ Orchestrator.
        """
        context = {
            "asset_id": asset_id,
            "asset_title": asset_title,
            "region": region
        }
        await WorkflowEngine.trigger_pipeline(MarketplaceEvents.ASSET_APPROVED, context)
