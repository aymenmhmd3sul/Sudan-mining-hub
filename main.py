from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"

def get_price():
    try:
        r = requests.get(BINANCE_URL, timeout=5)
        return float(r.json()["price"])
    except:
        return 2335.0


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/gold-price")
def gold_price():
    return {"status": "success", "gold_usd": get_price()}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    price = get_price()

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Sudan Mining Hub</title>

<style>
body {{
    margin:0;
    font-family: Arial;
    background:#0b1220;
    color:white;
}}

.header {{
    background:#111827;
    padding:15px;
    text-align:center;
    font-size:20px;
    font-weight:bold;
}}

.price {{
    text-align:center;
    font-size:60px;
    color:#22c55e;
    margin-top:20px;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:15px;
    padding:20px;
}}

.card {{
    background:#1f2937;
    padding:20px;
    border-radius:12px;
    text-align:center;
}}

.footer {{
    text-align:center;
    padding:15px;
    margin-top:20px;
    background:#111827;
    color:#94a3b8;
}}
</style>

</head>

<body>

<div class="header">🟡 Sudan Mining Hub Dashboard</div>

<div class="price">{price}</div>

<div class="grid">

    <div class="card">
        <h3>📦 Orders</h3>
        <p>Open Buy/Sell Requests</p>
    </div>

    <div class="card">
        <h3>👤 Traders</h3>
        <p>Active Network</p>
    </div>

    <div class="card">
        <h3>⛏️ Mining</h3>
        <p>Equipment & Operations</p>
    </div>

    <div class="card">
        <h3>📢 Ads</h3>
        <p>Market Promotions</p>
    </div>

    <div class="card">
        <h3>💳 Subscription</h3>
        <p>3000 SDG / Month</p>
    </div>

</div>

<div class="footer">
© Sudan Mining Hub | Live Market System
</div>

</body>
</html>
"""
