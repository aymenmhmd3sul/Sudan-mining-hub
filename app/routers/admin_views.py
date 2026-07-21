from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["Admin Center Views"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    user_data = getattr(request.state, 'user', None)
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={"user": user_data, "active_tab": "dashboard"}
    )
@router.get("/marketplace", response_class=HTMLResponse)
async def admin_marketplace(request: Request):
    return templates.TemplateResponse("admin/marketplace/index.html", context={"request": request})

@router.get("/mining", response_class=HTMLResponse)
async def admin_mining(request: Request):
    return templates.TemplateResponse("admin/mining/index.html", context={"request": request})

@router.get("/equipment", response_class=HTMLResponse)
async def admin_equipment(request: Request):
    return templates.TemplateResponse("admin/equipment/index.html", context={"request": request})

@router.get("/finance", response_class=HTMLResponse)
async def admin_finance(request: Request):
    return templates.TemplateResponse("admin/finance/index.html", context={"request": request})

@router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request):
    return templates.TemplateResponse("admin/users/index.html", context={"request": request})

@router.get("/communications", response_class=HTMLResponse)
async def admin_communications(request: Request):
    return templates.TemplateResponse("admin/communications/index.html", context={"request": request})

@router.get("/content", response_class=HTMLResponse)
async def admin_content(request: Request):
    return templates.TemplateResponse("admin/content/index.html", context={"request": request})

@router.get("/reports", response_class=HTMLResponse)
async def admin_reports(request: Request):
    return templates.TemplateResponse("admin/reports/index.html", context={"request": request})

@router.get("/administration", response_class=HTMLResponse)
async def admin_administration(request: Request):
    return templates.TemplateResponse("admin/administration/index.html", context={"request": request})

@router.get("/security", response_class=HTMLResponse)
async def admin_security(request: Request):
    return templates.TemplateResponse("admin/security/index.html", context={"request": request})

@router.get("/identity", response_class=HTMLResponse)
async def admin_identity_view(request: Request):
    return templates.TemplateResponse("admin/identity/index.html", {"request": request, "active_tab": "users"})

@router.get("/audit", response_class=HTMLResponse)
async def admin_audit_view(request: Request):
    return templates.TemplateResponse("admin/audit/index.html", {"request": request, "active_tab": "security"})

@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics_view(request: Request):
    return templates.TemplateResponse("admin/analytics/index.html", {"request": request, "active_tab": "reports"})

@router.get("/trade_desk", response_class=HTMLResponse)
async def admin_trade_desk_view(request: Request):
    return templates.TemplateResponse("admin/trade_desk/index.html", {"request": request, "active_tab": "marketplace"})

@router.get("/payments", response_class=HTMLResponse)
async def admin_payments_view(request: Request):
    return templates.TemplateResponse("admin/payments/index.html", {"request": request, "active_tab": "finance"})
