from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine
from app.core.security import get_password_hash
from app.routers import auth, buyer, seller  # تأكد من مطابقة الروترز النشطة لديك

app = FastAPI(title="Sudan Mining Hub API")

from sqlalchemy import text
from app.database import engine
from app.core.security import get_password_hash

@app.on_event('startup')
    try:
        clean_pass = 'SudanMining@2026'.strip()
        new_hash = get_password_hash(clean_pass)
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text("UPDATE users SET password_hash = :hash, role = 'ADMIN', status = 'ACTIVE' WHERE LOWER(TRIM(email)) = 'aymen.mhmd3@gmail.com'"),
                    {'hash': new_hash}
                )
    except Exception as e:


# ضبط الـ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# حدث الإقلاع المركزي الموثوق لترقية حسابك وتثبيت كلمة المرور برمجياً
@app.on_event("startup")
    try:
        clean_pass = 'SudanMining@2026'.strip()
        new_hash = get_password_hash(clean_pass)
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text("UPDATE users SET password_hash = :hash, role = 'ADMIN', status = 'ACTIVE' WHERE LOWER(TRIM(email)) = 'aymen.mhmd3@gmail.com'"),
                    {'hash': new_hash}
                )
        print("✅ [MAIN_BOOT] Master Admin synchronized and secured successfully.")
    except Exception as e:
        print("⚠️ [MAIN_BOOT_ERROR]", e)

# تضمين المسارات المتاحة
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# أضف هنا أي include_router أخرى إذا كانت موجودة في ملفك الأصلي

@app.get("/")
def read_root():
    return {"message": "Welcome to Sudan Mining Hub API", "status": "running"}

# --- FINAL CLEAN ADMIN SYNC ---
from sqlalchemy import text
from app.database import engine
from app.core.security import get_password_hash

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
