from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.services.templates import templates
from app.services.i18n import get_translations, translate
from app.translations import TRANSLATIONS
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.services.templates import templates
from app.services.i18n import get_translations, translate
from app.translations import TRANSLATIONS
from app.routers import (
    admin_subscription_plans,
    admin_views, auth, opportunities, chat, payments, admin,
    web, web_auth, admin_mining, mining_sites,
    admin_subscriptions, views, language, merchant_views, marketplace, showcase, negotiation
)
app = FastAPI(title="Sudan Mining Hub")


@app.middleware("http")
async def language_middleware(request: Request, call_next):
    lang = request.cookies.get("language", "ar")

    if lang not in ["ar", "en"]:
        lang = "ar"

    request.state.lang = lang
    request.state.direction = "rtl" if lang == "ar" else "ltr"
    request.state.translations = TRANSLATIONS.get(lang, TRANSLATIONS["ar"])

    response = await call_next(request)
    return response


# الملفات الاستاتيكية والقوالب
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# استدعاء الموجه الشامل للواجهات (بدون مضاعفة prefix)
app.include_router(admin_views.router)
app.include_router(merchant_views.router)
app.include_router(views.router)
app.include_router(web.router)
app.include_router(web_auth.router)
app.include_router(language.router)

# موجهات API الخلفية
app.include_router(auth.router, prefix="/api/auth", tags=["المصادقة"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["الفرص"])
app.include_router(chat.router, prefix="/api/chat", tags=["المحادثات"])
app.include_router(payments.router, prefix="/api/payments", tags=["المدفوعات"])
app.include_router(admin.router, prefix="/api/admin", tags=["الإدارة"])
app.include_router(admin_mining.router)
app.include_router(admin_subscriptions.router)
app.include_router(admin_subscription_plans.router)
app.include_router(mining_sites.router)
app.include_router(marketplace.router)
app.include_router(showcase.router)
app.include_router(negotiation.router)

@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/gateway")
