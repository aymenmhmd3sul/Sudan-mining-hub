from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/dashboard")
def dashboard():
    return {"status": "dashboard working", "gold": "disabled"}
