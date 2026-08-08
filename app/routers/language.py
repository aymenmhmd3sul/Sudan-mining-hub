from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/language/{lang}")
async def change_language(lang: str, request: Request):
    if lang not in ["ar", "en"]:
        lang = "ar"

    referer = request.headers.get("referer", "/")

    response = RedirectResponse(url=referer)
    response.set_cookie(
        key="language",
        value=lang,
        max_age=60 * 60 * 24 * 365
    )

    return response
