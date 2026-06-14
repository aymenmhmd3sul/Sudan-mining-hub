import requests

def fetch_raw_gold():
    try:
        r = requests.get(
            "https://api.metals.live/v1/spot/gold",
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return None

def get_gold_price():
    data = fetch_raw_gold()

    if data:
        return {
            "status": "success",
            "source": "metals.live",
            "price_raw": data
        }

    # fallback ثابت فقط لمنع crash وليس لتغيير المصدر
    return {
        "status": "error",
        "source": "no_data",
        "price_raw": None,
        "error": "external_api_failed"
    }
