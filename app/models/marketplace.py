from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, TypeDecorator, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import json
import enum
from app.database import Base

class SQLiteJSON(TypeDecorator):
    impl = String                        
    def process_bind_param(self, value, dialect):
        if value is None: return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None: return None
        return json.loads(value)

# تطبيق سياسة التصنيف المفتوح
class AssetType(str, enum.Enum):
    WELL = "well"                           # آبار
    MINE = "mine"                           # مناجم
    PRODUCTION_LINE = "production_line"     # خطوط إنتاج
    FACTORY_WORKSHOP = "factory_workshop"   # مصانع وورش
    SHOP = "shop"                           # دكاكين
    HEAVY_EQUIPMENT = "heavy_equipment"     # معدات ثقيلة
    LIGHT_EQUIPMENT = "light_equipment"     # معدات خفيفة
    PRODUCT = "product"                     # منتجات ومواد أخرى
    OTHER = "other"                         # أخرى (عام)

class MiningAsset(Base):
    __tablename__ = "mining_assets"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    # تصنيف الأصول المفتوح بناءً على الدستور المعماري
    asset_type = Column(Enum(AssetType), nullable=False, default=AssetType.OTHER, index=True)
    other_description = Column(String, nullable=True) # إلزامي برمجياً إذا كانت القيمة OTHER
    
    # الحقول القديمة متوافقة مع الأنواع الأخرى
    main_category = Column(String, nullable=False, default="GENERAL")
    sub_category = Column(String, nullable=False, default="GENERAL")
    
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    is_negotiable = Column(Boolean, default=True)
    
    # الموقع الجغرافي
    state_province = Column(String, nullable=False)
    locality = Column(String, nullable=False)
    coordinates = Column(String, nullable=True)
    
    # البيانات والمواصفات المرنة
    images_urls = Column(SQLiteJSON, default=[])
    specific_specs = Column(SQLiteJSON, default={})
    
    # الحالات والتميز
    is_featured = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    status = Column(String, default="ACTIVE")
    
    # -------------------------------------------------------------
    # تطبيق حقول الـ last_* الذكية والتدقيق القياسي لجدول المعروضات
    # -------------------------------------------------------------
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    last_status_change_at = Column(DateTime(timezone=True), nullable=True)
    last_negotiation_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", backref="assets")
