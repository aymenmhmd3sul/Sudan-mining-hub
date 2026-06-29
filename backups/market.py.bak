from fastapi import APIRouter, Depends
import sqlite3

from app.core.security.jwt import get_current_user

router = APIRouter(prefix="/market", tags=["Market"])

DB = "local.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# 1. Get Offers (SMART RULES)
# =========================
@router.get("/offers")
def get_offers(user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    role = user.get("role")
    user_id = user["user_id"]

    if role == "seller":
        # seller sees only his offers
        offers = cur.execute(
            "SELECT * FROM trader_offers WHERE seller_id=?",
            (user_id,)
        ).fetchall()

    else:
        # buyer + admin sees all offers
        offers = cur.execute(
            "SELECT * FROM trader_offers"
        ).fetchall()

    return [dict(o) for o in offers]


# =========================
# 2. Get Buyer Requests (optional rule)
# =========================
@router.get("/requests")
def get_requests(user=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    requests = cur.execute(
        "SELECT * FROM buyer_requests"
    ).fetchall()

    return [dict(r) for r in requests]
