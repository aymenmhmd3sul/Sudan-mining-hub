from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, database

app = FastAPI(title="Mining Smart API")

# ================= CORE =================
@app.get("/")
def root():
    return {"status": "API running Smart Version"}

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


# ================= CLASSIFICATION =================
def classify_deal(category: str):
    heavy_keywords = ["equipment", "factory", "mining", "plant", "drilling", "heavy"]
    return any(k in category.lower() for k in heavy_keywords)


# ================= REQUEST SYSTEM =================
class RequestIn(BaseModel):
    buyer_name: str
    whatsapp: str
    category: str
    specs: str


@app.post("/request")
def create_request(data: RequestIn):
    with Session(database.engine) as session:

        req = models.BuyerRequest(
            buyer_name=data.buyer_name,
            whatsapp=data.whatsapp,
            category=data.category,
            specs=data.specs
        )

        # AI-like classification layer
        req.is_heavy_deal = classify_deal(data.category)
        req.estimated_value = "500000" if req.is_heavy_deal else "100000"

        session.add(req)
        session.commit()
        session.refresh(req)

        return {
            "status": "created",
            "id": req.id,
            "is_heavy_deal": req.is_heavy_deal,
            "estimated_value": req.estimated_value
        }


# ================= CONFIRMATION SYSTEM =================
class Confirm(BaseModel):
    request_id: int
    party: str  # buyer or trader


@app.post("/confirm")
def confirm(data: Confirm):
    with Session(database.engine) as session:

        req = session.get(models.BuyerRequest, data.request_id)

        if not req:
            return {"error": "not found"}

        if data.party == "buyer":
            req.buyer_confirmed = True
        elif data.party == "trader":
            req.trader_confirmed = True

        # auto finalize
        if req.buyer_confirmed and req.trader_confirmed:
            req.status = "confirmed"

        session.commit()

        return {
            "status": "updated",
            "confirmed": req.buyer_confirmed and req.trader_confirmed
        }


# ================= COMMISSION SYSTEM =================
class CommissionCalc(BaseModel):
    request_id: int


@app.post("/commission")
def commission(data: CommissionCalc):
    with Session(database.engine) as session:

        req = session.get(models.BuyerRequest, data.request_id)

        if not req:
            return {"error": "not found"}

        commission_value = "0.25%" if req.is_heavy_deal else 100000

        return {
            "request_id": req.id,
            "status": req.status,
            "commission": commission_value
        }


# ================= SAFE COMMISSION =================
@app.post("/commission-safe")
def commission_safe(data: CommissionCalc):
    with Session(database.engine) as session:

        req = session.get(models.BuyerRequest, data.request_id)

        if not req:
            return {"error": "not found"}

        # safety rule
        if not (req.buyer_confirmed and req.trader_confirmed):
            return {
                "error": "deal not confirmed yet",
                "buyer_confirmed": req.buyer_confirmed,
                "trader_confirmed": req.trader_confirmed
            }

        commission_value = "0.25%" if req.is_heavy_deal else 100000

        return {
            "request_id": req.id,
            "status": req.status,
            "commission": commission_value,
            "confirmed": True
        }
