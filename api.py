from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/api/v1/market/items")
def get_items():
    return {"debug": "endpoint reached successfully"}
