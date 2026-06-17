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
    
    # البحث عن محادثة بين هذا المشتري والتاجر لهذا الطلب
    chat_id = None
    for chat in chats:
        if (chat["opportunity_id"] == msg.opportunity_id and 
            ((chat["buyer_id"] == msg.sender_id and chat["seller_id"] == msg.receiver_id) or
             (chat["buyer_id"] == msg.receiver_id and chat["seller_id"] == msg.sender_id))):
            chat_id = chat["id"]
            break
    
    # إنشاء محادثة جديدة إذا لم توجد
    if chat_id is None:
        # تحديد من هو المشتري ومن هو التاجر
        # نفرض أن المرسل هو التاجر والمستقبل هو المشتري (أو العكس)
        # لكننا نحدد الأدوار بناءً على ids
        # نستخدم منطقاً بسيطاً: الطرف الذي ليس له دور seller هو buyer
        # لكننا سنحصل على الأدوار من قاعدة البيانات (مبسط)
        # هنا سنفترض أن sender هو التاجر إذا كان receiver هو المشتري (والعكس)
        # لكننا سنستخدم منطقاً أكثر دقة: سنخمن من خلال ids
        # ولكن لتسهيل الأمور، نحدد buyer_id و seller_id بناءً على من أرسل الرسالة
        # في الواقع، يجب أن نعرف الأدوار، لكننا سنبسطها كالتالي:
        # سنعتبر أن أول من يرسل هو المشتري (لأن المشتري يبدأ المحادثة عادة)
        # لكن يمكن أن يكون التاجر أيضاً، لذا سنحدد الأدوار من خلال ids
        # سنستخدم قاعدة: إذا كان sender_id هو صاحب الطلب (buyer) أو لا.
        # لكن ليس لدينا معلومات عن صاحب الطلب هنا، لذا سنطلب من الواجهة إرسال buyer_id و seller_id صراحة.
        # سنعدل الـ API ليقبل buyer_id و seller_id في الطلب.
        # لكننا سنبسط: سنعتبر أن sender_id هو المشتري دائماً في البداية.
        # سنحل المشكلة بطلب إرسال buyer_id و seller_id من الواجهة.
        # سنقوم بتعديل `MessageSend` ليشمل buyer_id و seller_id.
        # لكن لتجنب تعقيد الـ API، سنقوم بحساب الأدوار من ids المتاحة.
        # سنفترض أن المشتري هو id أقل (مبسط) - لكن هذا غير دقيق.
        # الحل الصحيح: نطلب من الواجهة إرسال buyer_id و seller_id.
        # سأقوم بتعديل `MessageSend` لإضافة buyer_id و seller_id.
        # لكني سأقوم بتعديل الكود هنا لاستقبالهم.
        # سنقوم بتعديل الـ Model.
        # لكن لتجنب إعادة كتابة الـ Model، سنقوم بتمريرهم في request body.
        # سنقوم بتعديل الـ endpoint لاستقبالهم.
        # لكن بما أننا نكتب الآن، سنعدل الـ Model.
        # سأقوم بإعادة كتابة الـ Model.
        pass

# سنعيد كتابة الـ endpoint بطريقة صحيحة
@router.post("/send")
def send_message(payload: dict):
    # payload يحتوي على: opportunity_id, sender_id, receiver_id, message, buyer_id, seller_id
    opportunity_id = payload.get("opportunity_id")
    sender_id = payload.get("sender_id")
    receiver_id = payload.get("receiver_id")
    message = payload.get("message")
    buyer_id = payload.get("buyer_id")
    seller_id = payload.get("seller_id")
    
    if not all([opportunity_id, sender_id, receiver_id, message, buyer_id, seller_id]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    chats = get_chats()
    
    # البحث عن محادثة بين هذا المشتري والتاجر لهذا الطلب
    chat_id = None
    for chat in chats:
        if (chat["opportunity_id"] == opportunity_id and 
            chat["buyer_id"] == buyer_id and 
            chat["seller_id"] == seller_id):
            chat_id = chat["id"]
            break
    
    # إنشاء محادثة جديدة إذا لم توجد
    if chat_id is None:
        new_chat = {
            "id": len(chats) + 1,
            "opportunity_id": opportunity_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "messages": [],
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        chats.append(new_chat)
        chat_id = new_chat["id"]
    
    # إضافة الرسالة
    for chat in chats:
        if chat["id"] == chat_id:
            chat["messages"].append({
                "sender_id": sender_id,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            break
    
    save_chats(chats)
    
    # كشف الكلمات المفتاحية للذكاء الاصطناعي (مبسط)
    keywords = ["تم الاتفاق", "وافقت", "موافق", "تم البيع", "تم الشراء", "اتفقنا"]
    detected = any(keyword in message for keyword in keywords)
    
    return {
        "status": "success", 
        "chat_id": chat_id,
        "ai_detected": detected,
        "message": "تم إرسال الرسالة" + (" - تنبيه: يبدو أنكما توصلا إلى اتفاق! اضغط زر تأكيد الاتفاق." if detected else "")
    }

@router.get("/list/{user_id}")
def list_user_chats(user_id: int):
    chats = get_chats()
    result = []
    for chat in chats:
        if chat["buyer_id"] == user_id or chat["seller_id"] == user_id:
            result.append(chat)
    return {"chats": result}

@router.get("/{opportunity_id}/{buyer_id}/{seller_id}")
def get_chat(opportunity_id: int, buyer_id: int, seller_id: int):
    chats = get_chats()
    for chat in chats:
        if chat["opportunity_id"] == opportunity_id and chat["buyer_id"] == buyer_id and chat["seller_id"] == seller_id:
            return {"chat": chat}
    return {"chat": None}  # لا توجد محادثة بعد
