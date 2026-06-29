from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.core.security.jwt import decode_token


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        public_paths = (
            "/api/auth/login",
            "/docs",
            "/openapi.json",
        )

        # السماح للـ public routes
        if any(request.url.path.startswith(p) for p in public_paths):
            return await call_next(request)

        auth = request.headers.get("authorization")

        if not auth:
            raise HTTPException(status_code=401, detail="Missing token")

        token = auth.replace("Bearer ", "")

        try:
            payload = decode_token(token)
            request.state.user = payload
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
