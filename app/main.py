from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, negotiation, marketplace, services, admin

app = FastAPI(
    title="Sudan Mining Hub API",
    description="منصة المعاملات الشاملة لأصول التعدين في السودان - نسخة 2026",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(negotiation.router, prefix="/api/negotiation")
app.include_router(marketplace.router, prefix="/api/assets")
app.include_router(services.router, prefix="/api/services")
app.include_router(admin.router, prefix="/api/admin")

@app.get("/")
def read_root():
    return {"status": "online", "platform": "Sudan Mining Hub"}
