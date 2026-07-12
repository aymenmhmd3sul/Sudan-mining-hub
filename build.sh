#!/usr/bin/env bash
# الخروج فوراً في حال حدوث أي خطأ
set -o errexit

echo "=== بدء مرحلة البناء على Render ==="

# 1. تثبيت الاعتمادات
pip install -r requirements.txt

# 2. تشغيل الترحيلات على PostgreSQL
echo "=== تشغيل Alembic Migrations ==="
alembic upgrade head

echo "=== اكتمل البناء والترحيل بنجاح ==="
