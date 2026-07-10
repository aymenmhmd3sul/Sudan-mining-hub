import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# استيراد محرك قاعدة البيانات والموديلات بشكل صارم ومباشر من المصدر الموحد
try:
    from app.database import Base, engine, SessionLocal
    from app.models.user import User
    from app.models.opportunity import Opportunity

    # إنشاء كافة الجداول مسبقاً وبشكل حاسم عند الإقلاع
    Base.metadata.create_all(bind=engine)
    print("🚀 [RADICAL DB SUCCESS] Database engine fully unified and tables verified.")
    
    # حشو بيانات تجريبية آمنة لمنع فراغ الواجهة
    db_session = SessionLocal()
    if not db_session.query(Opportunity).first():
        db_session.add(Opportunity(
            title="مشروع استثماري تجريبي موحد",
            opportunity_type="تعدين",
            description="تم توليد هذه الفرصة تلقائياً بعد تطبيق الحل الجذري لقاعدة البيانات.",
            target_amount=120000.0,
            status="OPEN",
            deadline=datetime.datetime.utcnow() + datetime.timedelta(days=30)
        ))
        db_session.commit()
        print("🚀 [DB SEED] Sample opportunity generated successfully.")
    db_session.close()
except Exception as radical_err:
    print(f"⚠️ [DB STARTUP WARN] Database setup bypassed or logged: {radical_err}")

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Sudan Mining Hub API",
    description="البوابة الرقمية الموحدة لإدارة الفرص الاستثمارية والتعدينية",
    version="1.0.0"
)

# إعدادات الـ CORS لضمان اتصال الـ Streamlit والواجهات الأمامية بسلاسة
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# استيراد الراوترات المعتمدة للأقسام
from app.routers import auth, opportunities, payments, market, negotiation, communication, trade_desk

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(opportunities.router, prefix="/opportunities", tags=["Opportunities"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(market.router, prefix="/market", tags=["Market Desk"])
app.include_router(negotiation.router, prefix="/negotiation", tags=["Negotiation Rooms"])
app.include_router(communication.router, prefix="/communication", tags=["Communications & Audit"])
app.include_router(trade_desk.router, prefix="/trade", tags=["Trade Desk"])

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Welcome to Sudan Mining Hub API. Main core is running radically clean.",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
