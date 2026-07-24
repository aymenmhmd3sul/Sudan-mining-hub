from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import admin_views, auth, opportunities, chat, payments, admin, web

app = FastAPI(title="Sudan Mining Hub")

# الملفات الاستاتيكية والقوالب
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# استدعاء الموجه الشامل للواجهات (بدون مضاعفة prefix)
app.include_router(admin_views.router)
app.include_router(web.router)

# موجهات API الخلفية
app.include_router(auth.router, prefix="/api/auth", tags=["المصادقة"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["الفرص"])
app.include_router(chat.router, prefix="/api/chat", tags=["المحادثات"])
app.include_router(payments.router, prefix="/api/payments", tags=["المدفوعات"])
app.include_router(admin.router, prefix="/api/admin", tags=["الإدارة"])

@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin/dashboard")
