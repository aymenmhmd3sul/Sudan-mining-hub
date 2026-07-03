from app.domain.events.catalog import AssetEvent
from app.domain.services.workflow_service import AssetWorkflowService

class AssetStateService:
    @staticmethod
    def validate_transition(current_state: str, next_state: str, user_role: str):
        """التحقق من أن الانتقال مسموح به حسب الصلاحيات والدستور التقني."""
        # منطق التحقق (Logic) سيتم إضافته هنا
        return True

    @staticmethod
    def change_state(asset_id: int, new_state: str, user_id: str, reason: str = None):
        """تغيير الحالة وتوثيق العملية في سجل التاريخ."""
        # 1. التحديث في قاعدة البيانات
        # 2. التسجيل في asset_status_history
        # 3. إطلاق الحدث عبر الـ Workflow Service
        print(f"State Service: Asset {asset_id} moved to {new_state}")
        AssetWorkflowService.trigger(AssetEvent.PUBLISHED, asset_id) 
