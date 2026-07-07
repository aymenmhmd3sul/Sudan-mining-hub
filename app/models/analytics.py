from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from datetime import datetime
from app.database import Base

class MarketPriceTicker(Base):
    __tablename__ = 'market_price_tickers'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    asset_type = Column(String(50), nullable=False) # RAW_GOLD, MINERAL, EQUIPMENT, SERVICE
    subtype = Column(String(50), nullable=True)     # مثلاً: عيار 21, عيار 24, كسارة حجرية
    
    price_average = Column(Float, nullable=False)
    price_min = Column(Float, nullable=True)
    price_max = Column(Float, nullable=True)
    currency = Column(String(20), default='SDG')
    
    recorded_date = Column(DateTime, default=datetime.utcnow)

class AIRecommendation(Base):
    __tablename__ = 'ai_recommendations'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    target_asset_type = Column(String(50), nullable=False)
    
    recommendation_title = Column(String(200), nullable=False)
    recommendation_text = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.0) # نسبة ثقة النموذج الذكي (مثلا 0.85)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
