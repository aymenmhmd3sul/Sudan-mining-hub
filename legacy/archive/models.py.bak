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
    created_at = Column(String, default=str(datetime.utcnow()))

class Trader(Base):
    __tablename__ = 'traders'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    whatsapp = Column(String)
    specialties = Column(String)  # مثال: "بوكلين,لودر"
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

contact_locked = Column(Boolean, default=True)
agreed_price = Column(String, nullable=True)
