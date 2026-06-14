from datetime import datetime, timedelta

subscriptions = {}

def create_subscription(user_id: int, transaction_id: str):
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)

    subscriptions[user_id] = {
        "status": "pending",
        "start_date": start_date,
        "end_date": end_date,
        "transaction_id": transaction_id
    }

    return subscriptions[user_id]


def activate_subscription(user_id: int):
    if user_id in subscriptions:
        subscriptions[user_id]["status"] = "active"
        return True
    return False


def check_access(user_id: int):
    sub = subscriptions.get(user_id)

    if not sub:
        return False

    if sub["status"] != "active":
        return False

    if sub["end_date"] < datetime.utcnow():
        return False

    return True
