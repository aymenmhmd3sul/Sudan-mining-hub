import sqlite3

DB = "local.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- OFFER VALIDATION (SECURED) ----------------
def get_active_offer(offer_id: int):
    conn = get_db()
    cur = conn.cursor()

    offer = cur.execute(
        """
        SELECT id, seller_id, status 
        FROM trader_offers 
        WHERE id = ? AND status = 'active'
        """,
        (offer_id,)
    ).fetchone()

    conn.close()
    return offer


# ---------------- DUPLICATE CHECK (SECURE INDEX BEHAVIOR) ----------------
def room_exists(offer_id: int, buyer_id: int):
    conn = get_db()
    cur = conn.cursor()

    room = cur.execute(
        """
        SELECT id FROM negotiation_rooms 
        WHERE offer_id = ? AND buyer_id = ?
        LIMIT 1
        """,
        (offer_id, buyer_id)
    ).fetchone()

    conn.close()
    return room


# ---------------- CREATE ROOM ----------------
def create_room_logic(offer_id: int, buyer_id: int, seller_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO negotiation_rooms 
        (offer_id, buyer_id, seller_id, status, created_at)
        VALUES (?, ?, ?, 'active', datetime('now'))
        """,
        (offer_id, buyer_id, seller_id)
    )

    conn.commit()
    room_id = cur.lastrowid
    conn.close()

    return room_id


# ---------------- GET ROOMS ----------------
def get_user_rooms(user_id: int):
    conn = get_db()
    cur = conn.cursor()

    rooms = cur.execute(
        """
        SELECT * FROM negotiation_rooms 
        WHERE buyer_id = ? OR seller_id = ?
        """,
        (user_id, user_id)
    ).fetchall()

    conn.close()
    return [dict(r) for r in rooms]


# ---------------- GET MESSAGES ----------------
def get_room_messages(room_id: int):
    conn = get_db()
    cur = conn.cursor()

    messages = cur.execute(
        """
        SELECT * FROM messages 
        WHERE room_id = ? 
        ORDER BY id ASC
        """,
        (room_id,)
    ).fetchall()

    conn.close()
    return [dict(m) for m in messages]
