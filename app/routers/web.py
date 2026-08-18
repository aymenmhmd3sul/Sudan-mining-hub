from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.services.templates import templates, template_context

router = APIRouter()


@router.get("/gateway", response_class=HTMLResponse)
async def gateway(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="gateway.html",
        context=template_context(request),
    )
