from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/admin",
    tags=["Admin Negotiation Page"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/negotiation-room/{room_id}", response_class=HTMLResponse)
def negotiation_room_page(request: Request, room_id: int):
    return templates.TemplateResponse(
        "admin/negotiation_room/index.html",
        {
            "request": request,
            "room_id": room_id
        }
    )
