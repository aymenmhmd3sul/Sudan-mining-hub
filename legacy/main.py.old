from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from pathlib import Path

app = FastAPI(title="Sudan Mining Hub - Smart Deals")

# =====================
# CONNECTIONS
# =====================
active_connections: Dict[str, List[WebSocket]] = {}

# =====================
# STORAGE
# =====================
CHAT_STORE = Path("data/chat_messages.json")
CHAT_STORE.parent.mkdir(exist_ok=True)

def load_messages():
    if CHAT_STORE.exists():
        return json.loads(CHAT_STORE.read_text() or "{}")
    return {}

def save_messages(data):
    CHAT_STORE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

# =====================
# SMART DEAL ENGINE v2
# =====================

def classify_deal(deal_type, value=0, description=""):
    if deal_type in ["light", "heavy", "project"]:
        return deal_type

    value = float(value or 0)
    text = (description or "").lower()

    if any(k in text for k in ["مصنع", "خط إنتاج", "بئر", "شركة", "طاقة", "معدات ثقيلة"]):
        return "project"

    if value <= 1000000:
        return "light"
    elif value <= 50000000:
        return "heavy"
    else:
        return "project"


def calculate_commission(deal_type, value):
    if deal_type == "light":
        return {
            "type": "fixed",
            "value": 100000,
            "payer": "seller"
        }

    if deal_type == "heavy":
        return {
            "type": "percent",
            "value": float(value) * 0.0025,
            "rate": "0.25%",
            "payer": "negotiated"
        }

    if deal_type == "project":
        return {
            "type": "agreement",
            "value": None,
            "payer": "manual"
        }

    return {"type": "unknown", "value": 0, "payer": "none"}

# =====================
# WEB SOCKET
# =====================
@app.websocket("/ws/chat/{opportunity_id}/{buyer_id}/{seller_id}")
async def chat_websocket(websocket: WebSocket, opportunity_id: str, buyer_id: str, seller_id: str):

    await websocket.accept()

    room = f"{opportunity_id}:{buyer_id}:{seller_id}"

    if room not in active_connections:
        active_connections[room] = []

    active_connections[room].append(websocket)

    store = load_messages()
    if room not in store:
        store[room] = []

    try:
        while True:
            data = await websocket.receive_json()

            msg_type = data.get("type", "chat")

            message = {
                "room": room,
                "type": msg_type,
                "sender_id": data.get("sender_id"),
                "message": data.get("message"),
                "status": data.get("status"),
                "value": data.get("value"),
                "description": data.get("description"),
                "timestamp": data.get("timestamp")
            }

            # =====================
            # DEAL COMPLETION LOGIC
            # =====================
            if data.get("status") == "تم التسلم":

                deal_type = classify_deal(
                    data.get("deal_type"),
                    data.get("value"),
                    data.get("description")
                )

                commission = calculate_commission(
                    deal_type,
                    data.get("value", 0)
                )

                message["system"] = "DEAL_COMPLETED"
                message["deal_type"] = deal_type
                message["commission"] = commission

            # SAVE
            store[room].append(message)
            save_messages(store)

            # BROADCAST
            for conn in list(active_connections[room]):
                try:
                    await conn.send_json(message)
                except:
                    active_connections[room].remove(conn)

    except WebSocketDisconnect:
        if websocket in active_connections.get(room, []):
            active_connections[room].remove(websocket)

        if room in active_connections and not active_connections[room]:
            del active_connections[room]
