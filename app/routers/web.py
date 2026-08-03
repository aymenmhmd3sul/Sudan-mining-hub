from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/gateway", response_class=HTMLResponse)
async def gateway(request: Request):
    return templates.TemplateResponse("gateway.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})


@router.get("/gateway-v3", response_class=HTMLResponse)
async def gateway_v3(request: Request):
    return templates.TemplateResponse("gateway_v3.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})


@router.get("/gateway-v2", response_class=HTMLResponse)
async def gateway_v2(request: Request):
    return templates.TemplateResponse("gateway_v2_stable.html", {"request": request, "lang": request.state.lang, "direction": request.state.direction, "t": request.state.translations})
