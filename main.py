from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="Sudan Mining Hub API")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/market/items")
def get_items():
    return {
        "count": 1,
        "data": [
            {"id": 1, "name": "gold"}
        ]
    }
