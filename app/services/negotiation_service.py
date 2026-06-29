from app.db import get_db

# -------- OFFERS --------
def get_active_offer(offer_id: int):
    with get_db() as db:
        cur = db.execute(
            "SELECT * FROM offers WHERE id = ?",
            (offer_id,)
        )
        return cur.fetchone()


# -------- ROOMS --------
def room_exists(offer_id: int, buyer_id: int):
    with get_db() as db:
        cur = db.execute(
            "SELECT id FROM negotiation_rooms WHERE offer_id=? AND buyer_id=?",
            (offer_id, buyer_id)
        )
        return cur.fetchone() is not None


def create_room_logic(offer_id: int, buyer_id: int, seller_id: int):
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO negotiation_rooms (offer_id, buyer_id, seller_id) VALUES (?,?,?)",
            (offer_id, buyer_id, seller_id)
        )
        db.commit()
        return cur.lastrowid


# -------- USER ROOMS --------
def get_user_rooms(user_id: int):
    with get_db() as db:
        cur = db.execute(
            """
            SELECT * FROM negotiation_rooms
            WHERE buyer_id = ? OR seller_id = ?
            ORDER BY created_at DESC
            """,
            (user_id, user_id)
        )
        return cur.fetchall()


# -------- MESSAGES --------
def get_room_messages(room_id: int):
    with get_db() as db:
        cur = db.execute(
            "SELECT * FROM messages WHERE room_id = ? ORDER BY created_at ASC",
            (room_id,)
        )
        return cur.fetchall()
