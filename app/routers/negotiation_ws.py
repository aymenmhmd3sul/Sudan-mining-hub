from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from datetime import datetime, timezone
import json
from app.core.db import get_db_connection
from app.security.auth import get_current_user

router = APIRouter(prefix="/ws/negotiation", tags=["Negotiation WebSockets"])

class NegotiationManager:
    """مدير الاتصالات الحية لغرف التفاوض لمنع تسريب البيانات."""
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast_to_room(self, room_id: int, payload: dict):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(payload)
                except Exception:
                    pass

manager = NegotiationManager()

def verify_ws_token(token: str) -> dict:
    """فك التوكن الموحد والتحقق من صلاحيته لبيئة الـ WebSockets."""
    try:
        from jose import jwt
        from app.core.security import SECRET_KEY, ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return {}

@router.websocket("/{room_id}")
async def negotiation_ws(websocket: WebSocket, room_id: int):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    payload = verify_ws_token(token)
    if not payload or "sub" not in payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_email = payload["sub"]
    role = payload.get("role", "unknown")

    # التحقق الفوري من قاعدة البيانات الموحدة: هل هذا المستخدم طرف في الغرفة؟
    conn = get_db_connection()
    room = conn.execute("SELECT buyer_id, seller_id FROM negotiation_rooms WHERE id = ?", (room_id,)).fetchone()
    
    if not room or user_email not in [room["buyer_id"], room["seller_id"]]:
        conn.close()
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, room_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            message_text = data.get("message")
            if not message_text:
                continue

            now_iso = datetime.now(timezone.utc).isoformat()

            # حفظ الرسالة الحية في جدول الرسائل الموحد
            conn.execute("""
                INSERT INTO messages (room_id, sender_email, message, created_at)
                VALUES (?, ?, ?, ?)
            """, (room_id, user_email, message_text, now_iso))
            conn.commit()

            # بث الرسالة بشكل آمن ومعزول داخل الغرفة فقط
            await manager.broadcast_to_room(room_id, {
                "room_id": room_id,
                "sender_email": user_email,
                "role": role,
                "message": message_text,
                "timestamp": now_iso
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    finally:
        conn.close()
