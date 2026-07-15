from typing import Tuple, Optional
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.workflow import WorkflowEngine
from app.domain.services.security import SecurityGuard

class AssetStateService:
    def __init__(self, asset_repo: AssetRepository):
        self.asset_repo = asset_repo

    ALLOWED_TRANSITIONS = {
        "DRAFT": ["PENDING_REVIEW"],
        "PENDING_REVIEW": ["APPROVED", "REJECTED"],
        "APPROVED": ["RESERVED", "SUSPENDED"],
        "RESERVED": ["SOLD", "APPROVED"],
        "SOLD": ["ARCHIVED"],
        "SUSPENDED": ["PENDING_REVIEW", "DRAFT"]
    }

    async def transition_status(self, asset_id: int, to_state: str, actor: str, actor_id: str, role: str, reason: Optional[str] = None) -> Tuple[bool, str]:
        asset = await self.asset_repo.get_by_id_for_update(asset_id)
        if not asset:
            return False, "الأصل التعديني المستهدف غير موجود."

        # الحارس الشرطي (State Validation Guard)
        if asset.status == "RESERVED" and to_state == "RESERVED":
            return False, "عذراً، الأصل تم حجزه بواسطة معاملة أخرى في هذه اللحظة."
        
        current_state = asset.status
        allowed_next_states = self.ALLOWED_TRANSITIONS.get(current_state, [])
        if to_state not in allowed_next_states:
            return False, f"انتقال غير مسموح به من حالة {current_state} إلى {to_state}"

        allowed, msg = await SecurityGuard.authorize_action(
            db_session=self.asset_repo.db,
            action="TRANSITION_ASSET",
            actor_id=actor_id,
            actor_name=actor,
            role=role,
            asset=asset
        )
        if not allowed:
            return False, msg

        from app.infrastructure.models.interactions import AssetStatusHistory
        history_record = AssetStatusHistory(
            asset_id=asset.id,
            from_state=current_state,
            to_state=to_state,
            actor=actor,
            actor_id=actor_id,
            reason=reason or "تغيير حالة عبر المنصة"
        )
        self.asset_repo.db.add(history_record)
        
        asset.status = to_state
        await self.asset_repo.db.flush()

        if to_state == "APPROVED":
            await WorkflowEngine.trigger_post_approval_pipeline(
                asset_id=asset.id,
                asset_title=asset.title,
                region=asset.locations[0].state if asset.locations else "غير محدد"
            )
        return True, f"تم نقل حالة الأصل بنجاح إلى {to_state}"
