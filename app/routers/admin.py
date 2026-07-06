from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Platform"])
templates = Jinja2Templates(directory="app/templates")

# 1. مسار عرض الواجهة (مفتوح لعرض الهيكل فقط، المتصفح سيتولى طرد غير المسجلين)
@router.get("", response_class=HTMLResponse)
async def get_admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# 2. مسار جلب البيانات الحساسة (محمي بصرامة شديدة من جهة الخادم)
@router.get("/api/dashboard-data")
async def get_secure_dashboard_data(current_admin: dict = Depends(get_current_admin)):
    # هذا المسار لا يعيد أي بيانات إلا إذا كان التوكن صحيحاً وصلاحيته Admin
    return {
        "status": "success",
        "admin_email": current_admin.get("sub"),
        "system_stats": {
            "active_traders": 124,
            "foreign_investors": 18,
            "international_agents": 5,
            "pending_lois": 3
        }
    }
