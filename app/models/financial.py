from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

# 1. جدول وسائل الدفع الديناميكية (يتحكم فيها المشرف بالكامل)
class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    
    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(100), nullable=False) # مثل: بنكك، أوكاش، USDT
    name_en = Column(String(100), nullable=False)
    type = Column(String(50), default="local") # local أو international
    account_details = Column(Text, nullable=False) # رقم الحساب، اسم المستفيد، أو عنوان المحفظة
    is_active = Column(Boolean, default=True) # تشغيل/إيقاف الوسيلة
    display_order = Column(Integer, default=0) # ترتيب الظهور في الشاشة
    target_country = Column(String(50), default="ALL") # تقييد الوسيلة لدولة معينة أو للجميع

# 2. جدول المحافظ الرقمية للتجار (Wallet)
class Wallet(Base):
    __tablename__ = 'wallets'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    balance = Column(Float, default=0.0) # الرصيد الحالي المتاح للاستخدام الفوري
    frozen_balance = Column(Float, default=0.0) # الرصيد المحجوز معلقاً لصفقة أو إعلان قيد المراجعة
    total_deposits = Column(Float, default=0.0) # إجمالي الإيداعات التاريخية
    total_spent = Column(Float, default=0.0) # إجمالي المصروفات التاريخية
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 3. جدول تتبع طلبات الدفع والتحويلات اليدوية (المباشرة أو شحن المحفظة)
class PaymentTransaction(Base):
    __tablename__ = 'payment_transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="SDG")
    
    # خيار مرن يحدد هل الدفع لشحن المحفظة أم لخدمة مباشرة
    target_type = Column(String(50), nullable=False) # "WALLET_REFILL" أو "DIRECT_AD_PAYMENT" أو "SUBSCRIPTION"
    target_reference_id = Column(Integer, nullable=True) # رقم الإعلان أو الباقة المراد تفعيلها مباشرة
    
    # بيانات التحويل اليدوي في السودان (الواقعية)
    receipt_image_path = Column(String(255), nullable=True) # رابط صورة إشعار التحويل/الإيصال
    transaction_number = Column(String(100), nullable=False, unique=True) # رقم العملية
    transfer_date = Column(DateTime, nullable=False) # تاريخ التحويل
    
    # حالات المعاملة المالية كما طلبتها حرفياً
    status = Column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED, REFUNDED, UNDER_REVIEW
    rejection_reason = Column(Text, nullable=True) # يكتبه المشرف في حال الرفض ليظهر للعميل
    
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
