from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class MarketDeal(Base):
    __tablename__ = 'market_deals'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('market_listings.id', ondelete='RESTRICT'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    final_price = Column(Float, nullable=False)
    currency = Column(String(20), default='SDG')
    
    # حالة الصفقة الكلية: PENDING_APPROVAL, ACTIVE_DISPATCH, IN_LAB_TESTING, COMPLETED, DISPUTED
    status = Column(String(50), default='PENDING_APPROVAL')
    
    # توثيق الحسابات والعمولات المترتبة بناء على قواعد النظام
    calculated_commission = Column(Float, default=0.0)
    is_commission_paid = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    milestones = relationship('DealMilestone', back_populates='deal', cascade='all, delete-orphan')

class DealMilestone(Base):
    __tablename__ = 'deal_milestones'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey('market_deals.id', ondelete='CASCADE'), nullable=False)
    
    title = Column(String(150), nullable=False) # مثل: فحص عينة الذهب بالمعمل، الشحن، السداد
    description = Column(Text, nullable=True)
    step_order = Column(Integer, default=1) # ترتيب الخطوة في التنفيذ
    
    status = Column(String(50), default='PENDING') # PENDING, IN_PROGRESS, VERIFIED, FAILED
    is_critical = Column(Boolean, default=True) # هل الخطوة إلزامية لإغلاق الصفقة؟
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    deal = relationship('MarketDeal', back_populates='milestones')
