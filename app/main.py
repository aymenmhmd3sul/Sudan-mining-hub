from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "deploy_test", "message": "Render connection OK"}
