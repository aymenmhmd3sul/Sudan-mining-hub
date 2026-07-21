from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Frontend Views"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def render_login_gateway(request: Request):
    # التحقق من وجود توكن الجلسة في الكوكيز
    token = request.cookies.get("access_token") or request.cookies.get("token")
    if token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/admin/dashboard", status_code=302)
        
    return templates.TemplateResponse(
        request=request,
        name="gateway.html"
    )
@router.get("/explore", response_class=HTMLResponse)
async def explore_page(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")
