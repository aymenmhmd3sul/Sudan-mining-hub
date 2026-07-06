from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.security.auth import get_db, get_current_user
from app.security.policy import AuthorizationPolicy
from app.models.identity import User
from app.models.operations import FinancialTransaction
from pydantic import BaseModel

router = APIRouter(prefix="/payments", tags=["Financial & Subscriptions Engine"])

class PaymentSubmit(BaseModel):
    amount: float
    payment_method: str      # e.g., "Bank_of_Khartoum", "Cash", "International"
    reference_number: str    # رقم المعاملة أو الإشعار

class PaymentReview(BaseModel):
    transaction_id: int
    action: str              # APPROVED أو REJECTED

@router.post("/submit")
def submit_payment_proof(req: PaymentSubmit, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """رفع إشعار تحويل مالي لتفعيل اشتراك أو دفع عمولة صفقة"""
    existing = db.query(FinancialTransaction).filter(FinancialTransaction.reference_number == req.reference_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="رقم الإشعار هذا تم رفعه مسبقاً في النظام.")
        
    tx = FinancialTransaction(
        user_id=current_user.id,
        amount=req.amount,
        payment_method=req.payment_method,
        reference_number=req.reference_number,
        status="PENDING"
    )
    db.add(tx)
    db.commit()
    return {"message": "✅ تم رفع إشعار الدفع بنجاح، جاري مراجعته من قبل إدارة العمليات التمويلية."}

@router.get("/pending-reviews")
def list_pending_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """لوحة الإدارة: استعراض كافة الحوالات والمدفوعات المعلقة المترقبة للموافقة"""
    AuthorizationPolicy.can_manage_platform(current_user)
    txs = db.query(FinancialTransaction).filter(FinancialTransaction.status == "PENDING").all()
    return {"status": "success", "data": txs}

@router.post("/review")
def review_payment(req: PaymentReview, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """لوحة الإدارة: اعتماد أو رفض المدفوعات والحوالات بشكل فوري"""
    AuthorizationPolicy.can_manage_platform(current_user)
    
    tx = db.query(FinancialTransaction).filter(FinancialTransaction.id == req.transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="المعاملة المالية غير موجودة.")
        
    tx.status = req.action.upper()
    db.commit()
    return {"message": f"✅ تم تحديث حالة المعاملة بنجاح إلى: {tx.status}"}
