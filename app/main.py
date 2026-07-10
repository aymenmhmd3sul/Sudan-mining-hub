from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models  # لضمان تسجيل الموديلات في الـ Metadata

app = FastAPI(title="Sudan Mining Hub API")

# إعداد الـ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# بناء الجداول بشكل قياسي مباشر
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"status": "online", "message": "System Operational"}
