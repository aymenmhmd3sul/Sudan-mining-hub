from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import traceback

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "status": "running"
        })
    except Exception as e:
        return HTMLResponse(str(traceback.format_exc()), status_code=500)

