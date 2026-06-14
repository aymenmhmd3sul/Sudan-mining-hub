from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="Sudan Mining Hub API")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/api/v1/gold-price")
def gold_price():
    try:
        r = requests.get("https://api.metals.live/v1/spot/gold", timeout=5)
        data = r.json()
        return {"gold_usd": data[0]["price"]}
    except:
        return {"gold_usd": 0}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        r = requests.get("https://api.metals.live/v1/spot/gold", timeout=5)
        data = r.json()
        price = data[0]["price"]
    except:
        price = 0

    return templates.TemplateResponse("index.html", {
        "request": request,
        "gold_price": price
    })

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/market/items")
def get_items():
    return {
        "count": 1,
        "data": [{"id": 1, "name": "gold"}]
    }
