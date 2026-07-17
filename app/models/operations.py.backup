from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from datetime import datetime
from app.database import Base

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False) # FREE, TRADER, COMPANY, GLOBAL_PROVIDER
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, default=30)
    listing_limit = Column(Integer, default=5)              # حد الإعلانات المسموحة
    commission_rate = Column(Float, default=2.5)            # نسبة عمولة المنصة من الصفقات

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)     # Bank_of_Khartoum, Cache, International_Bank
    reference_number = Column(String(100), unique=True)     # رقم إشعار التحويل المرفوع
    status = Column(String(50), default="PENDING")           # PENDING, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)  # support_phone, terms_conditions, homepage_hero_title
    value = Column(Text, nullable=False)
