from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import requests

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

# ربط المسارات
app.include_router(auth.router, prefix="/api/auth", tags=["المصادقة"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["الفرص"])
app.include_router(chat.router, prefix="/api/chat", tags=["المحادثات"])
app.include_router(payments.router, prefix="/api/payments", tags=["المدفوعات"])
app.include_router(admin.router, prefix="/api/admin", tags=["الإدارة"])

# دالة جلب سعر الذهب (مع احتياطي)
def get_price():
    try:
        r = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT",
            timeout=5
        )
        return round(float(r.json()["price"]), 2)
    except:
        try:
            r = requests.get(
                "https://api.gold-api.com/price/XAU",
                timeout=5
            )
            return round(float(r.json()["price"]), 2)
        except:
            return 0.0

# مسار API لسعر الذهب العالمي
@app.get("/api/gold")
def api_gold():
    return {"gold": get_price()}

# الصفحة الرئيسية
@app.get("/")
def root():
    return {"status": "running", "message": "Sudan Mining Hub API"}

# لوحة التحكم الرئيسية
@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# لوحة تحكم المشرف
@app.get("/admin")
def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# ==========================================
# مسارات الأقسام الفرعية لـ v1 (إعادة توجيه الصفحات)
# ==========================================

@app.get("/admin/market")
async def admin_market(request: Request):
    return templates.TemplateResponse("admin/marketplace/index.html", {"request": request})

@app.get("/admin/mining")
async def admin_mining(request: Request):
    return templates.TemplateResponse("admin/mining/index.html", {"request": request})

@app.get("/admin/equipment")
async def admin_equipment(request: Request):
    return templates.TemplateResponse("admin/equipment/index.html", {"request": request})

@app.get("/admin/trade-desk")
async def admin_trade_desk(request: Request):
    return templates.TemplateResponse("admin/trade_desk/index.html", {"request": request})


# ==========================================
# مسارات الواجهات المخصصة لبقية موديولات v1
# ==========================================

@app.get("/admin/finance")
async def admin_finance(request: Request):
    return templates.TemplateResponse("admin/finance/index.html", {"request": request})

@app.get("/admin/users")
async def admin_users(request: Request):
    return templates.TemplateResponse("admin/users/index.html", {"request": request})

@app.get("/admin/communications")
async def admin_communications(request: Request):
    return templates.TemplateResponse("admin/communications/index.html", {"request": request})

@app.get("/admin/content")
async def admin_content(request: Request):
    return templates.TemplateResponse("admin/content/index.html", {"request": request})

@app.get("/admin/reports")
async def admin_reports(request: Request):
    return templates.TemplateResponse("admin/reports/index.html", {"request": request})

@app.get("/admin/administration")
async def admin_administration(request: Request):
    return templates.TemplateResponse("admin/administration/index.html", {"request": request})

@app.get("/admin/security")
async def admin_security(request: Request):
    return templates.TemplateResponse("admin/security/index.html", {"request": request})

@app.get("/admin/offers")
async def admin_offers(request: Request):
    return templates.TemplateResponse("admin/offers/index.html", {"request": request})

@app.get("/admin/payments")
async def admin_payments(request: Request):
    return templates.TemplateResponse("admin/payments/index.html", {"request": request})

@app.get("/admin/opportunities")
async def admin_opportunities(request: Request):
    return templates.TemplateResponse("admin/opportunities/index.html", {"request": request})

@app.get("/admin/services")
async def admin_services(request: Request):
    return templates.TemplateResponse("admin/services/index.html", {"request": request})

