import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# استدعاء المسارات المعتمدة للمصادقة وللإدارة
from app.routers import admin_views
try:
    from app.routers import auth
except ImportError:
    auth = None

app = FastAPI(title="Sudan Mining Hub")

# ربط الملفات الاستاتيكية
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# 1. الشاشة الرئيسية للموقع (Landing Page)
@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    if os.path.exists("app/templates/index.html"):
        return templates.TemplateResponse(request=request, name="index.html")
    elif os.path.exists("app/templates/gateway.html"):
        return templates.TemplateResponse(request=request, name="gateway.html")
    return HTMLResponse("<h2>مرحباً بك في منصة سودان مايننج هاب</h2>")

# 2. صفحة تسجيل الدخول
@app.get("/login", response_class=HTMLResponse)
async def serve_login_page(request: Request):
    if os.path.exists("app/templates/auth/login.html"):
        return templates.TemplateResponse(request=request, name="auth/login.html")
    elif os.path.exists("app/templates/login.html"):
        return templates.TemplateResponse(request=request, name="login.html")
    return templates.TemplateResponse(request=request, name="admin/dashboard.html")

# 3. تضمين رواتر المصادقة الأصلي (لتحقق السيرفر من كلمة المرور والبريد بشكل صحيح)
if auth and hasattr(auth, 'router'):
    app.include_router(auth.router)

# 4. تضمين مسارات الإدارة والداش بورد
app.include_router(admin_views.router)
