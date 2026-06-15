import time
import requests

_cache = {
    "price": None,
    "timestamp": 0
}

CACHE_TTL = 60  # ثانية واحدة للتجربة الآمنة
DEFAULT_GOLD_PRICE = 2400


def fetch_source_1():
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url, timeout=5)
    data = r.json()
    if isinstance(data, list):
        return float(data[0][1])
    return float(data["price"])


def fetch_source_2():
    # مصدر احتياطي بسيط (يمكن تطويره لاحقًا)
    url = "https://goldpricez.com/api/gold/spot"
    r = requests.get(url, timeout=5)
    data = r.json()
    return float(data.get("price", 0))


def get_price():
    now = time.time()

    # كاش
    if _cache["price"] is not None and (now - _cache["timestamp"]) < CACHE_TTL:
        return _cache["price"]

    prices = []

    for f in [fetch_source_1, fetch_source_2]:
        try:
            p = f()
            if p and p > 0:
                prices.append(p)
        except:
            continue

    if prices:
        price = sum(prices) / len(prices)
    else:
        price = DEFAULT_GOLD_PRICE

    _cache["price"] = float(price)
    _cache["timestamp"] = now

    return float(price)

