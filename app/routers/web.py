from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/gateway", response_class=HTMLResponse)
async def gateway(request: Request):
    return templates.TemplateResponse("gateway.html", {"request": request})
