from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.services.templates import templates, template_context
from app.core.dependencies import require_agent


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
    dependencies=[Depends(require_agent)],
)


@router.get("/dashboard", response_class=HTMLResponse)
@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def agent_dashboard(
    request: Request,
    current_user=Depends(require_agent),
):
    context = template_context(request)
    context["active_page"] = "dashboard"
    context["agent"] = current_user

    return templates.TemplateResponse(
        "agent/dashboard/index.html",
        context,
    )


@router.get("/profile", response_class=HTMLResponse)
async def agent_profile(
    request: Request,
    current_user=Depends(require_agent),
):
    context = template_context(request)
    context["active_page"] = "profile"
    context["agent"] = current_user

    return templates.TemplateResponse(
        "agent/dashboard/index.html",
        context,
    )
