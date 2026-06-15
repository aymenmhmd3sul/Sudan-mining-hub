from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        gold = 2400
    except:
        gold = 0

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "gold": gold,
        "status": "running"
    })
