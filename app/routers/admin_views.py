import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["Admin Views"])
templates = Jinja2Templates(directory="app/templates")

# الداش بورد الرئيسي للمشرف
@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={"active_tab": "dashboard"})

# معالج كافة أقسام القائمة الجانبية المنسدلة
@router.get("/{module_name}", response_class=HTMLResponse)
@router.get("/{module_name}/{subpath:path}", response_class=HTMLResponse)
async def render_admin_module(request: Request, module_name: str, subpath: str = ""):
    template_path = f"admin/{module_name}/index.html"
    full_path = os.path.join("app/templates", template_path)
    
    if os.path.exists(full_path):
        return templates.TemplateResponse(request=request, name=template_path, context={"active_tab": module_name})
    
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={"active_tab": module_name})
