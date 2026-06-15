import time
import requests

CACHE_TTL = 120
_cache = {"price": None, "timestamp": 0}

# قيمة احتياطية منطقية (ليست صفر)
FALLBACK_PRICE = 2400


def fetch_metals_live():
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url, timeout=5)
    data = r.json()
    return float(data[0][1])


def fetch_commoditypriceapi():
    # مصدر بديل (قد يفشل أحياناً)
    url = "https://commoditypriceapi.com/api/v1/spot/gold"
    r = requests.get(url, timeout=5)
    if r.status_code == 200:
        data = r.json()
        return float(data.get("price", 0))
    return None


def get_price():
    now = time.time()

    # كاش سريع
    if _cache["price"] is not None and (now - _cache["timestamp"]) < CACHE_TTL:
        return float(_cache["price"])

    sources = [
        fetch_metals_live,
        fetch_commoditypriceapi
    ]

    price = None

    for src in sources:
        try:
            price = src()
            if price and price > 0:
                break
        except:
            continue

    if not price or price <= 0:
        price = FALLBACK_PRICE

    _cache["price"] = float(price)
    _cache["timestamp"] = now

    return float(price)
