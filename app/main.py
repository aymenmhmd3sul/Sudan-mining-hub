from app.routers.admin_users import router as admin_users_router
from app.routers.admin_control import router as admin_control_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import auth, market, negotiation
from app.core.security.middleware import AuthMiddleware

app = FastAPI()

app.add_middleware(AuthMiddleware)

app.include_router(auth.router)
app.include_router(market.router)
app.include_router(negotiation.router)

@app.get("/")
def root():
    return {"status": "running"}

app.include_router(admin_users_router)
app.include_router(admin_control_router)
