import time
import requests

_cache = {
    "price": None,
    "timestamp": 0,
    "history": []
}

CACHE_TTL = 60
DEFAULT_GOLD_PRICE = 2400


def fetch_price():
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url, timeout=5)
    data = r.json()

    if isinstance(data, list):
        return float(data[0][1])
    return float(data.get("price", 0))


def get_price():
    now = time.time()

    # كاش سريع
    if _cache["price"] is not None and (now - _cache["timestamp"]) < CACHE_TTL:
        return _cache["price"]

    try:
        price = fetch_price()
    except:
        price = 0

    # fallback آمن
    if not price or price <= 0:
        price = DEFAULT_GOLD_PRICE

    # smoothing (منع التذبذب)
    _cache["history"].append(price)
    if len(_cache["history"]) > 5:
        _cache["history"].pop(0)

    smooth_price = sum(_cache["history"]) / len(_cache["history"])

    _cache["price"] = float(smooth_price)
    _cache["timestamp"] = now

    return float(smooth_price)

