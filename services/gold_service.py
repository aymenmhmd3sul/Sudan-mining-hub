import time

# قيمة ثابتة احتياطية (Fallback)
DEFAULT_GOLD_PRICE = 4200.0

# كاش بسيط جدًا لمنع أي ضغط أو فشل متكرر
_cache = {
    "price": None,
    "timestamp": 0
}

CACHE_TTL = 60  # ثانية واحدة كحد أدنى للاستقرار


def get_price():
    now = time.time()

    # إذا عندنا قيمة محفوظة وصالحة
    if _cache["price"] is not None and (now - _cache["timestamp"]) < CACHE_TTL:
        return float(_cache["price"])

    try:
        # هنا أي مصدر خارجي لاحقًا
        # حالياً لا نعتمد عليه لتفادي الفشل
        price = DEFAULT_GOLD_PRICE

        _cache["price"] = float(price)
        _cache["timestamp"] = now

        return float(price)

    except Exception:
        # ضمان عدم انهيار النظام نهائياً
        return DEFAULT_GOLD_PRICE
