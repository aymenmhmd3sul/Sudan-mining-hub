import datetime
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# 1. إعداد وحماية النواة وقاعدة البيانات بشكل صارم وموحد عند الإقلاع
try:
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print("🚀 [RADICAL DB SUCCESS] Database engine fully unified and tables verified via Gold Layout.")
except Exception as db_err:
    print(f"⚠️ [DB STARTUP WARN] Database setup bypassed: {db_err}")

# 2. إنشاء تطبيق FastAPI الرئيسي
app = FastAPI(
    title="Sudan Mining Hub API",
    description="البوابة الرقمية الموحدة لإدارة الفرص الاستثمارية والتعدينية",
    version="1.0.0"
)

# 3. إعدادات الـ CORS لضمان مرونة الاتصال
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. ربط الملفات الثابتة وإعداد محرك القوالب (Jinja2) للواجهات
templates = Jinja2Templates(directory="app/templates")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
elif os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 5. استيراد وتضمين الراوترات المعتمدة للأقسام والـ API
from app.routers import auth, opportunities, payments, market, negotiation, communication, trade_desk

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(opportunities.router, prefix="/opportunities", tags=["Opportunities"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(market.router, prefix="/market", tags=["Market Desk"])
app.include_router(negotiation.router, prefix="/negotiation", tags=["Negotiation Rooms"])
app.include_router(communication.router, prefix="/communication", tags=["Communications & Audit"])
app.include_router(trade_desk.router, prefix="/trade", tags=["Trade Desk"])

# 6. مسارات العرض للواجهات الأمامية والتناغم التاريخي المسترجع (Gold Layout)

@app.get("/")
@app.get("/login", response_class=HTMLResponse)
def render_login(request: Request):
    return templates.TemplateResponse("login_master.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def render_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/api/admin/permitted-modules")
def get_permitted_modules():
    # الاحتفاظ بنفس البنية والمنطق الأصلي للموديولات المصرحة
    return ["investors", "opportunities", "payments", "market", "negotiation", "communication", "trade_desk"]

@app.get("/admin/api/modules/{module_name}", response_class=HTMLResponse)
def render_module_fragment(module_name: str, request: Request):
    fragment_path = f"modules/{module_name}.html"
    if not os.path.exists(os.path.join("app/templates", fragment_path)):
        return HTMLResponse(content="<p class='text-danger'>الموديول المطلق غير موجود حالياً.</p>", status_code=404)
    return templates.TemplateResponse(fragment_path, {"request": request})

# 7. نقطة فحص برمجية مخصصة لحالة النظام الأساسي
@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "core_clean": True,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
