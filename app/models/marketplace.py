from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, TypeDecorator
from sqlalchemy.orm import relationship
from datetime import datetime
import json
from app.database import Base

class SQLiteJSON(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is None: return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None: return None
        return json.loads(value)

class MiningAsset(Base):
    __tablename__ = "mining_assets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    main_category = Column(String, nullable=False)
    sub_category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    is_negotiable = Column(Boolean, default=True)
    state_province = Column(String, nullable=False)
    locality = Column(String, nullable=False)
    coordinates = Column(String, nullable=True)
    images_urls = Column(SQLiteJSON, default=[])
    specific_specs = Column(SQLiteJSON, default={})
    is_featured = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # إضافة الحقل المطلوب من قبل الـ Schema هندسياً
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", backref="assets")
