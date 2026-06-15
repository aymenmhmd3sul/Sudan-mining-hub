from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_price():
    try:
        r = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT",
            timeout=5
        )
        return round(float(r.json()["price"]), 2)
    except:
        return 2330.0

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    gold = get_price()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "gold": gold
    })
