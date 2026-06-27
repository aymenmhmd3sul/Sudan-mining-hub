from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.security.jwt import decode_token
from datetime import datetime
import sqlite3

router = APIRouter()
DB = "local.db"

active_connections = {}

def get_db():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@router.websocket("/ws/negotiation/{room_id}")
async def negotiation_ws(websocket: WebSocket, room_id: int):
    await websocket.accept()

    token = websocket.query_params.get("token")
    payload = decode_token(token)

    if not payload:
        await websocket.close()
        return

    user_id = payload["user_id"]
    role = payload.get("role")

    active_connections.setdefault(room_id, []).append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")

            conn = get_db()
            cur = conn.cursor()

            room = cur.execute(
                "SELECT * FROM negotiation_rooms WHERE id=?",
                (room_id,)
            ).fetchone()

            if not room:
                continue

            if user_id not in (room["buyer_id"], room["seller_id"]):
                continue

            cur.execute(
                "INSERT INTO messages (room_id, sender_id, message, created_at) VALUES (?, ?, ?, ?)",
                (room_id, user_id, message, datetime.utcnow())
            )

            conn.commit()
            conn.close()

            for ws in active_connections[room_id]:
                await ws.send_json({
                    "room_id": room_id,
                    "sender_id": user_id,
                    "role": role,
                    "message": message,
                    "timestamp": str(datetime.utcnow())
                })

    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
