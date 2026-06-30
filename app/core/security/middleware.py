from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.security.jwt import decode_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")

        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]
            try:
                request.state.user = decode_token(token)
            except:
                request.state.user = None
        else:
            request.state.user = None

        return await call_next(request)
