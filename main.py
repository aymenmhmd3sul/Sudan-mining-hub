from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"

def get_price():
    try:
        r = requests.get(BINANCE_URL, timeout=3)
        return float(r.json()["price"])
    except:
        return 2333.0


# 🧠 نظام تسجيل النوافذ
WINDOWS = {
    "orders": {
        "title": "📦 الطلبات",
        "desc": "إدارة الطلبات المفتوحة والطلبات الجديدة"
    },
    "traders": {
        "title": "👤 التجار",
        "desc": "شبكة التجار المسجلين في المنصة"
    },
    "mining": {
        "title": "⛏️ التعدين",
        "desc": "معدات وعمليات التعدين"
    },
    "ads": {
        "title": "📢 الإعلانات",
        "desc": "إدارة الإعلانات والعروض"
    },
    "subscription": {
        "title": "💳 الاشتراك",
        "desc": "خطط الاشتراك والدفع"
    }
}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    price = get_price()

    cards = ""
    for key, w in WINDOWS.items():
        cards += f"""
        <div class="card" onclick="openWindow('{key}')">
            {w['title']}
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    padding:12px;
}}

.header {{
    text-align:center;
    padding:15px;
    background:#111827;
    border-radius:10px;
}}

.price {{
    text-align:center;
    font-size:45px;
    color:#22c55e;
    margin:15px 0;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
    gap:12px;
}}

.card {{
    background:#1f2937;
    padding:18px;
    border-radius:12px;
    text-align:center;
    cursor:pointer;
    transition:0.2s;
}}

.card:hover {{
    transform:scale(1.05);
    background:#273449;
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
    margin:20% auto;
    padding:20px;
    width:85%;
    border-radius:12px;
    text-align:center;
}}

.close {{
    float:left;
    cursor:pointer;
    color:red;
    font-size:20px;
}}
</style>
</head>

<body>

<div class="container">

<div class="header">🟡 Sudan Mining Hub</div>

<div class="price">{price:.2f} USD</div>

<div class="grid">
{cards}
</div>

</div>

<div class="modal" id="modal">
<div class="modal-content">
<span class="close" onclick="closeModal()">✖</span>
<h3 id="title"></h3>
<p id="desc"></p>
</div>
</div>

<script>

const WINDOWS = {WINDOWS};

function openWindow(key){{
    document.getElementById("title").innerText = WINDOWS[key].title;
    document.getElementById("desc").innerText = WINDOWS[key].desc;
    document.getElementById("modal").style.display = "block";
}}

function closeModal(){{
    document.getElementById("modal").style.display = "none";
}}
</script>

</body>
</html>
"""
