from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
import app.models

# 1. الترتيب الخطي: بناء الجداول فور تحميل النواة
Base.metadata.create_all(bind=engine)

# 2. حقن المشرف (Seeding) - يتم بعد بناء الجداول
def init_db():
    db = SessionLocal()
    try:
        from app.models.user import User
        from passlib.context import CryptContext
        
        admin_email = "aymen.mhmd3@gmail.com"
        if not db.query(User).filter(User.email == admin_email).first():
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            new_admin = User(
                full_name="Ayman Mohamed",
                email=admin_email,
                hashed_password=pwd_context.hash("12345678"),
                is_active=True
            )
            db.add(new_admin)
            db.commit()
            print("👤 Admin user seeded successfully.")
    except Exception as e:
        print(f"⚠️ Seeding failed: {e}")
    finally:
        db.close()

init_db()

# 3. إعداد التطبيق
app = FastAPI(title="Sudan Mining Hub")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 4. إعداد الراوترات
from app.routers import auth, opportunities, payments, market, negotiation, communication, trade_desk
app.include_router(auth.router, prefix="/auth")
app.include_router(opportunities.router, prefix="/opportunities")
app.include_router(payments.router, prefix="/payments")
app.include_router(market.router, prefix="/market")
app.include_router(negotiation.router, prefix="/negotiation")
app.include_router(communication.router, prefix="/communication")
app.include_router(trade_desk.router, prefix="/trade")

@app.get("/")
def home():
    return {"status": "online", "message": "System Operational"}
