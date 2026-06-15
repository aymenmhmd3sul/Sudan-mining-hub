from fastapi import FastAPI
from services.gold_service import get_price

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "build": "TEST-123"}

@app.get("/api/status")
def api_status():
    return {"status": "running"}

@app.get("/api/gold")
def api_gold():
    return {"gold": get_price()}

@app.get("/dashboard")
def dashboard():
    return {"status": "running", "gold": get_price()}

