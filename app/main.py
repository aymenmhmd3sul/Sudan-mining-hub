import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
# استيراد الموديلات لضمان تسجيلها في الـ Metadata
try:
    import app.models
except Exception as e:
    logging.error(f"❌ Error importing models: {e}")

app = FastAPI(title="Sudan Mining Hub API")

# إعداد الـ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# محاولة بناء الجداول دون السماح للسيرفر بالانهيار
try:
    Base.metadata.create_all(bind=engine)
    print("🚀 Database tables checked/created successfully!")
except Exception as e:
    print(f"❌ DATABASE INITIALIZATION ERROR: {e}")
    logging.error(f"Critical DB Error: {e}")

@app.get("/")
def home():
    return {"status": "online", "message": "System Operational, check logs for DB status"}
