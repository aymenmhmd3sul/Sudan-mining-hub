import os
from sqlmodel import create_engine, Session

# قراءة رابط قاعدة البيانات من المتغير البيئي الآمن في Render
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # تصحيح صيغة الرابط لتتوافق مع مكتبات SQLAlchemy الحديثة
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# إعدادات الاتصال الآمن الحتمية لـ Render (SSL Mode)
connect_args = {}
if DATABASE_URL and "postgresql" in DATABASE_URL:
    connect_args = {"sslmode": "require"}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

# دالة توليد الجلسات لإدارة العمليات وإغلاقها تلقائياً
def get_session():
    with Session(engine) as session:
        yield session
