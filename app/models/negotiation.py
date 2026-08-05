from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class MarketDeal(Base):
    __tablename__ = "negotiation_rooms"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("mining_assets.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="OPEN") # OPEN, ACCEPTED, REJECTED, CLOSED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # علاقة عكسية لجلب الرسائل المرتبطة بالغرفة
    messages = relationship("NegotiationMessage", back_populates="room", cascade="all, delete-orphan")
    
    asset = relationship("MiningAsset", backref="market_deals")
    seller = relationship("User", foreign_keys=[seller_id], backref="sales_deals")
    buyer = relationship("User", foreign_keys=[buyer_id], backref="purchase_deals")


class NegotiationMessage(Base):
    __tablename__ = "negotiation_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("negotiation_rooms.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_type = Column(String, default="TEXT") # TEXT, OFFER, SYSTEM
    message = Column(String, nullable=False)
    
    # حقول استثمار المستقبل
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=True)
    reply_to_id = Column(Integer, ForeignKey("negotiation_messages.id"), nullable=True)
    is_read = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    room = relationship("MarketDeal", back_populates="messages")
    sender = relationship("User", backref="sent_messages")
    replied_to = relationship("NegotiationMessage", remote_side=[id], backref="replies")


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("negotiation_rooms.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="PENDING") # PENDING, ACCEPTED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("MarketDeal", backref="offers")
    # تم ربط العرض بالرسالة عبر ForeignKey داخل كلاس NegotiationMessage
    message_entry = relationship("NegotiationMessage", backref="linked_offer", foreign_keys=[NegotiationMessage.offer_id], uselist=False)

class DealMilestone(Base):
    __tablename__ = "deal_milestones"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("negotiation_rooms.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
