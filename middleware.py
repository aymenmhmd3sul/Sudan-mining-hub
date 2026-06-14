from fastapi import Request
from subscription import check_access

class SubscriptionMiddleware:
    async def __call__(self, request: Request, call_next):
        path = request.url.path

        # السماح للمسارات العامة
        public_paths = ["/", "/docs", "/openapi.json", "/health"]

        if path in public_paths:
            return await call_next(request)

        # مؤقتاً user_id ثابت
        user_id = 1

        if not check_access(user_id):
            return {"error": "subscription required"}

        response = await call_next(request)
        return response
