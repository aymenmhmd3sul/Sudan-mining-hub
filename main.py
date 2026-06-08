from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from typing import Optional
from models import MarketItem, MarketOrder

app = FastAPI(title="Sudan Mining Hub API", version="1.0.0")

# تفعيل الـ CORS للسماح لـ Streamlit بالاتصال بحرية
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # يسمح بالاتصال من أي مكان حالياً للتطوير
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=False)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# --- نماذج استقبال البيانات لمنع تضارب الـ ID التلقائي ---
class MarketItemCreate(SQLModel):
    title: str
    category: str
    description: str
    location: Optional[str] = None
    price: Optional[float] = None

class MarketOrderCreate(SQLModel):
    item_id: int
    buyer_name: str
    message: Optional[str] = None

# ---------------- MARKET ITEMS ----------------

@app.get("/api/v1/market/items")
def get_items():
    with Session(engine) as session:
        items = session.exec(select(MarketItem)).all()
        return items

@app.post("/api/v1/market/items")
def create_item(item: MarketItemCreate):
    with Session(engine) as session:
        db_item = MarketItem.model_validate(item)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

# ---------------- MARKET ORDERS ----------------

@app.post("/api/v1/market/orders")
def create_order(order: MarketOrderCreate):
    with Session(engine) as session:
        db_order = MarketOrder.model_validate(order)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order

@app.get("/api/v1/market/orders")
def get_orders():
    with Session(engine) as session:
        orders = session.exec(select(MarketOrder)).all()
        return orders

@app.get("/")
def root():
    return {"status": "running", "system": "market-api"}
