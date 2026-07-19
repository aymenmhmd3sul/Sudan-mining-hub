"""
Database compatibility layer.
Supports legacy websocket modules and new SQLAlchemy modules.
"""

from app.database import engine, SessionLocal, get_db, Base


def get_db_connection():
    """
    Compatibility wrapper for legacy modules.
    Returns a raw sqlite connection.
    """
    import sqlite3

    db_url = str(engine.url)

    if db_url.startswith("sqlite:///"):
        path = db_url.replace("sqlite:///", "")
        return sqlite3.connect(
            path,
            check_same_thread=False
        )

    raise RuntimeError(
        "Legacy raw connection is only supported for SQLite"
    )
