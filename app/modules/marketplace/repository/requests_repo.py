import uuid
from datetime import datetime
from app.db.database import get_connection


def insert_request(user_id: str, title: str, category: str):
    conn = get_connection()
    cur = conn.cursor()

    request_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO requests (id, user_id, title, category, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        request_id,
        user_id,
        title,
        category,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    return request_id


def fetch_requests():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM requests ORDER BY created_at DESC")
    rows = cur.fetchall()

    conn.close()

    return [dict(r) for r in rows]
