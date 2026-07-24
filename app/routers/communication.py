from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.security.auth import get_current_user as require_any_user
from app.models.communication import Notification, DealEventLog

router = APIRouter(prefix="/communications", tags=["Communication & Audit Trail"])

# --- نماذج التحقق (Pydantic Schemas) ---
class NotificationResponse(BaseModel):
    id: int
    title: str
    content: str
    notification_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class EventLogResponse(BaseModel):
    id: int
    deal_id: int
    actor_id: int
    action: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- المسارات البرمجية (Endpoints) ---

@router.get("/notifications", response_model=List[NotificationResponse])
def get_my_notifications(unread_only: bool = False, db: Session = Depends(get_db), current_user: dict = Depends(require_any_user)):
    """جلب قائمة الإشعارات والتنبيهات الخاصة بالمستخدم الحالي."""
    user_id = current_user.get("id")
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
        
    return query.order_by(Notification.created_at.desc()).all()

@router.patch("/notifications/{notification_id}/read", status_code=status.HTTP_200_OK)
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_any_user)):
    """تحديث حالة الإشعار إلى 'مقروء' لتنظيف صندوق الوارد للمستخدم."""
    user_id = current_user.get("id")
    notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="الإشعار المستهدف غير موجود أو لا يخص هذا الحساب")
        
    notification.is_read = True
    db.commit()
    return {"status": "success", "message": "تم تعيين الإشعار كمقروء بنجاح"}

@router.get("/deals/{deal_id}/logs", response_model=List[EventLogResponse])
def get_deal_audit_trail(deal_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_any_user)):
    """استخراج سجل التدقيق التاريخي الكامل والأحداث المرتبطة بصفقة تعدينية معينة (Audit Trail)."""
    # تتاح القراءة لأطراف النظام الموثقين
    logs = db.query(DealEventLog).filter(DealEventLog.deal_id == deal_id).order_by(DealEventLog.created_at.asc()).all()
    return logs
