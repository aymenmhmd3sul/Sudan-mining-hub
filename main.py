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
        return 2330.0

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}

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
    padding:15px;
    text-align:center;
    background:#111827;
    font-size:22px;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:10px;
    padding:15px;
}}

.card {{
    background:#1f2937;
    padding:20px;
    border-radius:12px;
    text-align:center;
    cursor:pointer;
}}

.panel {{
    margin:15px;
    padding:15px;
    background:#111827;
    border-radius:12px;
}}

.footer {{
    text-align:center;
    padding:15px;
    background:#0b1220;
}}
</style>

</head>

<body>

<div class="header">🟡 منصة السودان للتعدين</div>

<div class="grid">
<div class="card" data-text="📦 الطلبات">الطلبات</div>
<div class="card" data-text="👤 التجار">التجار</div>
<div class="card" data-text="⛏️ التعدين">التعدين</div>
<div class="card" data-text="📢 الإعلانات">الإعلانات</div>
<div class="card" data-text="💳 الاشتراك">الاشتراك</div>
</div>

<div id="panel" class="panel">اضغط على أي قسم</div>

<div class="footer">
سياسة المنصة
</div>

<script>
document.addEventListener("click", function(e) {{
    const card = e.target.closest(".card");
    if(!card) return;

    document.getElementById("panel").innerText =
        "تم فتح: " + card.dataset.text;
}});
</script>

</body>
</html>
""")
