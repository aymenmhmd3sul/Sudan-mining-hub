import requests
import time

_cache = {
    "price": None,
    "timestamp": None,
    "status": "no_data"
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

    if _cache["price"] is not None:
        if now - _cache["timestamp"] < CACHE_TTL:
            return {"price": _cache["price"], "status": "cached"}

    try:
        price = fetch_from_api()

        _cache = {
            "price": price,
            "timestamp": now,
            "status": "live"
        }

        return {"price": price, "status": "live"}

    except Exception:
        if _cache["price"] is not None:
            return {"price": _cache["price"], "status": "stale"}

        return {"price": None, "status": "unavailable"}
