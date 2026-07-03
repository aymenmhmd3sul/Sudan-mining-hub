import sqlite3
import os

# تحويل المسار إلى مسار مطلق ثابت يضمن قراءة نفس الملف من أي مكان يُشغل منه السيرفر
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, "local.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
