import time

# قيمة افتراضية آمنة دائمًا
DEFAULT_GOLD_PRICE = 4200.0

# كاش بسيط
_cache = {
    "price": None,
    "timestamp": 0
}

CACHE_TTL = 60


def source_primary():
    """
    المصدر الأول (حاليًا آمن ومؤقت)
    لاحقًا نستبدله بـ API حقيقي
    """
    # الآن لا نكسر النظام
    return DEFAULT_GOLD_PRICE


def get_gold_price():
    now = time.time()

    # استخدام الكاش إذا موجود
    if _cache["price"] is not None and (now - _cache["timestamp"]) < CACHE_TTL:
        return float(_cache["price"])

    try:
        price = source_primary()

        _cache["price"] = float(price)
        _cache["timestamp"] = now

        return float(price)

    except Exception:
        return DEFAULT_GOLD_PRICE
