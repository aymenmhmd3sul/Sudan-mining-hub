from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.services.templates import templates, template_context

router = APIRouter(tags=["Frontend Views"])


@router.get("/", response_class=HTMLResponse)
async def render_login_gateway(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="gateway.html",
        context=template_context(request),
    )


@router.get("/explore", response_class=HTMLResponse)
async def explore_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=template_context(request),
    )
