from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5)
        return round(float(r.json()["price"]),2)
    except:
        return 2330.0

@app.get("/")
def root():
    return {"status":"ok"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/policy", response_class=HTMLResponse)
def policy():
    return "<html><body style=\"background:#0f172a;color:white;font-family:Arial;padding:20px\"><h1>سياسة المنصة</h1><p>منصة أسعار الذهب فقط.</p></body></html>"

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    gold = get_price()

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
}}

.header {{
background:#111827;
padding:16px;
text-align:center;
font-size:24px;
font-weight:bold;
position:sticky;
top:0;
}}

.ticker {{
background:#1e293b;
padding:10px;
text-align:center;
font-size:14px;
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
border-radius:10px;
text-align:center;
font-size:16px;
cursor:pointer;
}}

.card:active {{
transform:scale(0.98);
}}

.panel {{
margin:10px;
padding:15px;
background:#111827;
border-radius:10px;
min-height:100px;
}}

.footer {{
text-align:center;
padding:12px;
background:#111827;
margin-top:10px;
}}

a {{
color:#38bdf8;
}}
</style>

<script>
function showSection(t,x){{
document.getElementById("panel").innerHTML = "<h3>"+t+"</h3><p>"+x+"</p>";
}}
</script>

</head>

<body>

<div class="header">🟡 Sudan Mining Hub</div>

<div class="ticker">
🟡 أونصة الذهب: {gold} USD | 🔄 Live
</div>

<div class="grid">

<div class="card" onclick="showSection(الطلبات,لا
توجد
طلبات
حالياً)">📦 الطلبات</div>
<div class="card" onclick="showSection(التجار,لا
يوجد
تجار)">👤 التجار</div>
<div class="card" onclick="showSection(التعدين,معدات
التعدين)">⛏️ التعدين</div>
<div class="card" onclick="showSection(الإعلانات,لا
توجد
إعلانات)">📢 الإعلانات</div>
<div class="card" onclick="showSection(الاشتراك,قريباً)">💳 الاشتراك</div>

</div>

<div id="panel" class="panel">
اضغط على أي قسم
</div>

<div class="footer">
<a href="/policy">سياسة المنصة</a>
</div>

</body>
</html>
""")

