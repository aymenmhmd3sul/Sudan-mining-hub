import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_shared_data():
    fallback_data = {
        "status": "success",
        "source": "system_fallback",
        "price_raw": 2335.50,
        "gold_usd": 2335.50,
        "error": None
    }

    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        res = requests.get(url, timeout=5)
        res.raise_for_status()

        data = res.json()
        price_str = data.get("price")

        if price_str:
            val = float(price_str)
            return {
                "status": "success",
                "source": "binance",
                "price_raw": val,
                "gold_usd": val,
                "error": None
            }

    except Exception as e:
        print(f"Gold fetch error: {e}")

    return fallback_data


def get_gold_price():
    return get_shared_data()


def fetch_live_gold_price_v2():
    return get_shared_data()
