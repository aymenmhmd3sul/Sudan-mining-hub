import sqlite3

DB_PATH = "local.db"

def purge_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🧼 جاري تصفير وتطهير المنصة من كافة البيانات الوهمية...")
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM offers;")
    cursor.execute("DELETE FROM negotiation_rooms;")
    # تصغير حجم الملف برمجياً وإرجاعه للحجم الصفر
    cursor.execute("VACUUM;")
    
    conn.commit()
    conn.close()
    print("✨ قاعدة البيانات الآن نظيفة تماماً 100% وجاهزة لاستقبال البيانات الحقيقية!")

if __name__ == "__main__":
    purge_all()
