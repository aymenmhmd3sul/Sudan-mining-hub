from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# استيراد الراوتات
from app.routers import auth, opportunities, chat, payments, admin

app = FastAPI(
    title="Sudan Mining Hub",
    description="منصة السودان للتعدين والاستثمار",
    version="1.0.0"
)

# إعداد المجلدات
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

# ربط المسارات (Routers)
app.include_router(auth.router, prefix="/api/auth", tags=["المصادقة"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["الفرص"])
app.include_router(chat.router, prefix="/api/chat", tags=["المحادثات"])
app.include_router(payments.router, prefix="/api/payments", tags=["المدفوعات"])
app.include_router(admin.router, prefix="/api/admin", tags=["الإدارة"])

@app.get("/")
def root():
    return {"status": "running", "message": "Sudan Mining Hub API"}

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
