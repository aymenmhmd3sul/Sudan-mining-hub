from pathlib import Path

file = Path("main.py")
code = file.read_text()

# نحذف كل نسخ WebSocket القديمة بشكل آمن
start = "# =====================\n# Private Deal Rooms Chat System (FINAL CLEAN)"

if start in code:
    code = code.split(start)[0]

clean_ws = """
# =====================
# SINGLE CLEAN WEBSOCKET (FIXED)
# =====================
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from pathlib import Path

active_connections: Dict[str, List[WebSocket]] = {}

CHAT_STORE = Path("data/chat_messages.json")
CHAT_STORE.parent.mkdir(exist_ok=True)

def load_messages():
    if CHAT_STORE.exists():
        return json.loads(CHAT_STORE.read_text() or "{}")
    return {}

def save_messages(data):
    CHAT_STORE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def build_room_id(opportunity_id: str, buyer_id: str, seller_id: str):
    return f"{opportunity_id}:{buyer_id}:{seller_id}"

@app.websocket("/ws/chat/{opportunity_id}/{buyer_id}/{seller_id}")
async def chat_websocket(websocket: WebSocket, opportunity_id: str, buyer_id: str, seller_id: str):
    await websocket.accept()

    room_id = build_room_id(opportunity_id, buyer_id, seller_id)

    if room_id not in active_connections:
        active_connections[room_id] = []

    active_connections[room_id].append(websocket)

    store = load_messages()
    store.setdefault(room_id, [])

    try:
        while True:
            data = await websocket.receive_json()

            message = {
                "room_id": room_id,
                "sender_id": data.get("sender_id"),
                "message": data.get("message"),
                "timestamp": data.get("timestamp")
            }

            store[room_id].append(message)
            save_messages(store)

            dead = []
            for conn in active_connections[room_id]:
                try:
                    await conn.send_json(message)
                except:
                    dead.append(conn)

            for d in dead:
                active_connections[room_id].remove(d)

    except WebSocketDisconnect:
        if websocket in active_connections.get(room_id, []):
            active_connections[room_id].remove(websocket)

        if room_id in active_connections and not active_connections[room_id]:
            del active_connections[room_id]

"""

code = code.rstrip() + "\n\n" + clean_ws
file.write_text(code)

print("WEBSOCKET FULL FIX APPLIED")
