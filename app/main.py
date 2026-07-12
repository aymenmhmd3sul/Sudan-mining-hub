from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine
from app.core.security import get_password_hash

app = FastAPI(title="Sudan Mining Hub API")

# ضبط الـ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Sudan Mining Hub API", "status": "running"}

# دالة الترقية المركزية - تبدأ من أول السطر بدون مسافات أفقية مسببة للأخطاء
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
