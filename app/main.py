from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base

from app.routers import (
    finance,
    market,
    admin_market,
    admin_finance,
    admin_mining,
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
