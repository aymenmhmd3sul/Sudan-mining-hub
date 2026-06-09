from fastapi import FastAPI
from sqlmodel import Session, select
import models, database

app = FastAPI(title="Mining API")

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/prices")
def prices():
    return {
        "local": 114186,
        "global": 75.56,
        "status": "live"
    }

@app.get("/items")
def items():
    with Session(database.engine) as session:
        return session.exec(select(models.MarketItem)).all()
