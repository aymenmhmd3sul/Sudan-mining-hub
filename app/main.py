from fastapi import FastAPI
from app.api.routers.assets import router as asset_router
from app.api.routers.reports import router as report_router
from app.api.routers.views import router as web_views_router
from app.api.routers.commercial import router as commercial_router

app = FastAPI(
    title="Mining Hub API",
    description="المنصة الرقمية الإقليمية لإدارة وتداول الأصول والموارد التعدينية في السودان",
    version="1.0.0"
)

# تضمين كافة المسارات والمحركات (المبيعات، الأصول، البلاغات، الواجهات)
app.include_router(asset_router)
app.include_router(report_router)
app.include_router(web_views_router)
app.include_router(commercial_router)

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "healthy",
        "project": "Mining Hub",
        "region": "Sudan",
        "message": "المحرك التجاري ومركز القيادة لـ Sudan Mining Hub جاهز ومكتمل بالكامل"
    }
