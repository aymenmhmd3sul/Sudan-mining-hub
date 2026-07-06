import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# قراءة رابط قاعدة البيانات من خادم الإنتاج، أو التحول تلقائياً لـ SQLite محلياً
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sudan_mining_hub.db")

# معالجة خاصة لـ PostgreSQL على خوادم Render إذا بدأ الرابط بـ postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# إعداد المحرك برمجياً بشكل مرن ومحايد
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# دالة حقن الجلسة (Dependency Injection) للاستخدام في المسارات
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
