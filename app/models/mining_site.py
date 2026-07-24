from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.core.db import Base

class MiningSite(Base):
    __tablename__ = "mining_sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    resource_type = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=False)
    locality = Column(String(100), nullable=False)
    coordinates = Column(String(100), nullable=True)
    owner_id = Column(Integer, nullable=False, index=True)
    status = Column(String(50), default="active")
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
