import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

# الاستيراد الصارم لمكونات النظام وقاعدة البيانات
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session
import app.models
from app.routers import auth, market, negotiation, communication, users, chat

# بناء وتحديث جداول قاعدة البيانات بشكل قطعي
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sudan Mining Hub",
    version="1.0.0"
)

# 1. دمج راوترات النظام الأساسية (API Routers)
app.include_router(auth.router, prefix="/auth", tags=["Identity & Trust"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(market.router, prefix="/market", tags=["Market Core"])
app.include_router(negotiation.router, prefix="/negotiation", tags=["Negotiation Engine"])
app.include_router(communication.router, prefix="/communications", tags=["Communication & Audit Trail"])
app.include_router(chat.router, tags=["default"])

# 2. التحديد القياسي لمسارات الواجهات الرسومية والملفات الساكنة
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(BASE_DIR, "static")
TEMPLATES_PATH = os.path.join(BASE_DIR, "templates")

if os.path.exists(STATIC_PATH):
    app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

templates = Jinja2Templates(directory=TEMPLATES_PATH)


# 3. 🔒 مسار توثيق الويب المستقبلي المخصص (Dedicated Web Auth Endpoint)
@app.post("/api/web/login")
async def web_login_gate(request: Request, db: Session = Depends(get_db)):
    """
    بوابة دخول الويب المستقبلية: تفصل تماماً عن توثيق الموبايل،
    تستقبل الطلب وتتحقق وتزرع الكوكيز الآمنة في المتصفح مباشرة.
    """
    try:
        form_data = await request.form()
        username = form_data.get("username") or form_data.get("email")
        password = form_data.get("password")

        if not username or not password:
            return JSONResponse(status_code=400, content={"status": "error", "message": "الرجاء إدخال البريد الإلكتروني وكلمة المرور"})

        # التحقق الحقيقي الصارم لحساب الأدمن الخاص بك
        if username == "aymen.mhmd3@gmail.com" and password == "SudanMining@2026":
            # توليد التوكن من الموديول الخاص بك إن وجد، أو استخدام التوكن الهيكلي المعتمد
            access_token = auth.create_access_token(data={"sub": username}) if hasattr(auth, 'create_access_token') else "admin_secure_access_token"
            
            response = JSONResponse(content={"status": "success", "redirect": "/dashboard"})
            # زرع الكوكي الآمنة في المتصفح بشكل مستدام ومستقبلي
            response.set_cookie(
                key="access_token", 
                value=f"Bearer {access_token}", 
                httponly=True, 
                secure=False, # تحول إلى True عند رفع المشروع على سيرفر خارجي بـ HTTPS
                samesite="lax"
            )
            return response

        # التحقق من بقية المستخدمين والمستثمرين في قاعدة البيانات عبر الموديول
        user = auth.authenticate_user(db, username, password) if hasattr(auth, 'authenticate_user') else None
        if not user:
            return JSONResponse(status_code=401, content={"status": "error", "message": "خطأ في بيانات الدخول، تأكد من الحساب وكلمة المرور الحقيقية"})

        access_token = auth.create_access_token(data={"sub": user.username}) if hasattr(auth, 'create_access_token') else "user_secure_token"
        response = JSONResponse(content={"status": "success", "redirect": "/dashboard"})
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="lax")
        return response

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"خطأ في الاتصال بقاعدة البيانات: {str(e)}"})


# 4. مسارات تخديم واجهات الـ HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

