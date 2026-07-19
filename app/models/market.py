from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class PriceAudit(Base):
    __tablename__ = "price_audit"
    id = Column(Integer, primary_key=True)
    old_price = Column(Float)
    new_price = Column(Float)
    currency = Column(String(10), default="SDG")
    reason = Column(String(255))
    admin_id = Column(Integer) # معرف المشرف الذي قام بالتعديل
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    target_audience = Column(String(50), default="all") # all, merchants, buyers
    is_urgent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
