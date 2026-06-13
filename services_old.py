import random
import time

def get_gold_prices():
    base_local = 115000

    change = random.randint(-900, 1200)
    local = base_local + change

    return {
        "local": local,
        "global": round(local / 1600, 2),
        "change": change,
        "direction": "صعود 🔥" if change > 0 else "هبوط 🔻",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
