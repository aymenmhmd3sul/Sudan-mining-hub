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
