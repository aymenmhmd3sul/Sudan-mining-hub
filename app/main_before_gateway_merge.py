from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import finance, market, admin_market, web
from app.database import engine, Base

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sudan Mining Hub API")

# ربط المجلد الثابت
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# تضمين المسارات
app.include_router(finance.router)
app.include_router(market.router)
app.include_router(admin_market.router)
app.include_router(web.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Sudan Mining Hub API"}
