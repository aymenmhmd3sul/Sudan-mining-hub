import random
from datetime import datetime

def get_gold_prices():
    base_local = 114000
    variation = random.randint(-500, 500)

    local = base_local + variation
    global_price = 75.56

    direction = "صعود 🔥" if variation >= 0 else "هبوط 🔻"

    return {
        "local": local,
        "global": global_price,
        "direction": direction,
        "change": variation,
        "timestamp": datetime.utcnow().isoformat()
    }
