from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# 1. جدول الإعدادات المركزية للمنظومة بالكامل
class PlatformSetting(Base):
    __tablename__ = "platform_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

# 2. جدول المستخدمين (مضاف إليه أدوار منظومة التسوية الجديدة)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # الأدوار: ADMIN (المشرف)، IMPORTER (المستورد السوداني)، PROVIDER (مزود خدمة التسوية: بنك، صرافة، وكيل دولي)
    role = Column(String(50), default="IMPORTER") 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    invoices = relationship("InternationalInvoice", back_populates="client")
    bids = relationship("SettlementBid", back_populates="provider")

# 🚀 3. جدول الفواتير الدولية (Sudan Trade Settlement)
class InternationalInvoice(Base):
    __tablename__ = "international_invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id")) # المستورد السوداني
    
    invoice_title = Column(String(200), nullable=False) # مثال: شراء حفار كوماتسو أو قطع غيار مصانع
    business_sector = Column(String(100), default="MINING") # MINING, AGRICULTURE, LIVESTOCK, GENERAL
    
    amount = Column(Float, nullable=False) # قيمة الفاتورة الخارجية (مثلاً 120,000)
    currency = Column(String(20), default="USD") # العملة المطلوبة في الخارج (USD, CNY, AED)
    target_country = Column(String(100), nullable=False) # الدولة المستهدفة بالسداد (الصين، الإمارات، تركيا)
    
    invoice_file_url = Column(String(255), nullable=True) # رابط مستند الفاتورة للتحقق وضمان الجدية
    
    # حالة الفاتورة في السوق: 
    # OPEN (تستقبل عروض)، LOCKED (تم اختيار عرض وبدأت مراحل الضمان)، COMPLETED (أُغلقت بنجاح)
    market_status = Column(String(50), default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("User", back_populates="invoices")
    bids = relationship("SettlementBid", back_populates="invoice")
    escrow = relationship("InvoiceEscrow", uselist=False, back_populates="invoice")

# 🚀 4. جدول العروض التنافسية (Bidding System)
class SettlementBid(Base):
    __tablename__ = "settlement_bids"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("international_invoices.id"))
    provider_id = Column(Integer, ForeignKey("users.id")) # مزود الخدمة الذي قدم العرض
    
    commission_percentage = Column(Float, nullable=False) # نسبة العمولة المعروضة (مثال: 1.8%)
    delivery_days = Column(Integer, nullable=False) # الزمن المتوقع للتسوية بالأيام (مثال: 2)
    payment_method = Column(String(100)) # قنوات السداد المقترحة (مثال: بنك دبي الإسلامي، صرافة مرخصة)
    
    # حالة العرض: PENDING (معلق)، ACCEPTED (تم اختياره من العميل)، REJECTED (مرفوض)
    bid_status = Column(String(50), default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    invoice = relationship("InternationalInvoice", back_populates="bids")
    provider = relationship("User", back_populates="bids")

# 🚀 5. نظام مراحل الضمان الستة الموثوق (Invoice Escrow Engine)
class InvoiceEscrow(Base):
    __tablename__ = "invoice_escrows"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("international_invoices.id"), unique=True)
    accepted_bid_id = Column(Integer) # معرّف العرض الذي يجرى تنفيذه
    
    # الفئات الستة المحددة لتقليل المخاطر:
    # 1. CREATED (تم إنشاء الفاتورة وقبول الصفقة)
    # 2. ESCROW_DEPOSIT_CONFIRMED (تأكيد إيداع العميل المحلي أو الضمان المتبادل)
    # 3. PROOF_UPLOADED (مزود الخدمة دفع بالخارج ورفع إثبات الدفع والـ Swift)
    # 4. SUPPLIER_CONFIRMED (تأكيد المورد الخارجي في الصين/الإمارات استلام الأموال)
    # 5. CLOSED (إغلاق العملية بنجاح)
    # 6. DISPUTED (وجود نزاع تجاري تحت تحكيم إدارة المنصة)
    escrow_stage = Column(String(50), default="CREATED")
    
    proof_file_url = Column(String(255), nullable=True) # رابط إثبات السداد الخارجي المرفوع
    platform_fee_collected = Column(Float, default=0.0) # رسوم المنصة من تنظيم وتأمين هذه المناقصة الدولية
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    invoice = relationship("InternationalInvoice", back_populates="escrow")
