import time
import threading
import requests

CACHE = {
    "price": 2400.0,
    "timestamp": time.time()
}

UPDATE_INTERVAL = 60  # ثانية


def fetch_price():
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url, timeout=5)
    data = r.json()
    return float(data[0][1])


def updater():
    while True:
        try:
            price = fetch_price()
            if price:
                CACHE["price"] = float(price)
                CACHE["timestamp"] = time.time()
        except:
            pass

        time.sleep(UPDATE_INTERVAL)


# تشغيل التحديث في الخلفية عند بدء الخدمة
threading.Thread(target=updater, daemon=True).start()


def get_price():
    return float(CACHE["price"])
