from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models  # لضمان تسجيل الموديلات في الـ Metadata

# استيراد الـ Routers بناءً على التحقق الفعلي
from app.routers import (
    auth, users, market, marketplace, trade_desk,
    negotiation, negotiation_ws, communication, chat,
    opportunities, payments, services,
    admin, admin_center, admin_control, admin_modules, admin_users
)

app = FastAPI(title="Sudan Mining Hub API")

# إعداد الـ CORS لضمان اتصال جميع النوافذ والتطبيقات الخارجية بدون قيود
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# بناء وتحديث الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)

# دمج النوافذ الأساسية بناءً على الـ Prefixes الأصلية المعرفة داخلها
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(market.router)
app.include_router(marketplace.router)
app.include_router(trade_desk.router)
app.include_router(negotiation.router)
app.include_router(negotiation_ws.router)
app.include_router(communication.router)
app.include_router(chat.router, prefix="/api/chat") # تم تأمينه بـ prefix لأن ملفه الأصلي فارغ من الـ prefix
app.include_router(opportunities.router)
app.include_router(payments.router)
app.include_router(services.router)

# دمج نوافذ الإدارة والتحكم (Admin Panel) بدون تداخل مسارات
app.include_router(admin.router)
app.include_router(admin_center.router)
app.include_router(admin_control.router)
app.include_router(admin_modules.router)
app.include_router(admin_users.router)

@app.get("/")
def home():
    return {"status": "online", "message": "System Operational", "modules_loaded": True}
