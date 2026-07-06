from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, JSON
from app.models.base import Base # سنفترض وجود ملف للقاعدة الأساسية

# 1. جدول أنواع باقات الإعلانات (عادي، مميز، عاجل، مثبت، شركة)
class AdPackage(Base):
    __tablename__ = 'ad_packages'
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True) # مثلاً: 'urgent', 'pinned'
    name_ar = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, default=7)
    is_active = Column(Boolean, default=True)
    features = Column(JSON) # ميزات الباقة (مثلاً: {"top_position": true, "highlight_color": "gold"})

# 2. جدول محرك العمولات الديناميكي
class CommissionRule(Base):
    __tablename__ = 'commission_rules'
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100)) # مثلاً: 'ذهب', 'آليات ثقيلة', 'عقارات'
    ad_package_type = Column(String(50)) # نوع الإعلان المرتبط بالعمولة
    commission_type = Column(String(20)) # 'PERCENTAGE' أو 'FIXED'
    commission_value = Column(Float, nullable=False) # نسبة أو مبلغ مقطوع
    membership_level = Column(String(50), default="ALL") # 'VIP', 'NORMAL', 'ALL'
    
    # يتيح هذا الجدول للمشرف إضافة قاعدة جديدة: 
    # "إذا كان الإعلان (آليات ثقيلة) و(عضوية التاجر VIP)، احسب عمولة (2%)"
