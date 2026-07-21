from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base

from app.routers import (
    finance,
    market,
    admin_market,
    admin_finance,
    admin_mining,
    admin_system,
    admin_trade_bank,
    admin_escrow_disputes,
    web,
    auth,
    users,
    marketplace,
    mining_sites,
    negotiation,
    negotiation_ws,
    chat,
    communication,
    payments,
    opportunities,
    trade_desk,
    services,
    admin,
    admin_views,
    admin_users,
    admin_control,
    admin_center,
    admin_modules,
    admin_negotiation,
    admin_negotiation_actions,
    admin_negotiation_details,
    admin_negotiation_page,
    web_auth,
    views,
    offers,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sudan Mining Hub API",
    version="3.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

routers = [
    finance.router,
    market.router,
    admin_market.router,
    admin_finance.router,
    admin_mining.router,
    admin_system.router,
    admin_trade_bank.router,
    admin_escrow_disputes.router,
    web.router,
    auth.router,
    users.router,
    marketplace.router,
    mining_sites.router,
    negotiation.router,
    negotiation_ws.router,
    chat.router,
    communication.router,
    payments.router,
    opportunities.router,
    trade_desk.router,
    services.router,
    admin.router,
    admin_views.router,
    admin_users.router,
    admin_control.router,
    admin_center.router,
    admin_modules.router,
    admin_negotiation.router,
    admin_negotiation_actions.router,
    admin_negotiation_details.router,
    admin_negotiation_page.router,
    web_auth.router,
    views.router,
    offers.router,
]

for router in routers:
    app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "message": "Welcome to Sudan Mining Hub",
        "status": "running",
        "version": "3.0.0"
    }


# --- Root & Legacy Compatibility Redirects ---
@app.get('/login', include_in_schema=False)
def redirect_login():
    return RedirectResponse(url='/auth/login')

@app.get('/dashboard', include_in_schema=False)
def redirect_dashboard():
    return RedirectResponse(url='/admin/dashboard')

@app.get('/admin', include_in_schema=False)
def redirect_admin_root():
    return RedirectResponse(url='/admin/dashboard')

@app.get('/admin/operations/negotiation-room', include_in_schema=False)
def redirect_admin_neg_room():
    return RedirectResponse(url='/admin/negotiation')



# --- Legacy Router Aliases ---
@app.get('/admin-portal/finance/{path:path}', include_in_schema=False)
def redirect_legacy_finance(path: str):
    return RedirectResponse(url='/admin/finance')

@app.get('/admin-portal/users/{path:path}', include_in_schema=False)
def redirect_legacy_users(path: str):
    return RedirectResponse(url='/admin/users')

@app.get('/admin-portal/subscriptions/{path:path}', include_in_schema=False)
def redirect_legacy_subs(path: str):
    return RedirectResponse(url='/admin/users')



@app.get('/admin/api/dashboard-data', include_in_schema=False)
def redirect_admin_dash_data():
    return RedirectResponse(url='/admin-portal/api/dashboard-data')


@app.get("/")
def read_root():
    # توجيه الزائر مباشرة إلى بوابة الدخول (Gateway / Login)
    # بناءً على الهيكل، قد يكون المسار /login أو /auth/login أو مسار بوابة خاص
    return RedirectResponse(url="/login", status_code=303)
