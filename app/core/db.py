import os
import sqlite3
from sqlmodel import create_engine, Session, SQLModel

# الحصول على عنوان قاعدة البيانات
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
# استخراج مسار الملف للـ SQLite القديم
DATABASE_PATH = "./local.db" 

# إعدادات المحرك
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

# الدالة الأساسية الجديدة (ORM)
def get_db():
    with Session(engine) as session:
        yield session

# الدالة القديمة (Compatibility Wrapper) لمنع انهيار الـ Marketplace
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
