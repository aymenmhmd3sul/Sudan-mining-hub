from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)  # نوع الحركة: LOGIN, APPROVE_ASSET...
    target_type = Column(String(50), nullable=True) # الجدول المتأثر: asset, user, deal
    target_id = Column(Integer, nullable=True)     # معرف الصف المتأثر
    details = Column(Text, nullable=True)          # تفاصيل إضافية بتنسيق نصي أو JSON
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
