from app.routes.admin.escrow import router as escrow_router
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.routers import admin_views

try:
    from app.routers import admin_negotiation_page, admin_negotiation_actions, admin_negotiation_details
except ImportError:
    admin_negotiation_page = None
    admin_negotiation_actions = None
    admin_negotiation_details = None

try:
    from app.routers import auth
except ImportError:
    auth = None

app = FastAPI(title="Sudan Mining Hub")

if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    if os.path.exists("app/templates/index.html"):
        return templates.TemplateResponse(request=request, name="index.html")
    elif os.path.exists("app/templates/gateway.html"):
        return templates.TemplateResponse(request=request, name="gateway.html")
    return HTMLResponse("<h2>مرحباً بك في منصة سودان مايننج هاب</h2>")

@app.get("/login", response_class=HTMLResponse)
async def serve_login_page(request: Request):
    if os.path.exists("app/templates/auth/login.html"):
        return templates.TemplateResponse(request=request, name="auth/login.html")
    elif os.path.exists("app/templates/login.html"):
        return templates.TemplateResponse(request=request, name="login.html")
    return templates.TemplateResponse(request=request, name="admin/dashboard.html")

if auth and hasattr(auth, 'router'):
    app.include_router(auth.router)

app.include_router(admin_views.router)

if admin_negotiation_page and hasattr(admin_negotiation_page, 'router'):
    app.include_router(admin_negotiation_page.router)

if admin_negotiation_actions and hasattr(admin_negotiation_actions, 'router'):
    app.include_router(admin_negotiation_actions.router)

# disabled conflicting details router

app.include_router(escrow_router)
