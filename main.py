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
    return HTMLResponse("""
<html dir="rtl"><body style="background:#0f172a;color:white;font-family:Arial;padding:20px">
<h1 style="font-size:28px">سياسة المنصة</h1>
<p style="font-size:18px">هذه منصة لعرض أسعار الذهب والمعلومات السوقية.</p>
</body></html>
""")

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
font-size:26px;
font-weight:bold;
}}

.lang {{
position:absolute;
left:10px;
top:10px;
background:#1f2937;
padding:6px 10px;
border-radius:8px;
font-size:12px;
cursor:pointer;
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
border-radius:10px;
text-align:center;
cursor:pointer;
font-size:16px;
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

.policy-link {{
font-size:18px;
color:#38bdf8;
}}
</style>

<script>

let lang = "ar";

function toggleLang(){{
lang = (lang==="ar") ? "en" : "ar";

document.getElementById("title").innerText =
(lang==="ar") ? "🟡 منصة السودان للتعدين" : "🟡 Sudan Mining Hub";

document.getElementById("c1").innerText = (lang==="ar") ? "📦 الطلبات" : "Orders";
document.getElementById("c2").innerText = (lang==="ar") ? "👤 التجار" : "Traders";
document.getElementById("c3").innerText = (lang==="ar") ? "⛏️ التعدين" : "Mining";
document.getElementById("c4").innerText = (lang==="ar") ? "📢 الإعلانات" : "Ads";
document.getElementById("c5").innerText = (lang==="ar") ? "💳 الاشتراك" : "Subscription";
}}

function showSection(t,x){{
document.getElementById("panel").innerHTML = "<h2>"+t+"</h2><p>"+x+"</p>";
}}

</script>

</head>

<body>

<div class="lang" onclick="toggleLang()">AR | EN</div>

<div class="header" id="title">🟡 منصة السودان للتعدين</div>

<div class="ticker">
🟡 أونصة الذهب: {gold} USD | 🔄 Live
</div>

<div class="grid">

<div class="card" id="c1" onclick="showSection(الطلبات,لا
توجد
طلبات)">📦 الطلبات</div>
<div class="card" id="c2" onclick="showSection(التجار,لا
يوجد
تجار)">👤 التجار</div>
<div class="card" id="c3" onclick="showSection(التعدين,معدات
التعدين)">⛏️ التعدين</div>
<div class="card" id="c4" onclick="showSection(الإعلانات,لا
توجد
إعلانات)">📢 الإعلانات</div>
<div class="card" id="c5" onclick="showSection(الاشتراك,قريباً)">💳 الاشتراك</div>

</div>

<div id="panel" class="panel">
لوحة التحكم
</div>

<div style="text-align:center;margin:10px">
<a class="policy-link" href="/policy">سياسة المنصة</a>
</div>

</body>
</html>
""")

