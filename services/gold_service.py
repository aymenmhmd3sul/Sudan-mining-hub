import time
import requests

DEFAULT_GOLD_PRICE = 4200.0

_cache = {
    "price": None,
    "timestamp": 0
}

CACHE_TTL = 60


def source_api():
    """
    مصدر خارجي حقيقي (آمن مع timeout)
    """
    try:
        # مثال API بسيط (يمكن تغييره لاحقًا)
        url = "https://api.metals.live/v1/spot/gold"

        r = requests.get(url, timeout=5)
        data = r.json()

        # بعض الـ APIs ترجع list
        price = data[0][1] if isinstance(data, list) else data["price"]

        return float(price)

    except Exception:
        return None


def get_gold_price():
    now = time.time()

    # الكاش أولاً
    if _cache["price"] is not None and (now - _cache["timestamp"]) < CACHE_TTL:
        return float(_cache["price"])

    price = None

    # نحاول المصدر الخارجي
    try:
        price = source_api()
    except:
        price = None

    # fallback نهائي
    if price is None:
        price = DEFAULT_GOLD_PRICE

    _cache["price"] = float(price)
    _cache["timestamp"] = now

    return float(price)
