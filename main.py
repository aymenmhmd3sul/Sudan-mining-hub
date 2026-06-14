from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from services.gold_service import get_gold_price
from services.market_core import get_items, add_item

app = FastAPI(title="Sudan Mining Hub API")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/api/v1/gold-price")
def gold_price():
    price = get_gold_price()
    return {"status": "success", "gold_usd": float(price)}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    price = get_gold_price()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "gold_price": float(price),
        "status": "live"
    })

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/market/items")
def market_items():
    return {"status": "success", "data": get_items()}
