from typing import Tuple, Optional, List, Dict, Any
from datetime import datetime
from app.infrastructure.repositories.asset import AssetRepository
from app.domain.services.security import SecurityGuard
from app.infrastructure.models.interactions import AssetNegotiation, AssetEvent

class NegotiationStatus:
    OPEN = "OPEN"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"

class OfferStatus:
    CREATED = "CREATED"
    COUNTERED = "COUNTERED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class NegotiationService:
    def __init__(self, db_session, asset_repo: AssetRepository):
        self.db = db_session
        self.asset_repo = asset_repo

    # ==========================================
    # PHASE 1 & 2: LIFECYCLES (المراحل السابقة)
    # ==========================================

    async def start_negotiation(self, asset_id: int, buyer_id: str, role: str) -> Tuple[bool, str, Optional[AssetNegotiation]]:
        asset = await self.asset_repo.get_by_id(asset_id)
        if not asset: return False, "الأصل التعديني المستهدف غير موجود.", None
        allowed, msg = await SecurityGuard.authorize_action(db_session=self.db, action="CREATE_NEGOTIATION", actor_id=buyer_id, actor_name=f"Buyer_{buyer_id}", role=role, asset=asset)
        if not allowed: return False, msg, None
        from sqlalchemy import select
        stmt = select(AssetNegotiation).where(AssetNegotiation.asset_id == asset_id, AssetNegotiation.buyer_id == int(buyer_id), AssetNegotiation.status == NegotiationStatus.OPEN)
        result = await self.db.execute(stmt)
        if result.scalar_one_or_none(): return False, "لديك بالفعل جلسة تفاوض مفتوحة ونشطة لهذا الأصل.", None
        new_negotiation = AssetNegotiation(asset_id=asset_id, buyer_id=int(buyer_id), current_offer_price=0.0, status=NegotiationStatus.OPEN)
        self.db.add(new_negotiation)
        await self.db.flush()
        return True, "تم فتح جلسة التفاوض بنجاح ودخول مرحلة النقاش.", new_negotiation

    async def close_negotiation(self, negotiation_id: int, close_status: str) -> Tuple[bool, str]:
        from sqlalchemy import select
        stmt = select(AssetNegotiation).where(AssetNegotiation.id == negotiation_id)
        res = await self.db.execute(stmt)
        negotiation = res.scalar_one_or_none()
        if not negotiation: return False, "جلسة التفاوض المستهدفة غير موجودة."
        if negotiation.status != NegotiationStatus.OPEN: return False, f"فشل الإغلاق: الجلسة ليست مفتوحة حالياً ({negotiation.status})."
        negotiation.status = close_status
        negotiation.updated_at = datetime.utcnow()
        await self.db.flush()
        return True, f"تم إغلاق جلسة التفاوض بنجاح كـ [{close_status}]."

    async def create_offer(self, negotiation_id: int, amount: float, actor_id: str, role: str) -> Tuple[bool, str]:
        from sqlalchemy import select
        stmt = select(AssetNegotiation).where(AssetNegotiation.id == negotiation_id)
        res = await self.db.execute(stmt)
        negotiation = res.scalar_one_or_none()
        if not negotiation or negotiation.status != NegotiationStatus.OPEN: return False, "فشل تقديم العرض: جلسة التفاوض مغلقة أو غير موجودة."
        allowed, msg = await SecurityGuard.authorize_action(db_session=self.db, action="CREATE_OFFER", actor_id=actor_id, actor_name=f"Buyer_{actor_id}", role=role, negotiation=negotiation)
        if not allowed: return False, msg
        negotiation.current_offer_price = amount
        negotiation.updated_at = datetime.utcnow()
        event = AssetEvent(asset_id=negotiation.asset_id, event_type="OFFER_CREATED", payload=f"تقديم عرض مالي جديد بقيمة {amount}$ من المشتري {actor_id}", actor=f"Buyer_{actor_id}", actor_id=actor_id)
        self.db.add(event)
        await self.db.flush()
        return True, f"تم تسجيل عرضك المالي بمبلغ {amount}$ بنجاح."

    async def accept_offer(self, negotiation_id: int, asset_state_service, actor_id: str, role: str) -> Tuple[bool, str]:
        from sqlalchemy import select
        stmt = select(AssetNegotiation).where(AssetNegotiation.id == negotiation_id)
        res = await self.db.execute(stmt)
        negotiation = res.scalar_one_or_none()
        if not negotiation or negotiation.status != NegotiationStatus.OPEN: return False, "جلسة التفاوض غير موجودة أو مغلقة مسبقاً."
        allowed, msg = await SecurityGuard.authorize_action(db_session=self.db, action="RESPOND_OFFER", actor_id=actor_id, actor_name=f"Seller_{actor_id}", role=role, negotiation=negotiation)
        if not allowed: return False, msg
        success, state_msg = await asset_state_service.transition_status(asset_id=negotiation.asset_id, to_state="RESERVED", actor=f"Seller_{actor_id}", actor_id=actor_id, role=role, reason=f"تم قبول العرض المالي في التفاوض رقم {negotiation_id}")
        if not success: return False, f"فشل حجز الأصل: {state_msg}"
        negotiation.status = NegotiationStatus.ACCEPTED
        negotiation.updated_at = datetime.utcnow()
        stmt_others = select(AssetNegotiation).where(AssetNegotiation.asset_id == negotiation.asset_id, AssetNegotiation.id != negotiation_id, AssetNegotiation.status == NegotiationStatus.OPEN)
        res_others = await self.db.execute(stmt_others)
        for other_neg in res_others.scalars().all():
            other_neg.status = NegotiationStatus.CLOSED
            other_neg.updated_at = datetime.utcnow()
            self.db.add(AssetEvent(asset_id=negotiation.asset_id, event_type="NEGOTIATION_AUTO_CLOSED", payload=f"إغلاق تلقائي للتفاوض رقم {other_neg.id} بسبب قبول عرض منافس.", actor="System_Workflow", actor_id="0"))
        await self.db.flush()
        return True, "🎉 تم قبول العرض بنجاح، وتحويل الأصل إلى محجوز [RESERVED]، وإغلاق كافة المفاوضات المنافسة تلقائياً."

    # ==========================================
    # PHASE 3: MESSAGING ENGINE (المرحلة 3)
    # ==========================================

    async def send_message(
        self, negotiation_id: int, sender_id: str, role: str, text: str
    ) -> Tuple[bool, str]:
        """ 1. إرسال رسالة ككيان مستقل محمي ضد التلاعب والـ Admin Alteration """
        from sqlalchemy import select
        stmt = select(AssetNegotiation).where(AssetNegotiation.id == negotiation_id)
        res = await self.db.execute(stmt)
        negotiation = res.scalar_one_or_none()

        if not negotiation:
            return False, "جلسة التفاوض غير موجودة."

        # 4. close_chat(): فحص حالة شات الجلسة (مغلق حكماً إذا لم تكن الحالة OPEN)
        if negotiation.status != NegotiationStatus.OPEN:
            return False, f"المحادثة مغلقة حكماً نظراً لأن حالة التفاوض الحالية هي [{negotiation.status}]."

        # التحقق من أن المرسل طرف في التفاوض (المشتري، البائع مالك الأصل، أو المشرف للرقابة فقط)
        sender_id_int = int(sender_id) if sender_id.isdigit() else 0
        is_buyer = (negotiation.buyer_id == sender_id_int)
        is_seller = (negotiation.asset.seller_id == sender_id_int)
        is_admin = (role == "ADMIN")

        if not (is_buyer or is_seller or is_admin):
            return False, "خطأ أمني: لست طرفاً مصرحاً له بالمراسلة في هذه الجلسة."

        # توثيق الرسالة ككيان حدث توثيقي غير قابل للتعديل أو الحذف
        msg_payload = f"MESS_FROM_{role}_ID_{sender_id}: {text}"
        event = AssetEvent(
            asset_id=negotiation.asset_id,
            event_type="NEGOTIATION_MESSAGE_SENT",
            payload=msg_payload,
            actor=f"{role}_{sender_id}",
            actor_id=sender_id
        )
        self.db.add(event)
        await self.db.flush()
        return True, "تم إرسال وتوثيق الرسالة بنجاح في السجل القانوني للجلسة."

    async def list_messages(
        self, negotiation_id: int, user_id: str, role: str, limit: int = 10, offset: int = 0
    ) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """ 2. عرض رسائل المحادثة مرتبة زمنياً مع دعم الـ Pagination صيانة للأداء """
        from sqlalchemy import select
        stmt = select(AssetNegotiation).where(AssetNegotiation.id == negotiation_id)
        res = await self.db.execute(stmt)
        negotiation = res.scalar_one_or_none()

        if not negotiation:
            return False, "جلسة التفاوض غير موجودة.", []

        # التحقق من صلاحية الوصول للـ List
        u_id_int = int(user_id) if user_id.isdigit() else 0
        if role != "ADMIN" and negotiation.buyer_id != u_id_int and negotiation.asset.seller_id != u_id_int:
            return False, "خطأ أمني: غير مصرح لك بالاطلاع على محادثات هذه الجلسة.", []

        # جلب الرسائل المخزنة في الـ Events المرتبطة بهذه الجلسة (مصفاة ومرتبة زمنياً)
        # في المعمارية الكاملة ستجلب من جدول مستقل، هنا نحاكيها بـ Pagination حقيقي
        stmt_events = select(AssetEvent).where(
            AssetEvent.asset_id == negotiation.asset_id,
            AssetEvent.event_type == "NEGOTIATION_MESSAGE_SENT"
        ).order_by(AssetEvent.created_at.asc()).limit(limit).offset(offset)
        
        events_res = await self.db.execute(stmt_events)
        messages_records = events_res.scalars().all()

        formatted_messages = []
        for record in messages_records:
            formatted_messages.append({
                "id": record.id,
                "sender_actor": record.actor,
                "content": record.payload,
                "timestamp": record.created_at.isoformat() if record.created_at else str(datetime.utcnow()),
                "is_read_placeholder": True # 3. mark_as_read() المخطط لها مستقبلاً للهواتف
            })

        return True, f"تم جلب الرسائل بنجاح (Limit: {limit}, Offset: {offset})", formatted_messages
