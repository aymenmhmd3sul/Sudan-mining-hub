import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# قراءة إعدادات البيئة
load_dotenv()

# قراءة رابط قاعدة البيانات من متغيرات البيئة في ريندر
DATABASE_URL = os.getenv("DATABASE_URL")

# تأمين التوافق مع روابط PostgreSQL الحديثة
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# إذا لم يجد الرابط، يستخدم قاعدة بيانات محلية مؤقتة للاختبار
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
