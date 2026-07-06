from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime
from app.database import Base

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    opportunity_type = Column(String(100), nullable=False)  # INVESTMENT, TENDER, AUCTION, FUNDING
    description = Column(Text, nullable=False)
    target_amount = Column(Float, nullable=True)            # للمزادات أو التمويل
    deadline = Column(DateTime, nullable=True)
    status = Column(String(50), default="OPEN")             # OPEN, CLOSED, AWARDED
    created_at = Column(DateTime, default=datetime.utcnow)
