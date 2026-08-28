from app.routers import legal
from app.routes.admin.escrow import router as escrow_router
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.translations import TRANSLATIONS
from fastapi.responses import HTMLResponse

from app.routers import merchant_views, buyer_views, agent_views, communication
from app.routers import admin_views
from app.routers import admin_users
from app.routers import language, web, negotiation, marketplace, market, mining_sites
from app.api.routers.search import router as search_router

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

@app.middleware("http")
async def language_middleware(request: Request, call_next):
    lang = request.cookies.get("language", "ar")

    if lang not in ("ar", "en"):
        lang = "ar"

    request.state.lang = lang
    request.state.direction = "rtl" if lang == "ar" else "ltr"
    request.state.translations = TRANSLATIONS.get(
        lang,
        TRANSLATIONS["ar"]
    )

    response = await call_next(request)
    return response



if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

from app.services.templates import templates, template_context

@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    if os.path.exists("app/templates/index.html"):
        return templates.TemplateResponse(request=request, name="index.html", context=template_context(request))
    elif os.path.exists("app/templates/gateway.html"):
        return templates.TemplateResponse(request=request, name="gateway.html", context=template_context(request))
    return HTMLResponse("<h2>مرحباً بك في منصة سودان مايننج هاب</h2>")

@app.get("/login", response_class=HTMLResponse)
async def serve_login_page(request: Request):
    if os.path.exists("app/templates/auth/login.html"):
        return templates.TemplateResponse(request=request, name="auth/login.html", context=template_context(request))
    elif os.path.exists("app/templates/login.html"):
        return templates.TemplateResponse(request=request, name="login.html", context=template_context(request))
    return templates.TemplateResponse(request=request, name="admin/dashboard.html")

@app.get("/register", response_class=HTMLResponse)
async def serve_register_page(request: Request):
    if os.path.exists("app/templates/register.html"):
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context=template_context(request),
        )
    return HTMLResponse(
        "<h2>صفحة التسجيل غير متاحة حالياً</h2>",
        status_code=404
    )

if auth and hasattr(auth, 'router'):
    app.include_router(auth.router)


app.include_router(admin_views.router)
app.include_router(merchant_views.router)
app.include_router(communication.router)
app.include_router(buyer_views.router)
app.include_router(agent_views.router)
app.include_router(admin_users.router)
app.include_router(language.router)
app.include_router(web.router)
app.include_router(negotiation.router)
app.include_router(legal.router)
app.include_router(marketplace.router)
app.include_router(market.router)
app.include_router(mining_sites.router)

if admin_negotiation_page and hasattr(admin_negotiation_page, 'router'):
    app.include_router(admin_negotiation_page.router)

if admin_negotiation_actions and hasattr(admin_negotiation_actions, 'router'):
    app.include_router(admin_negotiation_actions.router)

# disabled conflicting details router

app.include_router(escrow_router)
app.include_router(search_router)

# Render / platform health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

