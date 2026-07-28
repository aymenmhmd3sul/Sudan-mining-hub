import uuid
from datetime import datetime
from app.db.database import get_connection


def insert_offer(user_id: str, request_id: str, price: float):
    conn = get_connection()
    cur = conn.cursor()

    offer_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO offers (id, user_id, request_id, price, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        offer_id,
        user_id,
        request_id,
        price,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    return offer_id


def fetch_offers(request_id: str = None):
    conn = get_connection()
    cur = conn.cursor()

    if request_id:
        cur.execute(
            "SELECT * FROM offers WHERE request_id=? ORDER BY created_at DESC",
            (request_id,)
        )
    else:
        cur.execute("SELECT * FROM offers ORDER BY created_at DESC")

    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]
