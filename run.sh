#!/bin/bash

# أمر طوارئ مركزي يُنفذ مباشرة داخل السيرفر قبل إقلاع الـ API
python3 -c "
from sqlalchemy import create_engine, text
try:
    engine = create_engine('postgresql://mining_hub_user:aT78wH2pL9qX@dpg-cpl7v9g11fds7397c8fg-a.oregon-postgres.render.com/mining_hub_db')
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text(\"UPDATE \\\"user\\\" SET role = 'ADMIN', status = 'ACTIVE' WHERE email = 'aymen.mhmd3@gmail.com'\"))
    print('✅ SYSTEM_BOOT: Admin privileges verified and forced on production database.')
except Exception as e:
    print('⚠️ SYSTEM_BOOT_ERROR:', e)
"

# أمر تشغيل السيرفر الأصلي الخاص بك (تأكد أنه يطابق أمر التشغيل الافتراضي لديك، مثل uvicorn أو gunicorn)
uvicorn app.main:app --host 0.0.0.0 --port $PORT
