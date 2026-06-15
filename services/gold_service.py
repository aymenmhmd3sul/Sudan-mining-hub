import requests

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"

def _fetch_binance():
    try:
        r = requests.get(BINANCE_URL, timeout=5)
        return float(r.json()["price"])
    except:
        return None


def _fetch_backup():
    # fallback ثابت (يمكن لاحقاً ربطه بمصدر آخر)
    return 2330.0


def get_gold_price():
    prices = []

    b = _fetch_binance()
    if b:
        prices.append(b)

    if not prices:
        prices.append(_fetch_backup())

    avg_price = sum(prices) / len(prices)

    return {
        "status": "success",
        "gold_usd": round(avg_price, 2),
        "sources_used": len(prices)
    }
