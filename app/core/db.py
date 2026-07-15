"""
هذا الملف يعمل كواجهة معمارية (Interface) موحدة للوصول إلى محرك ومخططات قاعدة البيانات،
موجهاً الاستدعاءات إلى المورد الحقيقي في app/database.py لضمان عدم تكرار الكود (DRY).
"""
from app.database import engine, SessionLocal, get_db

# جعل الـ Base متوافقاً تماماً مع SQLAlchemy 2.0 الصارم
from app.database import Base
