import requests

def get_gold_price():
    try:
        # مصدر بديل مستقر (proxy عالمي للأسعار)
        r = requests.get(
            "https://api.exchangerate.host/latest?base=XAU&symbols=USD",
            timeout=10
        )
        r.raise_for_status()
        data = r.json()

        return {
            "status": "success",
            "source": "exchangerate.host",
            "price_raw": data
        }

    except Exception as e:
        return {
            "status": "error",
            "source": "none",
            "price_raw": None,
            "error": str(e)
        }
