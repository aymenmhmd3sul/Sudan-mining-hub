from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.db import engine
from app.core.security import get_password_hash

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.admin import router as admin_router
from app.routers.admin_views import router as admin_views_router
from app.routers.market import router as market_router
from app.routers.negotiation import router as negotiation_router
from app.routers.communication import router as communication_router
from app.routers.chat import router as chat_router
from app.routers.payments import router as payments_router
from app.routers.trade_desk import router as trade_desk_router
from app.routers.opportunities import router as opportunities_router

app = FastAPI(
    title="Sudan Mining Hub API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core
app.include_router(auth_router)
app.include_router(users_router)

# Business Modules
app.include_router(admin_router)
app.include_router(admin_views_router)
app.include_router(market_router)
app.include_router(negotiation_router)
app.include_router(communication_router)
app.include_router(chat_router)
app.include_router(payments_router)
app.include_router(trade_desk_router)
app.include_router(opportunities_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Sudan Mining Hub API",
        "status": "running",
        "version": "2.0.0"
    }

@app.on_event("startup")
def sync_admin_account_clean():
    try:
        clean_pass = "SudanMining@2026".strip()
        new_hash = get_password_hash(clean_pass)

        with engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text(
                        """
                        UPDATE users
                        SET password_hash=:hash,
                            role='ADMIN',
                            status='ACTIVE'
                        WHERE LOWER(TRIM(email))='aymen.mhmd3@gmail.com'
                        """
                    ),
                    {"hash": new_hash},
                )

        print("✅ [BOOT_SUCCESS] Admin synchronized successfully.")

    except Exception as e:
        print("⚠️ [BOOT_ERROR]", e)
