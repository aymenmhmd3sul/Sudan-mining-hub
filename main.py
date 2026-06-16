from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

def get_price():
    try:
        r = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT",
            timeout=5
        )
        return round(float(r.json()["price"]), 2)
    except:
        return 0.0

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/gold")
def api_gold():
    return {"gold": get_price()}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    gold = get_price()
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Sudan Mining Hub</title>
    <meta charset="utf-8">
    <style>
        body {{ background:#0f172a; color:white; font-family:Arial; padding:20px; }}
        .box {{ background:#1e293b; padding:20px; margin:10px 0; border-radius:12px; }}
        button {{ padding:10px; background:#22c55e; border:none; color:white; border-radius:8px; cursor:pointer; }}
        button:hover {{ background:#16a34a; }}
    </style>
</head>
<body>
    <h1>🟡 Sudan Mining Hub</h1>
    <div class="box">
        <h3>Gold Price</h3>
        <p style="font-size:24px">{gold} USD</p>
    </div>
    <div class="box">
        <h3>Status</h3>
        <p>✅ Running</p>
    </div>
    <div class="box">
        <button onclick="alert('✅ زر يعمل بشكل صحيح!')">Test Button</button>
    </div>
</body>
</html>
"""
# force rebuild
