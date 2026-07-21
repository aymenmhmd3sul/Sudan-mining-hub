from fastapi import APIRouter, Request, Depends
from app.core.dependencies import verify_admin_token
from app.models.user import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["Admin Center Views"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, current_user: User = Depends(verify_admin_token)):
    user_data = getattr(request.state, 'user', None)
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={"user": user_data, "active_tab": "dashboard"}
    )
@router.get("/marketplace", response_class=HTMLResponse)
async def admin_marketplace(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/marketplace/index.html", context={"request": request}

@router.get("/mining", response_class=HTMLResponse)
async def admin_mining(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/mining/index.html", context={"request": request}


# --- قسم المعدات والخدمات (Equipment & Services) ---
@router.get("/equipment", response_class=HTMLResponse)
async def admin_equipment(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/equipment/index.html")

@router.get("/rentals", response_class=HTMLResponse)
async def admin_rentals(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/rentals/index.html")

@router.get("/service_providers", response_class=HTMLResponse)
async def admin_service_providers(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/services/index.html")

@router.get("/logistics", response_class=HTMLResponse)
async def admin_logistics(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/logistics/index.html")

@router.get("/transport", response_class=HTMLResponse)
async def admin_transport(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/transport/index.html")

@router.get("/warehouses", response_class=HTMLResponse)
async def admin_warehouses(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/warehouses/index.html")

@router.get("/maintenance", response_class=HTMLResponse)
async def admin_maintenance(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/maintenance/index.html")

@router.get("/finance", response_class=HTMLResponse)
async def admin_finance(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/finance/index.html", context={"request": request}

@router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/users/index.html", context={"request": request}

@router.get("/communications", response_class=HTMLResponse)
async def admin_communications(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/communications/index.html", context={"request": request}

@router.get("/content", response_class=HTMLResponse)
async def admin_content(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/content/index.html", context={"request": request}

@router.get("/reports", response_class=HTMLResponse)
async def admin_reports(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/reports/index.html", context={"request": request}

@router.get("/administration", response_class=HTMLResponse)
async def admin_administration(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/administration/index.html", context={"request": request}

@router.get("/security", response_class=HTMLResponse)
async def admin_security(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/security/index.html", context={"request": request}

@router.get("/identity", response_class=HTMLResponse)
async def admin_identity_view(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/identity/index.html")

@router.get("/audit", response_class=HTMLResponse)
async def admin_audit_view(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/audit/index.html")

@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics_view(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/analytics/index.html")

@router.get("/trade_desk", response_class=HTMLResponse)
async def admin_trade_desk_view(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/trade_desk/index.html")

@router.get("/payments", response_class=HTMLResponse)
async def admin_payments_view(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/payments/index.html")


# --- قسم العمليات المتقدمة (Advanced Operations - 9 Subsections) ---
@router.get("/negotiations", response_class=HTMLResponse)
async def admin_negotiations(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/negotiations/index.html")

@router.get("/trade_desk", response_class=HTMLResponse)
async def admin_trade_desk(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/trade_desk/index.html")

@router.get("/offers", response_class=HTMLResponse)
async def admin_offers(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/offers/index.html")

@router.get("/payments", response_class=HTMLResponse)
async def admin_payments(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/payments/index.html")

@router.get("/opportunities", response_class=HTMLResponse)
async def admin_opportunities(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/opportunities/index.html")

@router.get("/services", response_class=HTMLResponse)
async def admin_services(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/services/index.html")

@router.get("/identity", response_class=HTMLResponse)
async def admin_identity(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/identity/index.html")

@router.get("/audit", response_class=HTMLResponse)
async def admin_audit(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/audit/index.html")

@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics(request: Request, current_user: User = Depends(verify_admin_token)):
    return templates.TemplateResponse(request=request, name="admin/analytics/index.html")
