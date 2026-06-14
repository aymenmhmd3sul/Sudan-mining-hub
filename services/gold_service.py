import requests

def get_gold_price():
    try:
        # مصدر عالمي مستقر (USD index based proxy)
        r = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=XAUUSDT",
            timeout=10
        )
        r.raise_for_status()

        return {
            "status": "success",
            "source": "binance",
            "price_raw": r.json()
        }

    except Exception as e:
        return {
            "status": "error",
            "source": "binance",
            "price_raw": None,
            "error": str(e)
        }
