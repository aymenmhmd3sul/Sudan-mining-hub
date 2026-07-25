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
@router.get("/dashboard-v2", response_class=HTMLResponse)
async def admin_dashboard_v2(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard_v2.html",
        context={"active_tab": "dashboard"}
    )

@router.get("/{module_name}", response_class=HTMLResponse)
@router.get("/{module_name}/{subpath:path}", response_class=HTMLResponse)
async def render_admin_module(request: Request, module_name: str, subpath: str = ""):

    # استثناء وحدة Escrow حتى لا يلتقطها الـ wildcard العام
    if module_name == "finance" and subpath == "escrow":
        return templates.TemplateResponse(
            request=request,
            name="admin/finance/escrow.html",
            context={"active_tab": "escrow"}
        )

    # تحويل الشرطة العادية إلى سفليّة لتطابق مجلدات القوالب
    normalized_module = module_name.replace('-', '_')
    normalized_subpath = subpath.replace('-', '_') if subpath else ''

    if normalized_subpath:
        sub_template_path = f"admin/{normalized_module}/{normalized_subpath}/index.html"
        if os.path.exists(os.path.join("app/templates", sub_template_path)):
            template_path = sub_template_path
        else:
            template_path = f"admin/{normalized_module}/index.html"
    else:
        template_path = f"admin/{normalized_module}/index.html"

    full_path = os.path.join("app/templates", template_path)
    
    context = {"active_tab": module_name, "room_id": subpath if subpath else "1"}
    
    if os.path.exists(full_path):
        return templates.TemplateResponse(request=request, name=template_path, context=context)
    
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context=context)


@router.get("/dashboard-v2", response_class=HTMLResponse)
async def admin_dashboard_v2(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard_v2.html",
        context={"active_tab": "dashboard"}
    )
