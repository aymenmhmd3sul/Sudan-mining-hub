import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. إعداد المسارات المطلقة لقاعدة البيانات
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, "local.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# 2. إعداد محرك ومولد جلسات SQLAlchemy (للمستقبل والـ ORM والإدارة)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# [النمط الأول المستقبلي]: مولد جلسات ORM يغلق الاتصال تلقائياً بعد كل طلب
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# [النمط الثاني الحالي]: الاتصال الخام لملفات الـ Marketplace القديمة
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
