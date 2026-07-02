import sqlite3

DATABASE_PATH = "local.db"

def get_db_connection():
    """
    مصدر الحقيقة الموحد لفتح اتصال بقاعدة البيانات.
    يضمن تفعيل Row factory لقراءة الحقول كـ Dictionaries.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
