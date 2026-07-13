from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine
from app.core.security import get_password_hash

# استيراد الروترز الحقيقي المؤكد
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

app = FastAPI(title="Sudan Mining Hub API")

# ضبط الـ CORS لضمان استقبال الطلبات
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط المسارات بشكل مباشر ليطابق تماماً روابط الفحص
app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(users_router, prefix="", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Sudan Mining Hub API", "status": "running"}

# دالة الترقية المركزية المستقرة دون أي إزاحات حروف
@app.on_event("startup")
def sync_admin_account_clean():
    try:
        clean_pass = 'SudanMining@2026'.strip()
        new_hash = get_password_hash(clean_pass)
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text("UPDATE users SET password_hash = :hash, role = 'ADMIN', status = 'ACTIVE' WHERE LOWER(TRIM(email)) = 'aymen.mhmd3@gmail.com'"),
                    {"hash": new_hash}
                )
        print("✅ [BOOT_SUCCESS] Admin synchronized successfully.")
    except Exception as e:
        print("⚠️ [BOOT_ERROR]", e)
