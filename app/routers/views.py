from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Frontend Views"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/home", response_class=HTMLResponse)
async def render_login_gateway(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})

@router.get("/explore", response_class=HTMLResponse)
async def explore_page(request: Request):
    return templates.TemplateResponse("explore.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})


@router.get("/market", response_class=HTMLResponse)
async def market_page(request: Request):
    return templates.TemplateResponse("market.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})


@router.get("/opportunity/{opp_id}", response_class=HTMLResponse)
async def opportunity_details_page(request: Request, opp_id: int):
    return templates.TemplateResponse(
        "opportunity_details.html",
        {"request": request,
            "lang": getattr(request.state, "lang", "ar"),
            "direction": "rtl" if getattr(request.state, "lang", "ar") == "ar" else "ltr", "opp_id": opp_id}
    )



@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations}
    )


@router.get("/visitor", response_class=HTMLResponse)
async def visitor_page(request: Request):
    return templates.TemplateResponse("visitor.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})
