import os
import sys
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError



app = FastAPI(title="Sudan Mining Hub")

# كود تهيئة قاعدة البيانات التكيفي والآمن
try:
    try:
        from app.security.auth import engine
        from app.db.database import Base
    except ImportError:
        try:
            from app.database import Base, engine
        except ImportError:
try:
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print('🚀 [RADICAL DB SUCCESS] Database engine fully unified and tables verified via Gold Layout.')
except Exception as db_err:
    print(f'⚠️ [DB STARTUP WARN] Database setup bypassed: {db_err}')
try:
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print('🚀 [RADICAL DB SUCCESS] Database engine fully unified and tables verified via Gold Layout.')
except Exception as db_err:
    print(f'⚠️ [DB STARTUP WARN] Database setup bypassed: {db_err}')
try:
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print('🚀 [RADICAL DB SUCCESS] Database engine fully unified and tables verified via Gold Layout.')
except Exception as db_err:
    print(f'⚠️ [DB STARTUP WARN] Database setup bypassed: {db_err}')
