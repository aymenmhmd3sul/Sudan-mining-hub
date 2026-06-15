import requests
import time

_cache = {
    "price": None,
    "timestamp": None
}

CACHE_TTL = 300  # 5 minutes


def fetch_from_api():
    url = "https://api.metals.live/v1/spot/gold"

    r = requests.get(url, timeout=8)
    r.raise_for_status()

    data = r.json()

    if isinstance(data, list) and len(data) > 0:
        return float(data[0][1]) if isinstance(data[0], list) else float(data[0])

    if isinstance(data, dict):
        return float(data.get("price"))

    raise ValueError("Unexpected API format")


def get_price():
    global _cache

    now = time.time()

    try:
        if _cache["price"] is not None:
            if now - _cache["timestamp"] < CACHE_TTL:
                return _cache["price"]

        price = fetch_from_api()

        _cache = {
            "price": price,
            "timestamp": now
        }

        return price

    except Exception:
        return _cache["price"]
