from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/merchant", tags=["Merchant"])

templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def merchant_dashboard(request: Request):
    return templates.TemplateResponse(
        "merchant/dashboard/index.html",
        {
            "request": request,
            "lang": "ar"
        }
    )
