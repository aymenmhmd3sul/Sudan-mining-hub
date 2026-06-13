from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, database

app = FastAPI(title="Mining API V2")

# ---------------- CORE ----------------
@app.get("/")
def root():
    return {"status": "API running V2"}

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
        return session.query(models.TraderOffer).all()


# ---------------- REQUEST ----------------
class RequestIn(BaseModel):
    buyer_name: str
    whatsapp: str
    category: str
    specs: str


def classify_deal(category: str):
    heavy_keywords = ["equipment", "factory", "mining", "plant", "drilling", "heavy"]
    return any(word in category.lower() for word in heavy_keywords)


@app.post("/request")
def create_request(data: RequestIn):
    with Session(database.engine) as session:
        req = models.BuyerRequest(
            buyer_name=data.buyer_name,
            whatsapp=data.whatsapp,
            category=data.category,
            specs=data.specs
        )

        req.is_heavy_deal = classify_deal(data.category)

        if req.is_heavy_deal:
            req.estimated_value = "500000"
        else:
            req.estimated_value = "100000"

        session.add(req)
        session.commit()
        session.refresh(req)

        return {
            "status": "created",
            "id": req.id,
            "is_heavy_deal": req.is_heavy_deal
        }

# ---------------- COMMISSION SYSTEM ----------------
class CommissionCalc(BaseModel):
    request_id: int


@app.post("/commission")
def calculate_commission(data: CommissionCalc):
    with Session(database.engine) as session:
        req = session.get(models.BuyerRequest, data.request_id)

        if not req:
            return {"error": "not found"}

        # ---------------- RULE ----------------
        if req.is_heavy_deal:
            commission = "0.25%"
        else:
            commission = 100000

        return {
            "request_id": req.id,
            "status": req.status,
            "commission": commission
        }

# ---------------- SAFE COMMISSION (ONLY AFTER CONFIRM) ----------------
@app.post("/commission-safe")
def commission_safe(data: CommissionCalc):
    with Session(database.engine) as session:
        req = session.get(models.BuyerRequest, data.request_id)

        if not req:
            return {"error": "not found"}

        # ---------------- SAFETY RULE ----------------
        if not (req.buyer_confirmed and req.trader_confirmed):
            return {
                "error": "deal not confirmed yet",
                "buyer_confirmed": req.buyer_confirmed,
                "trader_confirmed": req.trader_confirmed
            }

        # ---------------- COMMISSION LOGIC ----------------
        if req.is_heavy_deal:
            commission = "0.25%"
        else:
            commission = 100000

        return {
            "request_id": req.id,
            "status": req.status,
            "commission": commission,
            "confirmed": True
        }
