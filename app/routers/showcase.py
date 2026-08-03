from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.data.showcase_data import SHOWCASE_DATA

router = APIRouter(prefix="/showcase", tags=["Showcase"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{section}")
async def showcase_section(request: Request, section: str):
    data = SHOWCASE_DATA.get(section, SHOWCASE_DATA['equipment'])
    return templates.TemplateResponse('showcase/section.html', {
        'request': request,
        'title': request.state.translations.get(data.get('title_key'), data.get('title')),
        'items': data['items'],
        'lang': request.state.lang,
        'direction': request.state.direction,
        't': request.state.translations
    })
