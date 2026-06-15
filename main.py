from fastapi import FastAPI, Request
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
    return {"gold": get_price()}

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "gold": get_price(),
        "status": "running"
    })
