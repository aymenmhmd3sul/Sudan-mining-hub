from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    # البيانات الأساسية للحساب الموحد
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=True)
    
    # 🔒 فلسفة القدرات المفعّلة (Capabilities) بدلاً من الأدوار الجامدة
    is_admin = Column(Boolean, default=False)           # مشرف النظام ذو التحكم الكامل
    is_moderator = Column(Boolean, default=False)       # مراقب جودة العمليات والنزاعات والبلاغات
    is_seller = Column(Boolean, default=False)          # تاجر/معدن يمتلك قدرة نشر الأصول والمعدات
    is_importer = Column(Boolean, default=False)        # مستورد يمتلك قدرة فتح طلبات الاستيراد والتسوية الدولية
    is_global_provider = Column(Boolean, default=False) # مزود خدمات عالمي (شحن، تمويل، حوكمة)
    is_company = Column(Boolean, default=False)         # حساب مؤسسي موثق (شركات تعدين أو تجارة كبرى)
    
    # تفاصيل إضافية لمزودي الخدمات والتجار الدوليين
    provider_country = Column(String(100), nullable=True) # دولة التمركز التجاري (بريطانيا، قطر، عمان، إلخ)
    provider_rating = Column(Float, default=5.0)          # تقييم النجوم الافتراضي من العملاء
    
    # حالة الحساب والتوثيق الإداري
    is_active = Column(Boolean, default=True)
    is_verified_by_admin = Column(Boolean, default=False) # هل راجعت الإدارة مستندات هويته أو سجله التجاري؟
    created_at = Column(DateTime, default=datetime.utcnow)
