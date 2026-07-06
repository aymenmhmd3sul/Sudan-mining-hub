from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class MiningAsset(Base):
    __tablename__ = "mining_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id")) # يربط بالـ User الموحد (الذي لديه قدرة is_seller)
    
    title = Column(String(200), nullable=False)        # عنوان الإعلان (مثال: كسارة حجرية للبيع)
    category = Column(String(100), nullable=False)     # EQUIPMENT, SPARE_PARTS, MINING_LOCATION
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(20), default="SDG")       # العملة المحلية الافتراضية
    
    # إدارة الجودة والبلاغات
    is_featured = Column(Boolean, default=False)       # إعلان مميز (مدفوع باشتراك)
    is_approved = Column(Boolean, default=False)       # معتمد للنشر بعد مراجعة الـ Moderator
    status = Column(String(50), default="ACTIVE")      # ACTIVE, SOLD, SUSPENDED
    created_at = Column(DateTime, default=datetime.utcnow)
