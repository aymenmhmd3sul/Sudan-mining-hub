import time
import requests

CACHE_TTL = 60
_cache = {"price": None, "timestamp": 0}

DEFAULT_GOLD_PRICE = 0.0


def source_api():
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url, timeout=5)
    data = r.json()

    if isinstance(data, list):
        return float(data[0][1])
    return float(data["price"])


def get_price():
    now = time.time()

    if _cache["price"] is not None and (now - _cache["timestamp"]) < CACHE_TTL:
        return float(_cache["price"])

    try:
        price = source_api()
    except:
        price = None

    if price is None:
        price = DEFAULT_GOLD_PRICE

    _cache["price"] = float(price)
    _cache["timestamp"] = now

    return float(price)
