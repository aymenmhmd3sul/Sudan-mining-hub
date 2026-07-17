from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.security.auth import get_db, get_current_user
from app.security.policy import AuthorizationPolicy
from app.models.user import User
from app.models.finance import Invoice as InvoiceModel, Escrow as EscrowModel
from app.models.operations import FinancialTransaction
from app.schemas.invoice import InvoiceCreate, Invoice as InvoiceSchema
from app.schemas.escrow import EscrowCreate, Escrow as EscrowSchema
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
        invoice_id=req.invoice_id,
        amount=req.amount,
        payment_method=req.payment_method,
        reference_number=req.reference_number,
        status="PENDING"
    )
    db.add(tx)
    
    if req.invoice_id:
        invoice = db.query(InvoiceModel).filter(InvoiceModel.id == req.invoice_id).first()
        if invoice:
            invoice.status = "pending"
            
    db.commit()
    return {"message": "✅ تم رفع إشعار الدفع بنجاح، جاري مراجعته من قبل إدارة العمليات المالية."}

# ==========================================
# 2. محرك الفواتير (Invoice Endpoints)
# ==========================================

@router.post("/invoices", response_model=InvoiceSchema, status_code=status.HTTP_201_CREATED)
def create_invoice(req: InvoiceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """إنشاء فاتورة جديدة مرتبطة بصفقة تعدينية"""
    import uuid
    from decimal import Decimal
    invoice = InvoiceModel(
        opportunity_id=req.opportunity_id,
        buyer_id=current_user.id,
        seller_id=req.seller_id,
        invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
        status="draft",
        subtotal=Decimal(str(req.subtotal)),
        total_amount=Decimal(str(req.total_amount)),
        currency="USD"
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/invoices/my-invoices", response_model=list[InvoiceSchema])
def get_my_invoices(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """استعراض الفواتير التي يكون المستخدم مشترياً فيها"""
    return db.query(InvoiceModel).filter(InvoiceModel.buyer_id == current_user.id).all()

# ==========================================
# 3. محرك الضمان المالي (Escrow Endpoints)
# ==========================================

@router.post("/escrow/initiate", response_model=EscrowSchema, status_code=status.HTTP_201_CREATED)
def initiate_escrow(req: EscrowCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """إنشاء حساب ضمان مالي وربطه بفاتورة معينة لحماية الصفقة"""
    invoice = db.query(InvoiceModel).filter(InvoiceModel.id == req.invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="الفاتورة المحددة غير موجودة لتفعيل الضمان عليها.")
        
    escrow = EscrowModel(
        invoice_id=req.invoice_id,
        amount=invoice.total_amount,
        currency=invoice.currency,
        status="pending"
    )
    db.add(escrow)
    db.commit()
    db.refresh(escrow)
    return escrow

@router.post("/escrow/{escrow_id}/release")
def release_escrow(escrow_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """تأكيد الاستلام من قبل المشتري والإفراج عن الأموال"""
    escrow = db.query(EscrowModel).filter(EscrowModel.id == escrow_id).first()
    if not escrow:
        raise HTTPException(status_code=404, detail="حساب الضمان غير موجود.")
    
    if escrow.invoice.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="غير مصرح لك بالإفراج عن هذه الأموال، المشتري فقط من يملك الصلاحية.")
        
    escrow.status = "released"
    db.commit()
    return {"message": "✅ تم الإفراج عن الضمان المالي وتحويله لحساب البائع بنجاح."}

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

    if action_upper == "APPROVED":

        if tx.invoice_id:
            invoice = db.query(InvoiceModel).filter(
                InvoiceModel.id == tx.invoice_id
            ).first()

            if invoice:
                invoice.status = "PAID"

                escrow = db.query(EscrowModel).filter(
                    EscrowModel.invoice_id == invoice.id
                ).first()

                if escrow:
                    escrow.status = "funded"

    db.commit()

    return {
        "message": f"✅ تم تحديث المعاملة والفاتورة والضمان إلى: {tx.status}"
    }

