from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.database import Base

class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    swift_code = Column(String(20))
    is_active = Column(Boolean, default=True)
    config = Column(JSON)
