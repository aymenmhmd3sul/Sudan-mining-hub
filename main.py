from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

def price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5)
        return round(float(r.json()["price"]),2)
    except:
        return 2330.0

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    gold = price()

    return HTMLResponse(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sudan Mining Hub</title>

<style>

body {{
margin:0;
font-family:Arial;
background:#0f172a;
color:white;
-webkit-user-select:none;
user-select:none;
touch-action:manipulation;
}}

.header {{
background:#111827;
padding:16px;
text-align:center;
font-size:24px;
font-weight:bold;
}}

.ticker {{
background:#1e293b;
padding:10px;
text-align:center;
}}

.grid {{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
padding:12px;
}}

.card {{
background:#1f2937;
padding:18px;
border-radius:12px;
text-align:center;
font-size:16px;
cursor:pointer;

-webkit-tap-highlight-color:transparent;
touch-action:manipulation;
}}

.card:active {{
transform:scale(0.96);
background:#374151;
}}

.panel {{
margin:12px;
padding:18px;
background:#111827;
border-radius:10px;
min-height:120px;
}}

.footer {{
text-align:center;
padding:15px;
background:#111827;
}}

</style>

<script>

function showSection(t,x){{
document.getElementById("panel").innerHTML =
"<h2>"+t+"</h2><p>"+x+"</p>";
}}

</script>

</head>

<body>

<div class="header">🟡 Sudan Mining Hub</div>

<div class="ticker">
🟡 أونصة الذهب: {gold} USD | Live
</div>

<div class="grid">

<div class="card" ontouchstart="showSection(الطلبات,لا
توجد
طلبات)" onclick="showSection(الطلبات,لا
توجد
طلبات)">📦 الطلبات</div>
<div class="card" ontouchstart="showSection(التجار,لا
يوجد
تجار)" onclick="showSection(التجار,لا
يوجد
تجار)">👤 التجار</div>
<div class="card" ontouchstart="showSection(التعدين,معدات
التعدين)" onclick="showSection(التعدين,معدات
التعدين)">⛏️ التعدين</div>
<div class="card" ontouchstart="showSection(الإعلانات,لا
توجد
إعلانات)" onclick="showSection(الإعلانات,لا
توجد
إعلانات)">📢 الإعلانات</div>
<div class="card" ontouchstart="showSection(الاشتراك,قريباً)" onclick="showSection(الاشتراك,قريباً)">💳 الاشتراك</div>

</div>

<div id="panel" class="panel">
اضغط على أي قسم
</div>

</body>
</html>
""")

