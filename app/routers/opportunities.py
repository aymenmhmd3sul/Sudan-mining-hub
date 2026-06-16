from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime

router = APIRouter()
OPPORTUNITIES_FILE = "data/opportunities.json"
OFFERS_FILE = "data/offers.json"

os.makedirs("data", exist_ok=True)

if not os.path.exists(OPPORTUNITIES_FILE):
    with open(OPPORTUNITIES_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(OFFERS_FILE):
    with open(OFFERS_FILE, "w") as f:
        json.dump([], f)

class OpportunityCreate(BaseModel):
    buyer_id: int
    type: str
    specs: str
    budget: float
    location: str
    city: str

class OfferCreate(BaseModel):
    opportunity_id: int
    seller_id: int
    price: float
    specs: str
    delivery_time: str
    condition: str

def get_opportunities():
    with open(OPPORTUNITIES_FILE, "r") as f:
        return json.load(f)

def save_opportunities(data):
    with open(OPPORTUNITIES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_offers():
    with open(OFFERS_FILE, "r") as f:
        return json.load(f)

def save_offers(data):
    with open(OFFERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@router.post("/create")
def create_opportunity(opp: OpportunityCreate):
    opportunities = get_opportunities()
    new_opp = {
        "id": len(opportunities) + 1,
        **opp.dict(),
        "status": "open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    opportunities.append(new_opp)
    save_opportunities(opportunities)
    return {"status": "success", "opportunity": new_opp}

@router.get("/list")
def list_opportunities():
    return {"opportunities": get_opportunities()}

@router.get("/all-offers")
def list_all_offers():
    return {"offers": get_offers()}

@router.get("/{opp_id}")
def get_opportunity(opp_id: int):
    opportunities = get_opportunities()
    for opp in opportunities:
        if opp["id"] == opp_id:
            return {"opportunity": opp}
    raise HTTPException(status_code=404, detail="الطلب غير موجود")

@router.post("/offer")
def create_offer(offer: OfferCreate):
    offers = get_offers()
    new_offer = {
        "id": len(offers) + 1,
        **offer.dict(),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    offers.append(new_offer)
    save_offers(offers)
    return {"status": "success", "offer": new_offer}

@router.get("/offers/{opportunity_id}")
def get_offers_for_opportunity(opportunity_id: int):
    offers = get_offers()
    result = [o for o in offers if o["opportunity_id"] == opportunity_id]
    return {"offers": result}
