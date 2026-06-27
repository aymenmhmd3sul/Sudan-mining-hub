from fastapi import FastAPI, Form
from app.db.compat import add_user, users_db
from app.modules.auth.login_service import login_user

app = FastAPI()


# =========================
# STARTUP SEED
# =========================
@app.on_event("startup")
def startup():
    add_user("user1", "test@test.com", "123", "user")
    print("✔ system ready")


# =========================
# AUTH LOGIN (JWT)
# =========================
@app.post("/auth/login")
def login(email: str = Form(...), password: str = Form(...)):
    result = login_user(email, password)

    if not result:
        return {"detail": "invalid credentials"}

    return result


# =========================
# BASIC HEALTH
# =========================
@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/market/requests")
def market_requests():
    return []
