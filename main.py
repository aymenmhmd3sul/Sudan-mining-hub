from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.gold_service import get_price

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/status")
def api_status():
    return {"status": "running"}

@app.get("/api/gold")
def api_gold():
    try:
        return {"gold": get_price()}
    except:
        return {"gold": 0}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        gold = get_price()
    except:
        gold = 0

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "gold": gold,
        "status": "running"
    })

