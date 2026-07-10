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
    # 🎯 استيراد موديل المستخدم والروابط صراحة لضمان قيام SQLAlchemy بتخليق الجداول فوراً في السيرفر
    from app.models.user import User
    
    Base.metadata.create_all(bind=engine)
    print("🚀 [RADICAL DB SUCCESS] Database engine fully unified and tables (including users) verified.")
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

# 🔄 مسار جسر مستعار وحاسم لحل مشكلة الدخول فوراً بدون تعديل الـ HTML
@app.post("/api/auth/login")
async def api_login_bridge(request: Request):
    """جسر برمجي يستقبل طلبات الواجهة القديمة ويدفعها مباشرة لراوتر الـ Auth المعتمد"""
    from app.routers.auth import login as auth_login_func
    form_data = await request.form()
    
    class MockLoginForm:
        def __init__(self, username, password):
            self.username = username
            self.password = password
    
    mock_form = MockLoginForm(username=form_data.get("username"), password=form_data.get("password"))
    
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        return await auth_login_func(form_data=mock_form, db=db)
    finally:
        db.close()

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
    return ["investors", "dashboard", "opportunities", "payments", "market", "negotiation", "communication", "trade_desk"]

@app.get("/admin/api/modules/{module_name}", response_class=HTMLResponse)
def render_module_fragment(module_name: str, request: Request):
    fragment_path = f"modules/{module_name}.html"
    full_path = os.path.join("app/templates", fragment_path)
    
    if os.path.exists(full_path):
        return templates.TemplateResponse(fragment_path, {"request": request})
        
    placeholder_html = f"""
    <div style="background: #1e1e1e; color: #fff; padding: 30px; border-radius: 8px; text-align: center; border: 1px solid #DAA520; margin: 20px;">
        <h4 style="color: #DAA520; margin-bottom: 15px;"><i class="fas fa-tools"></i> قسم {module_name.upper()} قيد التنشيط الربطي</h4>
        <p style="color: #ccc; font-size: 14px;">يجري العمل حالياً على ربط واجهات هذا القسم بالنواة المركزية وتأمين قنوات تدفق البيانات.</p>
        <div style="margin-top: 15px; color: #DAA520;"><i class="fas fa-spinner fa-spin fa-2x"></i></div>
    </div>
    """
    return HTMLResponse(content=placeholder_html, status_code=200)

# 7. نقطة فحص برمجية مخصصة لحالة النظام الأساسي
@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "core_clean": True,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
