
# --- FIXED ADMIN INJECTION ---
from sqlalchemy import create_engine, text
from app.core.security import get_password_hash
try:
    _eng = create_engine('postgresql://mining_hub_user:aT78wH2pL9qX@dpg-cpl7v9g11fds7397c8fg-a.oregon-postgres.render.com/mining_hub_db')
    clean_pass = 'SudanMining@2026'.strip()
    new_hash = get_password_hash(clean_pass)
    with _eng.connect() as _conn:
        with _conn.begin():
            _conn.execute(text("UPDATE users SET password_hash = :hash, role = 'ADMIN', status = 'ACTIVE' WHERE LOWER(TRIM(email)) = 'aymen.mhmd3@gmail.com'"), {'hash': new_hash})
    print('✅ ADMIN_SYNC: Password and role fixed without spaces.')
except Exception as e:
    print('⚠️ ADMIN_SYNC_ERROR:', e)
# ------------------------------


# --- AUTO ADMIN SYNC BOOT ---
from sqlalchemy import create_engine, text
try:
    _eng = create_engine('postgresql://mining_hub_user:aT78wH2pL9qX@dpg-cpl7v9g11fds7397c8fg-a.oregon-postgres.render.com/mining_hub_db')
    with _eng.connect() as _conn:
        with _conn.begin():
            _conn.execute(text("UPDATE users SET role = 'ADMIN', status = 'ACTIVE' WHERE email = 'aymen.mhmd3@gmail.com'"))
    print('✅ SYSTEM_BOOT: Admin synced successfully.')
except Exception as e:
    print('⚠️ SYSTEM_BOOT_ERROR:', e)
# ----------------------------

import os
import importlib
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.core.db import engine

# استيراد النماذج لضمان تعيينها لـ SQLModel قبل إنشاء الجداول
from app.models.auth import User

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(on_startup=[create_db_and_tables])

# Auto-discovery for routers
routers_dir = os.path.join(os.path.dirname(__file__), "routers")
for filename in os.listdir(routers_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"app.routers.{filename[:-3]}"
        module = importlib.import_module(module_name)
        if hasattr(module, "router"):
            app.include_router(module.router)
