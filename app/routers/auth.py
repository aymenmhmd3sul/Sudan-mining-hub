from fastapi import APIRouter, Form
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return AuthService.authenticate_user(username, password)
