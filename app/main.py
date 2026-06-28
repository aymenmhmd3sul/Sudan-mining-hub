from fastapi import FastAPI
from app.routers import auth, market, negotiation

app = FastAPI()

app.include_router(auth.router)
app.include_router(market.router)
app.include_router(negotiation.router, prefix="/negotiation")

@app.get("/")
def root():
    return {"status": "running"}
