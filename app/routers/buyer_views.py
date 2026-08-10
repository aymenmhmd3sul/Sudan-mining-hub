from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.templates import templates, template_context
from app.core.dependencies import require_buyer
from fastapi import Depends

router = APIRouter(
    prefix="/buyer",
    tags=["Buyer"],
    dependencies=[Depends(require_buyer)]
)


def render(request: Request, page: str):
    return templates.TemplateResponse(
        request=request,
        name=f"buyer/{page}/index.html",
        context=template_context(request)
    )


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def buyer_dashboard(request: Request):
    return render(request, "dashboard")


@router.get("/profile", response_class=HTMLResponse)
async def buyer_profile(request: Request):
    return render(request, "profile")


@router.get("/opportunities", response_class=HTMLResponse)
async def buyer_opportunities(request: Request):
    return render(request, "opportunities")


@router.get("/requests", response_class=HTMLResponse)
async def buyer_requests(request: Request):
    return render(request, "requests")


@router.get("/negotiation", response_class=HTMLResponse)
async def buyer_negotiation(request: Request):
    return render(request, "negotiation")


@router.get("/deals", response_class=HTMLResponse)
async def buyer_deals(request: Request):
    return render(request, "deals")


@router.get("/finance", response_class=HTMLResponse)
async def buyer_finance(request: Request):
    return render(request, "finance")
