from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.gold_service import get_price

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        gold = get_price()
    except Exception:
        gold = None

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "gold": gold
    })
