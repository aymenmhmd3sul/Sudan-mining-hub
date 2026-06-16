from fastapi import FastAPI, HTMLResponse
import requests

app = FastAPI()

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT", timeout=5)
        return round(float(r.json()["price"]), 2)
    except:
        return 2330.0

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/gold")
def api_gold():
    return {"gold": get_price()}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    gold = get_price()

    return HTMLResponse(f"""
    <html>
    <head>
        <title>Sudan Mining Hub</title>
        <meta charset="utf-8">
    </head>

    <body style="background:#0f172a;color:white;font-family:Arial;padding:20px">

        <h1>🟡 Sudan Mining Dashboard</h1>

        <div style="padding:15px;background:#1f2937;border-radius:10px;margin-top:20px">
            <h3>Gold Price</h3>
            <p style="font-size:24px">{gold} USD</p>
        </div>

        <div style="margin-top:20px">
            <p>Status: Running</p>
        </div>

    </body>
    </html>
    """)

