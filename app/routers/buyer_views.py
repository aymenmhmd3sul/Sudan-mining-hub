from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.services.templates import templates, template_context
from app.core.dependencies import require_buyer


router = APIRouter(
    prefix="/buyer",
    tags=["Buyer"],
    dependencies=[Depends(require_buyer)],
)


@router.get("/dashboard", response_class=HTMLResponse)
@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def buyer_dashboard(
    request: Request,
    current_user=Depends(require_buyer),
):
    context = template_context(request)
    context["active_page"] = "dashboard"
    context["buyer"] = current_user

    return templates.TemplateResponse(
        "buyer/dashboard/index.html",
        context,
    )


@router.get("/profile", response_class=HTMLResponse)
async def buyer_profile(
    request: Request,
    current_user=Depends(require_buyer),
):
    context = template_context(request)
    context["active_page"] = "profile"
    context["buyer"] = current_user

    return templates.TemplateResponse(
        "buyer/dashboard/index.html",
        context,
    )
