from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/legal", tags=["Legal"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/{page}", response_class=HTMLResponse)
async def legal_page(request: Request, page: str):
    allowed_pages = [
        "terms",
        "privacy",
        "marketplace",
        "merchant",
        "buyer",
        "escrow",
        "commission",
        "dispute",
        "compliance"
    ]

    if page not in allowed_pages:
        return HTMLResponse("Page not found", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name=f"legal/{page}.html",
        context={}
    )
