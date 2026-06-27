from datetime import datetime
import uuid
from app.db.database import get_connection


# -------------------------
# REQUESTS
# -------------------------

def create_request(user_id: str, title: str, category: str):
    conn = get_connection()
    cur = conn.cursor()

    req_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO requests (id, user_id, title, category, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (req_id, user_id, title, category, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return req_id


def get_requests():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM requests ORDER BY created_at DESC")
    rows = cur.fetchall()

    conn.close()
    return [dict(r) for r in rows]


# -------------------------
# OFFERS
# -------------------------

def create_offer(user_id: str, request_id: str, price: float):
    conn = get_connection()
    cur = conn.cursor()

    offer_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO offers (id, user_id, request_id, price, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (offer_id, user_id, request_id, price, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return offer_id


def get_offers(request_id: str = None):
    conn = get_connection()
    cur = conn.cursor()

    if request_id:
        cur.execute("SELECT * FROM offers WHERE request_id=? ORDER BY created_at DESC", (request_id,))
    else:
        cur.execute("SELECT * FROM offers ORDER BY created_at DESC")

    rows = cur.fetchall()

    conn.close()
    return [dict(r) for r in rows]
