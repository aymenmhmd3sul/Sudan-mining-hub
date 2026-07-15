from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)

class MiningAsset(Base):
    __tablename__ = "mining_assets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    currency = Column(String(10), default="SDG")
    
    # فلسفة النشر لعام 2026
    listing_tier = Column(String(20), default="OPEN") # OPEN, VERIFIED, PREMIUM
    status = Column(String(50), default="DRAFT")
    
    seller_id = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # مؤشرات سريعة للنشاط والذكاء التعديني
    views_count = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)
    trust_score = Column(Float, default=50.0)
    
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


    version = Column(Integer, default=1, nullable=False)

    __mapper_args__ = {
        "version_id_col": version
    }
    # العلاقات الكاملة والمطابقة %100 لكافة امتدادات النظام لضمان استقرار الـ Mapper
    category = relationship("Category", back_populates="assets")
    locations = relationship("AssetLocation", back_populates="asset", cascade="all, delete-orphan")
    specs = relationship("AssetSpec", back_populates="asset", cascade="all, delete-orphan")
    status_history = relationship("AssetStatusHistory", back_populates="asset", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="asset", cascade="all, delete-orphan")
    
    # شبكة العلاقات التفاعلية المتبقية (المفاوضات، البلاغات، الفعاليات)
    negotiations = relationship("AssetNegotiation", back_populates="asset", cascade="all, delete-orphan")
    events = relationship("AssetEvent", back_populates="asset", cascade="all, delete-orphan")
    reports = relationship("AssetReport", back_populates="asset", cascade="all, delete-orphan")
    
    # سجلات التفاعل الجماهيري للأصول (المفضلة والمشاهدات)
    favorites = relationship("AssetFavorite", back_populates="asset", cascade="all, delete-orphan")
    views = relationship("AssetView", back_populates="asset", cascade="all, delete-orphan")
    
    # ربط برمي مرن للصور بدون متطلب حقل عكسي
    images = relationship("AssetImage", cascade="all, delete-orphan")

Category.assets = relationship("MiningAsset", order_by=MiningAsset.id, back_populates="category")
