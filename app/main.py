from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import auth, market, negotiation
from app.core.security.jwt import decode_token

app = FastAPI()

@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    public_paths = ["/api/auth/login", "/api/auth/logout", "/docs", "/openapi.json", "/"]

    if any(request.url.path.startswith(p) for p in public_paths):
        return await call_next(request)

    auth_header = request.headers.get("authorization")

    if not auth_header:
        return JSONResponse(status_code=401, content={"detail": "Missing token"})

    token = auth_header.replace("Bearer ", "").strip()

    try:
        payload = decode_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        request.state.user = payload

    except Exception as e:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)


app.include_router(auth.router)
app.include_router(market.router)
app.include_router(negotiation.router)

@app.get("/")
def root():
    return {"status": "running"}
