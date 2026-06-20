import sqlite3
import time

DB = 'local.db'

def remind():
    print('Running reminder system...')
    # هنا لاحقاً سنربط قاعدة البيانات الفعلية
    print('Checked pending invoices')

if __name__ == '__main__':
    while True:
        remind()
        time.sleep(86400)
