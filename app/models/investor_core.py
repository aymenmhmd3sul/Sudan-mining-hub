from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class InvestorProfile(Base):
    __tablename__ = "investor_profiles"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    country = Column(String(100), nullable=False)
    interests = Column(Text, nullable=True)
    contact_info = Column(Text, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    lois = relationship("LetterOfIntent", back_populates="investor")

class LetterOfIntent(Base):
    __tablename__ = "letters_of_intent"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investor_profiles.id"), nullable=False)
    asset_id = Column(Integer, nullable=False)
    deal_room_id = Column(Integer, nullable=True)
    status = Column(String(50), default="Draft")
    document_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    investor = relationship("InvestorProfile", back_populates="lois")
    audit_logs = relationship("LOIAuditTrail", back_populates="loi")

class LOIAuditTrail(Base):
    __tablename__ = "loi_audit_trails"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    loi_id = Column(Integer, ForeignKey("letters_of_intent.id"), nullable=False)
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    changed_by = Column(String(100), nullable=False)
    action_details = Column(Text, nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)
    loi = relationship("LetterOfIntent", back_populates="audit_logs")
