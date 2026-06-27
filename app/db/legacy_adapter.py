from app.db.database import get_connection

def get_user(email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_session(user_id: str):
    return "mock-session"


def hash_password(password: str):
    return "hashed_" + password
