from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime

router = APIRouter()
CHAT_FILE = "data/chats.json"

os.makedirs("data", exist_ok=True)

if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump([], f)

class MessageSend(BaseModel):
    opportunity_id: int
    sender_id: int
    receiver_id: int
    message: str

def get_chats():
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

def save_chats(data):
    with open(CHAT_FILE, "w") as f:
        json.dump(data, f, indent=2)

@router.post("/send")
def send_message(msg: MessageSend):
    chats = get_chats()
    
    chat_id = None
    for chat in chats:
        if (chat["opportunity_id"] == msg.opportunity_id and 
            ((chat["seller_id"] == msg.sender_id and chat["buyer_id"] == msg.receiver_id) or
             (chat["seller_id"] == msg.receiver_id and chat["buyer_id"] == msg.sender_id))):
            chat_id = chat["id"]
            break
    
    if chat_id is None:
        new_chat = {
            "id": len(chats) + 1,
            "opportunity_id": msg.opportunity_id,
            "buyer_id": msg.receiver_id if msg.sender_id != msg.receiver_id else msg.sender_id,
            "seller_id": msg.sender_id if msg.sender_id != msg.receiver_id else msg.receiver_id,
            "messages": [],
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        chats.append(new_chat)
        chat_id = new_chat["id"]
    
    for chat in chats:
        if chat["id"] == chat_id:
            chat["messages"].append({
                "sender_id": msg.sender_id,
                "message": msg.message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            break
    
    save_chats(chats)
    
    keywords = ["تم الاتفاق", "وافقت", "موافق", "تم البيع", "تم الشراء", "اتفقنا"]
    detected = any(keyword in msg.message for keyword in keywords)
    
    return {
        "status": "success", 
        "chat_id": chat_id,
        "ai_detected": detected,
        "message": "تم إرسال الرسالة" + (" - تنبيه: يبدو أنكما توصلا إلى اتفاق! اضغط زر تأكيد الاتفاق." if detected else "")
    }

@router.get("/{opportunity_id}/{user_id}")
def get_chat(opportunity_id: int, user_id: int):
    chats = get_chats()
    for chat in chats:
        if chat["opportunity_id"] == opportunity_id and (chat["buyer_id"] == user_id or chat["seller_id"] == user_id):
            return {"chat": chat}
    raise HTTPException(status_code=404, detail="لا توجد محادثة")
