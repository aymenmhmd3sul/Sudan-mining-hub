from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/legal", tags=["Legal"])

from app.services.templates import templates


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
