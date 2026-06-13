from sqlalchemy import Column, Boolean, Integer, String, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class BuyerRequest(Base):
    __tablename__ = 'buyer_requests'

    id = Column(Integer, primary_key=True)
    buyer_name = Column(String)
    whatsapp = Column(String)
    category = Column(String)
    specs = Column(Text)

    status = Column(String, default='new')
    buyer_confirmed = Column(Boolean, default=False)
    trader_confirmed = Column(Boolean, default=False)
    is_heavy_deal = Column(Boolean, default=False)
    manual_override = Column(Boolean, default=False)
    estimated_value = Column(String, nullable=True)
    created_at = Column(String, default=str(datetime.utcnow()))


class Trader(Base):
    __tablename__ = 'traders'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    whatsapp = Column(String)
    specialties = Column(String)
    code = Column(String)
    created_at = Column(String, default=str(datetime.utcnow()))


class TraderOffer(Base):
    __tablename__ = 'trader_offers'

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer)
    trader_id = Column(Integer)
    price = Column(String)
    details = Column(Text)
    status = Column(String, default='active')
    created_at = Column(String, default=str(datetime.utcnow()))


class MarketItem(Base):
    __tablename__ = 'market_items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    category = Column(String)
    created_at = Column(String, default=str(datetime.utcnow()))
