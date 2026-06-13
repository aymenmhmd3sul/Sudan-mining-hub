import models
from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
try:
    from patch_streamlit import patch_streamlit_ctx
except ImportError:
    patch_streamlit_ctx = None

app = FastAPI(title="Sudan Mining Hub API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "running"}

@app.get("/api/v1/market/items")
def get_items():
    with Session(engine) as session:
        items = session.exec(select(models.MarketItem)).all()
        return items

@app.get("/api/v1/prices")
def get_prices():
    return {
        "local_price": 114842,
        "global_price": 75.56,
        "direction": "مستقر",
        "change": 0,
        "history": [114700, 114750, 114800, 114850]
    }

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
