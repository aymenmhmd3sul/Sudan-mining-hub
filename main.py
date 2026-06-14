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
        return 2333.0


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

.container {{
    max-width:1000px;
    margin:auto;
    padding:15px;
}}

.header {{
    text-align:center;
    padding:18px;
    background:#111827;
    border-radius:12px;
}}

.price {{
    text-align:center;
    font-size:50px;
    color:#22c55e;
    margin:20px 0;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
    gap:12px;
}}

.card {{
    background:#1f2937;
    padding:20px;
    border-radius:12px;
    text-align:center;
    cursor:pointer;
    transition:0.2s;
}}

.card:hover {{
    transform:scale(1.05);
    background:#2b3a52;
}}

.modal {{
    display:none;
    position:fixed;
    top:0;left:0;
    width:100%;height:100%;
    background:rgba(0,0,0,0.7);
}}

.modal-content {{
    background:#111827;
    margin:15% auto;
    padding:20px;
    width:80%;
    border-radius:12px;
    text-align:center;
}}

.close {{
    color:red;
    float:left;
    font-size:22px;
    cursor:pointer;
}}
</style>

</head>

<body>

<div class="container">

<div class="header">🟡 Sudan Mining Hub</div>

<div class="price">{price}</div>

<div class="grid">

<div class="card">📦 الطلبات</div>
<div class="card">👤 التجار</div>
<div class="card">⛏️ التعدين</div>
<div class="card">📢 الإعلانات</div>
<div class="card">💳 الاشتراك</div>

</div>

</div>

</body>
</html>
"""
