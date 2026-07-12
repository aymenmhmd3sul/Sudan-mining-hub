import os
import importlib
from fastapi import FastAPI

app = FastAPI()

# Auto-discovery for routers
routers_dir = os.path.join(os.path.dirname(__file__), "routers")
for filename in os.listdir(routers_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"app.routers.{filename[:-3]}"
        module = importlib.import_module(module_name)
        if hasattr(module, "router"):
            app.include_router(module.router)
