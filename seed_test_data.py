import sqlite3
from datetime import datetime
import json

DB_PATH = "local.db"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.utcnow().isoformat()
    
    print("🧹 تنظيف البيانات القديمة لضمان فحص نقي...")
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM offers;")
    cursor.execute("DELETE FROM negotiation_rooms;")
    
    print("👤 1. حقن المستخدمين بمختلف التصنيفات الإدارية والتجارية...")
    users = [
        ("admin_chief@gold.sd", "admin", None, "ACTIVE", now_str),
        ("light_trader@gold.sd", "trader", "LIGHT_EQUIPMENT", "ACTIVE", now_str),
        ("heavy_trader@gold.sd", "trader", "HEAVY_EQUIPMENT", "ACTIVE", now_str),
        ("buyer_test@test.com", "buyer", None, "ACTIVE", now_str)
    ]
    cursor.executemany("""
        INSERT INTO users (email, role, trader_category, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, users)
    
    print("📢 2. حقن إعلانات التعدين والمعدات في السوق...")
    # إعلان معدات خفيفة (عمولة مقطوعة 100,000 ج.س)
    # إعلان معدات ثقيلة (عمولة 1% - سعر 50,000,000 ج.س -> العمولة المتوقعة 500,000 ج.س)
    offers = [
        (1, "light_trader@gold.sd", "مكابس هيدروليكية صغيرة لتعدين الذهب", "LIGHT_EQUIPMENT", 1500000.0, 0.0, "TRADER", "ACTIVE", now_str),
        (2, "heavy_trader@gold.sd", "جرافة كاتر بيلر D9 ثقيلة لمواقع الذهب", "HEAVY_EQUIPMENT", 50000000.0, 0.0, "TRADER", "ACTIVE", now_str)
    ]
    cursor.executemany("""
        INSERT INTO offers (id, trader_email, title, category, price, custom_commission, commission_payer, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, offers)
    
    print("🤝 3. فتح غرف تفاوض وإغلاق صفقات لحساب العمولات تلقائياً...")
    # الغرفة الأولى: صفقة مقفولة ومقبولة ومحسوب عمولتها تلقائياً عبر النظام
    history_room1 = [
        {"by_role": "buyer", "timestamp": now_str, "price": 50000000.0, "quantity": 1.0, "notes": "جاهز لإتمام الصفقة بالسعر الرسمي"}
    ]
    cursor.execute("""
        INSERT INTO negotiation_rooms (id, offer_id, buyer_id, seller_id, state, offers_history, final_commission, commission_status, created_at, last_updated)
        VALUES (701, 2, 'buyer_test@test.com', 'heavy_trader@gold.sd', 'ACCEPT', ?, 500000.0, 'UNPAID', ?, ?)
    """, (json.dumps(history_room1), now_str, now_str))
    
    # الغرفة الثانية: غرفة تفاوض جارية ومفتوحة لم يحدد سعرها النهائي بعد
    cursor.execute("""
        INSERT INTO negotiation_rooms (id, offer_id, buyer_id, seller_id, state, offers_history, final_commission, commission_status, created_at, last_updated)
        VALUES (702, 1, 'buyer_test@test.com', 'light_trader@gold.sd', 'OPEN', '[]', 0.0, 'UNPAID', ?, ?)
    """, (now_str, now_str))
    
    conn.commit()
    conn.close()
    print("✨ تم ملء قاعدة البيانات ببيانات الفحص الشاملة بنجاح باهر!")

if __name__ == "__main__":
    seed_data()
