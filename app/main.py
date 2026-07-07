from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.models.marketplace import MiningAsset
from app.models.role import Role
from app.routers import market

# تهيئة التطبيق
app = FastAPI(title="Sudan Mining Hub API")

# دورة حياة التطبيق لضمان سلامة هيكل البيانات (Migrations-Lite)
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✓ تم التأكد من سلامة الهيكل الجدولي في قاعدة البيانات.")

# ربط الموجهات الأساسية
app.include_router(market.router)
