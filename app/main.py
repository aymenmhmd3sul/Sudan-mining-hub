from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.admin import router as admin_router
from routers.buyer import router as buyer_router
from routers.seller import router as seller_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(buyer_router)
app.include_router(seller_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "system running"}
