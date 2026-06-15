from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.gold_service import get_price

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# --------------------
# Health Check
# --------------------
@app.get("/")
def root():
    return {"status": "ok"}


# --------------------
# API LAYER
# --------------------
@app.get("/api/gold")
def api_gold():
    try:
        return {"gold": get_price()}
    except Exception:
        return {"gold": None}


@app.get("/api/status")
def api_status():
    return {"status": "running"}


# --------------------
# UI LAYER
# --------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        gold = get_price()
    except Exception:
        gold = None

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "gold": gold,
        "status": "running"
    })
