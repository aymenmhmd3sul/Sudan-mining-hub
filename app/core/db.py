import os
from sqlmodel import create_engine, Session, SQLModel

# الحصول على عنوان قاعدة البيانات من البيئة (Render سيقوم بتوفير DATABASE_URL)
# إذا لم يوجد، سنستخدم قاعدة بيانات محلية للتطوير
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")

# إعدادات المحرك: SQLite يحتاج لـ check_same_thread=False
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_db():
    with Session(engine) as session:
        yield session
