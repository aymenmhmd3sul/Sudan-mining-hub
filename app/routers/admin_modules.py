from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["Admin Modules"])

templates = Jinja2Templates(directory="app/templates")


modules = [
    "negotiation",
    "trade_desk",
    "offers",
    "payments",
    "opportunities",
    "services",
    "identity",
    "audit",
    "analytics",
]


def create_module_route(module_name):
    async def module_page(request: Request):
        return templates.TemplateResponse(
            f"admin/{module_name}/index.html",
            {
                "request": request,
                "module_name": module_name
            }
        )

    return module_page


for module in modules:
    router.add_api_route(
        f"/{module}",
        create_module_route(module),
        methods=["GET"],
        response_class=HTMLResponse,
        name=f"admin_{module}"
    )
