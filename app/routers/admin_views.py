from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.user import User
from app.core.security import verify_admin_token

router = APIRouter(prefix="/admin", tags=["Admin Views"])
templates = Jinja2Templates(directory="app/templates")

# --- لوحة القيادة والتعدين ---
@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={"active_tab": "dashboard"})

@router.get("/mining", response_class=HTMLResponse)
async def admin_mining(request: Request):
    return templates.TemplateResponse(request=request, name="admin/mining/index.html", context={"active_tab": "mining"})

@router.get("/concessions", response_class=HTMLResponse)
async def admin_concessions(request: Request):
    return templates.TemplateResponse(request=request, name="admin/concessions/index.html", context={"active_tab": "mining"})

@router.get("/minerals", response_class=HTMLResponse)
async def admin_minerals(request: Request):
    return templates.TemplateResponse(request=request, name="admin/minerals/index.html", context={"active_tab": "mining"})

# --- العمليات المتقدمة ---
@router.get("/negotiations", response_class=HTMLResponse)
async def admin_negotiations(request: Request):
    return templates.TemplateResponse(request=request, name="admin/negotiations/index.html", context={"active_tab": "operations"})

@router.get("/trade_desk", response_class=HTMLResponse)
async def admin_trade_desk(request: Request):
    return templates.TemplateResponse(request=request, name="admin/trade_desk/index.html", context={"active_tab": "operations"})

@router.get("/offers", response_class=HTMLResponse)
async def admin_offers(request: Request):
    return templates.TemplateResponse(request=request, name="admin/offers/index.html", context={"active_tab": "operations"})

@router.get("/payments", response_class=HTMLResponse)
async def admin_payments(request: Request):
    return templates.TemplateResponse(request=request, name="admin/payments/index.html", context={"active_tab": "operations"})

@router.get("/opportunities", response_class=HTMLResponse)
async def admin_opportunities(request: Request):
    return templates.TemplateResponse(request=request, name="admin/opportunities/index.html", context={"active_tab": "operations"})

@router.get("/services", response_class=HTMLResponse)
async def admin_services(request: Request):
    return templates.TemplateResponse(request=request, name="admin/services/index.html", context={"active_tab": "operations"})

@router.get("/identity", response_class=HTMLResponse)
async def admin_identity(request: Request):
    return templates.TemplateResponse(request=request, name="admin/identity/index.html", context={"active_tab": "operations"})

@router.get("/audit", response_class=HTMLResponse)
async def admin_audit(request: Request):
    return templates.TemplateResponse(request=request, name="admin/audit/index.html", context={"active_tab": "operations"})

@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics(request: Request):
    return templates.TemplateResponse(request=request, name="admin/analytics/index.html", context={"active_tab": "operations"})
