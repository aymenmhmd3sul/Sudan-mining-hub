from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AssetItem(Base):
    __tablename__ = 'asset_items'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id', ondelete='SET NULL'), nullable=True)

    asset_type = Column(String(50), nullable=False) # RAW_GOLD, MINERAL, EQUIPMENT, SERVICE
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    quantity = Column(Float, nullable=False, default=0.0)
    unit = Column(String(20), default='GRAM')
    purity_estimate = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    listings = relationship('MarketListing', back_populates='asset', cascade='all, delete-orphan')

class MarketListing(Base):
    __tablename__ = 'market_listings'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('asset_items.id', ondelete='CASCADE'), nullable=False)
    publisher_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    price = Column(Float, nullable=False)
    currency = Column(String(20), default='SDG')
    listing_type = Column(String(50), default='FIXED')

    status = Column(String(50), default='OPEN')
    is_verified_by_agent = Column(Boolean, default=False)
    verified_agent_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    asset = relationship('AssetItem', back_populates='listings')
    orders = relationship('MarketOrder', back_populates='listing')

class MarketOrder(Base):
    __tablename__ = 'market_orders'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey('market_listings.id', ondelete='CASCADE'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    offered_price = Column(Float, nullable=False)
    order_type = Column(String(50), default='DIRECT')
    status = Column(String(50), default='PENDING')

    created_at = Column(DateTime, default=datetime.utcnow)

    listing = relationship('MarketListing', back_populates='orders')
