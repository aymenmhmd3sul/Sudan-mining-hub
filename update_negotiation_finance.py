import os

MAIN_NEGOTIATION_PATH = "./app/routers/negotiation.py"

with open(MAIN_NEGOTIATION_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# استبدال الدالة القديمة بالدالة الجديدة الذكية التي تحسب العمولات ديناميكياً
old_function_start = "def db_transition_to_state(room_id: int, new_state: str, actor_role: str, offer_data: Optional[dict] = None) -> tuple[bool, str]:"

new_function_code = """def db_transition_to_state(room_id: int, new_state: str, actor_role: str, offer_data: Optional[dict] = None) -> tuple[bool, str]:
    room = fetch_room_from_db(room_id)
    if not room:
        return False, "غرفة التفاوض غير موجودة في قاعدة البيانات"
    
    current_state = room["state"]
    if current_state in ["ACCEPT", "CLOSE"]:
        msg = f"التفاوض منتهي، الغرفة مغلقة بحالة: {current_state}"
        log_security_breach(
            user_email=room.get("buyer_id", "unknown"),
            action="ILLEGAL_STATE_MODIFICATION",
            details=f"محاولة تعديل السعر في غرفة مقفلة رقم {room_id} بحالة {current_state} بواسطة دور {actor_role}"
        )
        return False, msg
        
    if new_state not in VALID_STATES:
        return False, "حالة تفاوض غير قانونية"
        
    if new_state == "ACCEPT" and current_state not in ["OFFER", "COUNTER"]:
        return False, "لا يمكن قبول الصفقة قبل تقديم عرض أو عرض مضاد"
        
    history = room["offers_history"]
    if offer_data:
        history.append({
            "by_role": actor_role,
            "timestamp": datetime.utcnow().isoformat(),
            **offer_data
        })
        
    # حساب العمولة ديناميكياً عند قبول الصفقة نهائياً
    calculated_commission = 0.0
    if new_state == "ACCEPT":
        try:
            conn_settings = sqlite3.connect(DB_PATH)
            conn_settings.row_factory = sqlite3.Row
            
            # جلب تفاصيل العرض لمعرفة التصنيف والسعر الأخير
            offer = conn_settings.execute("SELECT category, price, custom_commission FROM offers WHERE id = ?", (room["offer_id"],)).fetchone()
            
            last_price = room["offers_history"][-1]["price"] if len(room["offers_history"]) > 0 else (offer["price"] if offer else 0.0)
            
            if offer:
                cat = offer["category"]
                if cat == "LIGHT_EQUIPMENT":
                    res = conn_settings.execute("SELECT value FROM system_settings WHERE key = 'light_equipment_fee'").fetchone()
                    calculated_commission = float(res["value"]) if res else 100000.0
                elif cat == "HEAVY_EQUIPMENT":
                    res = conn_settings.execute("SELECT value FROM system_settings WHERE key = 'heavy_equipment_rate'").fetchone()
                    rate = float(res["value"]) if res else 0.01
                    calculated_commission = last_price * rate
                elif cat == "ASSETS_FACILITIES":
                    # الأصول والورش تعتمد على القيمة التي حددها وسجلها التاجر بالتراضي
                    calculated_commission = float(offer["custom_commission"])
            conn_settings.close()
        except Exception:
            calculated_commission = 0.0

    conn = get_db_connection()
    conn.execute(\"\"\"
        UPDATE negotiation_rooms 
        SET state = ?, offers_history = ?, final_commission = ?, last_updated = ?
        WHERE id = ?
    \"\"\", (new_state, json.dumps(history), calculated_commission, datetime.utcnow().isoformat(), room_id))
    conn.commit()
    conn.close()
    
    return True, "تم تحديث قاعدة البيانات وحساب العمولة المالية بنجاح\""

# نقوم بالاستبدال المباشر لضمان التعديل الآمن
if old_function_start in code:
    # لتسهيل الاستبدال بدقة سنقوم بحقن التعديل في البنية التحتية للملف
    print("🎯 تم العثور على الدالة المستهدفة وجاري ترقيتها مالياً...")
"""

# لتجنب أي تعقيد في الاستبدال النصي، سنقوم بإعادة صياغة الملف الإجرائي لـ negotiation بكفاءة
# وسنقوم بالخطوة مباشرة برمجياً للتأكد من السلامة
