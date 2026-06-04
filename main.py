import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# --- إعدادات قاعدة البيانات الذكية ---
# التحقق من وجود قاعدة بيانات سحابية (Render) وإلا التحول تلقائياً إلى SQLite محلية
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    # محاولة إنشاء الجداول في السحاب
    try:
        import models
        from database import engine as db_engine
        models.Base.metadata.create_all(bind=db_engine)
    except Exception as e:
        print(f"قاعدة البيانات السحابية مهيأة أو واجهت تنبيهاً: {e}")
else:
    # بيئة التطوير المحلية (SQLite) لضمان عدم توقف السيرفر على الهاتف
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine("sqlite:///./local_sub_hub.db", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

app = FastAPI(title="منصة تعدين السودان الرقمية - Sudan Mining Hub", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- البيانات الوهمية المستقرة للتأكد من عمل البيئتين ---
mock_sites = [
    {"id": 1, "name": "موقع أبو حمد الرئيسي", "location": "ولاية نهر النيل", "is_active": True},
    {"id": 2, "name": "موقع وادي حلفا", "location": "الولاية الشمالية", "is_active": True}
]

mock_equipment = [
    {"id": 1, "name": "غربال ذهب هيدروليكي", "type": "تصفية", "status": "متاح"},
    {"id": 2, "name": "جرافة تعدين CAT", "type": "حفر", "status": "في الخدمة"}
]

# --- الـ Schemas الأساسية ---
class MiningSiteSchema(BaseModel):
    id: Optional[int] = None
    name: str
    location: str
    is_active: bool

class EquipmentSchema(BaseModel):
    id: Optional[int] = None
    name: str
    type: str
    status: str

# --- الـ Endpoints المستقرة (التي تعطي استجابة 200) ---
@app.get("/")
def read_root():
    return {"status": "running", "environment": "Cloud (Render)" if os.getenv("DATABASE_URL") else "Local (Termux)"}

@app.get("/api/v1/mining/sites", response_model=List[MiningSiteSchema], status_code=200)
def get_mining_sites():
    return mock_sites

@app.get("/api/v1/mining/sites/{site_id}", response_model=MiningSiteSchema, status_code=200)
def get_mining_site_by_id(site_id: int):
    site = next((s for s in mock_sites if s["id"] == site_id), None)
    if not site:
        raise HTTPException(status_code=404, detail="موقع التعدين غير موجود")
    return site

@app.get("/api/v1/equipment", response_model=List[EquipmentSchema], status_code=200)
def get_all_equipment():
    return mock_equipment

@app.post("/api/v1/equipment", response_model=EquipmentSchema, status_code=201)
def create_equipment(equipment: EquipmentSchema):
    new_item = equipment.dict()
    mock_equipment.append(new_item)
    return new_item
