from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Notification(Base):
    __tablename__ = 'notifications'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    notification_type = Column(String(50), default='GENERAL') # DEAL_UPDATE, SYSTEM, CHAT_ALERT
    
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DealEventLog(Base):
    __tablename__ = 'deal_event_logs'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey('market_deals.id', ondelete='CASCADE'), nullable=False)
    actor_id = Column(Integer, ForeignKey('users.id'), nullable=False) # من قام بالإجراء
    
    action = Column(String(100), nullable=False) # APPROVED, REJECTED, MILESTONE_COMPLETED
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
