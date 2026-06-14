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
background:#0b1220;
color:white;
user-select:none;
}}

.top {{
position:sticky;
top:0;
background:#111827;
padding:14px;
text-align:center;
font-size:20px;
font-weight:bold;
}}

.lang {{
position:fixed;
top:10px;
left:10px;
background:#1f2937;
padding:6px 10px;
border-radius:8px;
cursor:pointer;
z-index:9999;
}}

.price {{
display:flex;
justify-content:space-between;
padding:10px;
background:#1e293b;
font-size:13px;
}}

.grid {{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
padding:12px;
}}

.card {{
background:#1f2937;
padding:16px;
border-radius:12px;
text-align:center;
cursor:pointer;
}}

.card:active {{
transform:scale(0.97);
}}

.panel {{
margin:12px;
padding:16px;
background:#111827;
border-radius:12px;
min-height:120px;
}}

.footer {{
text-align:center;
padding:14px;
background:#0b1220;
border-top:1px solid #1f2937;
font-size:13px;
}}

a {{
color:#38bdf8;
text-decoration:none;
}}

</style>
</head>

<body>

<div class="lang" id="langBtn">AR/EN</div>

<div class="top" id="title">🟡 منصة السودان للتعدين</div>

<div class="price">
<div id="price">🟡 أونصة الذهب: {gold} USD</div>
<div>LIVE</div>
</div>

<div class="grid">

<div class="card" id="c1">📊 لوحة التحكم</div>
<div class="card" id="c2">💰 الأسعار</div>
<div class="card" id="c3">📦 الطلبات</div>
<div class="card" id="c4">👤 التجار</div>
<div class="card" id="c5">⛏️ التعدين</div>
<div class="card" id="c6">📢 الإعلانات</div>
<div class="card" id="c7">📰 الأخبار</div>
<div class="card" id="c8">💳 الاشتراك</div>
<div class="card" id="c9">📜 سياسة المنصة</div>

</div>

<div id="panel" class="panel">اضغط على أي قسم</div>

<div class="footer">
Sudan Mining Hub
</div>

<script>

let lang = "ar";

const labels = {
ar: ["لوحة التحكم","الأسعار","الطلبات","التجار","التعدين","الإعلانات","الأخبار","الاشتراك","سياسة المنصة"],
en: ["Dashboard","Prices","Orders","Traders","Mining","Ads","News","Subscription","Policy"]
};

function render(){
document.getElementById("title").innerText =
lang==="ar" ? "🟡 منصة السودان للتعدين" : "🟡 Sudan Mining Hub";

for(let i=1;i<=9;i++){
document.getElementById("c"+i).innerText = labels[lang][i-1];
}
}

document.addEventListener("DOMContentLoaded", () => {

document.getElementById("langBtn").addEventListener("click", () => {
lang = (lang==="ar") ? "en" : "ar";
render();
});

for(let i=1;i<=9;i++){
document.getElementById("c"+i).addEventListener("click", () => {
document.getElementById("panel").innerHTML =
"<h3>"+labels[lang][i-1]+"</h3><p>سيتم تفعيل هذا القسم قريباً</p>";
});
}

});
</script>

</body>
</html>
""")

