import uuid
from datetime import datetime
from app.db.database import get_connection


def insert_deal(request_id: str, offer_id: str, buyer_id: str, seller_id: str, price: float, commission: float):
    conn = get_connection()
    cur = conn.cursor()

    deal_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO deals (
            id,
            request_id,
            offer_id,
            buyer_id,
            seller_id,
            price,
            commission,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        deal_id,
        request_id,
        offer_id,
        buyer_id,
        seller_id,
        price,
        commission,
        "active",
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    return deal_id


def fetch_deals():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM deals ORDER BY created_at DESC")
    rows = cur.fetchall()

    conn.close()

    return [dict(r) for r in rows]
