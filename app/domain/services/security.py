from typing import Optional, Tuple
from app.infrastructure.models.core import MiningAsset
from app.infrastructure.models.interactions import AssetNegotiation, AssetEvent

class SecurityGuard:
    # 1. مصفوفة الصلاحيات العامة حسب الدور
    ROLE_PERMISSIONS = {
        "CREATE_ASSET": ["SELLER", "ADMIN"],
        "EDIT_ASSET": ["SELLER", "ADMIN"],
        "DELETE_ASSET": ["ADMIN"],
        "TRANSITION_ASSET": ["SELLER", "ADMIN"],
        "CREATE_NEGOTIATION": ["BUYER", "ADMIN"],
        "CREATE_OFFER": ["BUYER", "ADMIN"],
        "RESPOND_OFFER": ["SELLER", "ADMIN"], # قبول أو رفض العرض من قبل البائع
        "ADMIN_ACTIONS": ["ADMIN"]
    }

    @staticmethod
    async def authorize_action(
        db_session,
        action: str,
        actor_id: str,
        actor_name: str,
        role: str,
        asset: Optional[MiningAsset] = None,
        negotiation: Optional[AssetNegotiation] = None,
        context_data: Optional[dict] = None
    ) -> Tuple[bool, str]:
        """
        المحرك المركزي لاتخاذ القرارات الأمنية وضمان تسجيلها في الـ asset_events.
        """
        actor_id_int = int(actor_id) if actor_id.isdigit() else 0
        is_authorized = True
        error_message = ""

        # ---- أولاً: فحص صلاحية الدور العامة ----
        allowed_roles = SecurityGuard.ROLE_PERMISSIONS.get(action, [])
        if role not in allowed_roles:
            is_authorized = False
            error_message = f"خطأ أمني: الدور [{role}] غير مصرح له بتنفيذ [{action}]."

        # ---- ثانياً: فحص قواعد الأعمال المتقدمة والأمن التشغيلي ----
        if is_authorized:
            
            # أ) محددات الأصول (Asset Rules)
            if action in ["EDIT_ASSET", "TRANSITION_ASSET"] and asset:
                if role != "ADMIN" and asset.seller_id != actor_id_int:
                    is_authorized = False
                    error_message = "خطأ أمني: لا تملك الصلاحية لتعديل أو نقل حالة هذا الأصل (ليست ملكك)."

            # ب) محددات بدء التفاوض (Negotiation Rules)
            elif action == "CREATE_NEGOTIATION" and asset:
                if asset.seller_id == actor_id_int:
                    is_authorized = False
                    error_message = "قاعدة عمل: لا يستطيع البائع التفاوض على أصله الخاص بصفة مشترٍ."
                
                # تطابقاً مع التسميات، APPROVED تعني أنه منشـور ومتاح في السوق حالياً
                elif asset.status != "APPROVED": 
                    is_authorized = False
                    error_message = f"قاعدة عمل: لا يمكن بدء تفاوض لأن الأصل ليس في حالة نشطة بالماركت بليس (الحالة الحالية: {asset.status})."

            # ج) محددات تقديم وقبول العروض الماليـة (Offer Rules)
            elif action == "CREATE_OFFER" and negotiation:
                if negotiation.status != "OPEN":
                    is_authorized = False
                    error_message = "قاعدة عمل: لا يمكن تقديم عرض مالي لأن جلسة التفاوض هذه مغلقة."
                
                if negotiation.asset.status in ["RESERVED", "SOLD", "ARCHIVED"]:
                    is_authorized = False
                    error_message = f"قاعدة عمل: تم حظر تقديم العرض، الأصل أصبح في حالة [{negotiation.asset.status}]."

            elif action == "RESPOND_OFFER" and negotiation:
                if role != "ADMIN" and negotiation.asset.seller_id != actor_id_int:
                    is_authorized = False
                    error_message = "خطأ أمني: أنت لست البائع المالك للأصل المرتبط بهذا العرض المالي."

        # ---- ثالثاً: التوثيق الإلزامي في جدول الـ Events (قفل الأمان الشامل) ----
        asset_id_for_event = asset.id if asset else (negotiation.asset_id if negotiation else None)
        
        event_record = AssetEvent(
            asset_id=asset_id_for_event or 0,
            event_type=f"AUTH_{action}_{'SUCCESS' if is_authorized else 'FAILURE'}",
            payload=f"{'تمت الموافقة الأمنية' if is_authorized else 'مرفوض: ' + error_message} | الفاعل: {actor_name} (ID: {actor_id})",
            actor=actor_name,
            actor_id=actor_id
        )
        db_session.add(event_record)
        # نقوم بعمل flush لحفظ الحدث الأمني دون إنهاء المعاملة الكلية
        await db_session.flush()

        return is_authorized, error_message
