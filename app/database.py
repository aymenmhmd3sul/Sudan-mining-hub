import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# توحيد اسم ملف قاعدة البيانات على dev.db لضمان قراءة حقيقية موحدة
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# إعداد المحرك برمجياً
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False, "timeout": 30} # رفع مهلة الانتظار لمنع قفل البيانات
    )
    
    # حقن قواعد المعاملات الصارمة لـ SQLite لضمان سلامة العلاقات والكتابة المتزامنة
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL") # وضع الكتابة المسبقة لرفع أداء التزامن
        cursor.close()
else:
    # تم تصحيح المتغير هنا لتمرير DATABASE_URL مباشرة بدلاً من engine
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
