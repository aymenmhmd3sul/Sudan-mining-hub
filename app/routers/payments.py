from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.security.auth import get_db, get_current_user
from app.security.policy import AuthorizationPolicy
from app.models.user import User
from app.models.finance import Invoice, EscrowTransaction, FinancialTransaction
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.schemas.escrow import EscrowCreate, EscrowResponse
from pydantic import BaseModel

router = APIRouter(prefix="/payments", tags=["Financial & Escrow Engine"])

class PaymentSubmit(BaseModel):
    amount: float
    payment_method: str       # e.g., "Bank_of_Khartoum", "Cash"
    reference_number: str     # رقم المعاملة أو الإشعار
    invoice_id: int | None = None

class PaymentReview(BaseModel):
    transaction_id: int
    action: str               # APPROVED أو REJECTED

# ==========================================
# 1. إشعارات التحويل وحوالات بنك الخرطوم
# ==========================================

@router.post("/submit", status_code=status.HTTP_201_CREATED)
def submit_payment_proof(req: PaymentSubmit, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """رفع إشعار تحويل مالي لتسوية فاتورة أو دفع عمولة"""
    existing = db.query(FinancialTransaction).filter(FinancialTransaction.reference_number == req.reference_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="رقم الإشعار هذا تم رفعه مسبقاً في النظام.")

    tx = FinancialTransaction(
        user_id=current_user.id,
        amount=req.amount,
        payment_method=req.payment_method,
        reference_number=req.reference_number,
        invoice_id=req.invoice_id,
        status="PENDING"
    )
    db.add(tx)
    
    if req.invoice_id:
        invoice = db.query(Invoice).filter(Invoice.id == req.invoice_id).first()
        if invoice:
            invoice.status = "PROCESSING"
            
    db.commit()
    return {"message": "✅ تم رفع إشعار الدفع بنجاح، جاري مراجعته من قبل إدارة العمليات المالية."}

# ==========================================
# 2. محرك الفواتير (Invoice Endpoints)
# ==========================================

@router.post("/invoices", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(req: InvoiceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """إنشاء فاتورة جديدة مرتبطة بصفقة تعدينية أو رسوم منصة"""
    invoice = Invoice(
        user_id=current_user.id,
        amount=req.amount,
        description=req.description,
        status="UNPAID"
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/invoices/my-invoices", response_model=list[InvoiceResponse])
def get_my_invoices(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """استعراض الفواتير الخاصة بالمستخدم الحالي"""
    return db.query(Invoice).filter(Invoice.user_id == current_user.id).all()

# ==========================================
# 3. محرك الضمان المالي (Escrow Endpoints)
# ==========================================

@router.post("/escrow/initiate", response_model=EscrowResponse, status_code=status.HTTP_201_CREATED)
def initiate_escrow(req: EscrowCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """إنشاء حساب ضمان مالي لحماية المشتري والبائع في صفقات المعادن"""
    escrow = EscrowTransaction(
        buyer_id=current_user.id,
        seller_id=req.seller_id,
        deal_id=req.deal_id,
        amount=req.amount,
        status="HOLD"
    )
    db.add(escrow)
    db.commit()
    db.refresh(escrow)
    return escrow

@router.post("/escrow/{escrow_id}/release")
def release_escrow(escrow_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """تأكيد الاستلام من قبل المشتري والإفراج عن الأموال للبائع"""
    escrow = db.query(EscrowTransaction).filter(EscrowTransaction.id == escrow_id).first()
    if not escrow:
        raise HTTPException(status_code=404, detail="حساب الضمان غير موجود.")
    if escrow.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="غير مصرح لك بالإفراج عن هذه الأموال.")
    if escrow.status != "HOLD":
        raise HTTPException(status_code=400, detail="حالة الحساب الحالي لا تسمح بالإفراج.")
        
    escrow.status = "RELEASED"
    db.commit()
    return {"message": "✅ تم الإفراج عن الأموال وتحويلها لحساب البائع بنجاح."}

# ==========================================
# 4. لوحة الإدارة والرقابة المالية (Admin Center)
# ==========================================

@router.get("/admin/pending-reviews")
def list_pending_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """لوحة الإدارة: استعراض كافة الحوالات والمدفوعات المعلقة للموافقة"""
    AuthorizationPolicy.can_manage_platform(current_user)
    txs = db.query(FinancialTransaction).filter(FinancialTransaction.status == "PENDING").all()
    return {"status": "success", "data": txs}

@router.post("/admin/review")
def review_payment(req: PaymentReview, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """لوحة الإدارة: اعتماد أو رفض المدفوعات والحوالات يدعمه تحديث الفواتير"""
    AuthorizationPolicy.can_manage_platform(current_user)

    tx = db.query(FinancialTransaction).filter(FinancialTransaction.id == req.transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="المعاملة المالية غير موجودة.")
    
    action_upper = req.action.upper()
    tx.status = action_upper
    
    if tx.invoice_id:
        invoice = db.query(Invoice).filter(Invoice.id == tx.invoice_id).first()
        if invoice:
            invoice.status = "PAID" if action_upper == "APPROVED" else "UNPAID"
            
    db.commit()
    return {"message": f"✅ تم تحديث حالة المعاملة بنجاح إلى: {tx.status}"}
