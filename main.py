from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import subprocess

from services.gold_service import get_price

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except:
        return "no-git"

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/gold")
def api_gold():
    return {"gold": get_price()}

@app.get("/api/status")
def api_status():
    return {"status": "running"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "gold": get_price(),
        "status": "running",
        "commit": get_commit()
    })
