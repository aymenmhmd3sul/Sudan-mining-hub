from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/dashboard")
def dashboard():
    return {"status": "dashboard reached successfully"}

