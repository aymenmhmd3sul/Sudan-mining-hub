from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["Admin Center Views"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", context={"request": request})

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
