from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class GlobalTradeDeskRequest(Base):
    __tablename__ = "global_trade_desk_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))      # المستورد طالب الخدمة (is_importer)
    
    title = Column(String(200), nullable=False)              # مثل: تنسيق استيراد لوادر شحن من الصين
    service_type = Column(String(100))                      # LOGISTICS, FINANCING, COMPLIANCE
    target_country = Column(String(100), nullable=False)    # الصين، تركيا، الإمارات
    estimated_value = Column(Float, nullable=False)          # القيمة التقديرية بالدولار
    
    # مستندات الحوكمة للملف
    proforma_invoice_url = Column(String(255), nullable=True)
    packing_list_url = Column(String(255), nullable=True)
    
    status = Column(String(50), default="OPEN")             # OPEN, IN_PROGRESS, COMPLETED, DISPUTED
    created_at = Column(DateTime, default=datetime.utcnow)

class GlobalTradeBid(Base):
    __tablename__ = "global_trade_bids"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("global_trade_desk_requests.id"))
    provider_id = Column(Integer, ForeignKey("users.id"))    # مزود الخدمة (is_global_provider)
    
    service_name = Column(String(150), nullable=False)       # اسم الكيان التجاري المقترح (Oman Logistics مثلاً)
    commission_percentage = Column(Float, nullable=False)    # نسبة التنسيق
    delivery_time_frame = Column(String(100), nullable=False) # مدة التنفيذ المقترحة
    service_description = Column(String(500), nullable=True)
    
    status = Column(String(50), default="PENDING")           # PENDING, ACCEPTED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)
