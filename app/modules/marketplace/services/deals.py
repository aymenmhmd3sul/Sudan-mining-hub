from datetime import datetime
import uuid
from app.db.database import get_connection


# -----------------------------
# COMMISSION RULES
# -----------------------------

def calculate_commission(price: float, category: str):
    """
    Rules:
    - equipment light: fixed 100,000
    - everything else: 2%
    """

    if category == "light":
        return 100000
    return price * 0.02


# -----------------------------
# CREATE DEAL
# -----------------------------

def create_deal(request_id: str, offer_id: str, buyer_id: str, seller_id: str, price: float, category: str):
    conn = get_connection()
    cur = conn.cursor()

    deal_id = str(uuid.uuid4())
    commission = calculate_commission(price, category)

    cur.execute("""
        INSERT INTO deals (
            id, request_id, offer_id, buyer_id, seller_id,
            price, commission, status, created_at
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

    return {
        "deal_id": deal_id,
        "commission": commission,
        "status": "active"
    }


# -----------------------------
# GET DEALS
# -----------------------------

def get_deals():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM deals ORDER BY created_at DESC")
    rows = cur.fetchall()

    conn.close()
    return [dict(r) for r in rows]
