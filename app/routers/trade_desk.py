from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security.auth import get_current_user
from app.core.db import get_db
from app.security.policy import AuthorizationPolicy
from app.models.user import User
from app.models.trade_desk import GlobalTradeDeskRequest

router = APIRouter(prefix="/trade-desk", tags=["Global Trade Desk"])

@router.post("/create-request/")
def create_trade_request(title: str, target_country: str, value: float, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """مسار محمي: يسمح فقط للمستوردين والشركات بإنشاء ملف صفقة دولية"""
    AuthorizationPolicy.can_use_trade_desk(current_user)
    
    new_request = GlobalTradeDeskRequest(
        client_id=current_user.id,
        title=title,
        target_country=target_country,
        estimated_value=value,
        status="OPEN"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {"message": "✅ تم إنشاء ملف الصفقة في قسم Global Trade Desk بنجاح!", "request_id": new_request.id}

@router.get("/view-bids/")
def view_global_bids(current_user: User = Depends(get_current_user)):
    """مسار محمي: يسمح فقط لمزودي الخدمات أو الإدارة برؤية وتقديم العروض"""
    AuthorizationPolicy.can_provide_global_services(current_user)
    return {"message": "مرحباً بك في لوحة العروض الدولية، تم التحقق من هويتك كـ Global Service Provider بنجاح!"}
