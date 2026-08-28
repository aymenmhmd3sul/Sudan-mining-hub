from datetime import timedelta

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.services.auth_service import verify_password, get_password_hash
from app.core.security import create_access_token


router = APIRouter(tags=["Auth"])


def _role_value(user: User) -> str:
    """Return the canonical lowercase role value."""
    return str(
        getattr(user.role, "value", user.role)
    ).strip().lower()


def _redirect_for_role(role: str) -> str:
    """Return the real dashboard route for each supported role."""
    redirects = {
        UserRole.ADMIN.value: "/admin/dashboard",
        UserRole.MERCHANT.value: "/merchant/workspace/dashboard",
        UserRole.BUYER.value: "/buyer/dashboard",
        UserRole.AGENT.value: "/agent/dashboard",
    }
    return redirects.get(role, "/login")


async def _read_credentials(request: Request):
    """
    Accept both JSON and HTML form submissions.
    Returns: email, password
    """
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        try:
            body = await request.json()
            return (
                body.get("email") or body.get("username"),
                body.get("password"),
            )
        except Exception:
            pass

    try:
        form = await request.form()
        return (
            form.get("email") or form.get("username"),
            form.get("password"),
        )
    except Exception:
        return None, None


async def _read_registration_data(request: Request):
    """
    Accept JSON and form registration payloads.
    """
    content_type = request.headers.get("content-type", "").lower()

    email = None
    password = None
    full_name = None
    phone = None
    account_type = UserRole.BUYER.value

    if "application/json" in content_type:
        try:
            body = await request.json()

            email = body.get("email") or body.get("username")
            password = body.get("password")
            full_name = body.get("full_name") or body.get("name")
            phone = body.get("phone") or body.get("phone_number")
            account_type = (
                body.get("account_type")
                or body.get("role")
                or UserRole.BUYER.value
            )
        except Exception:
            pass

    if not email or not password:
        try:
            form = await request.form()

            email = form.get("email") or form.get("username")
            password = form.get("password")
            full_name = (
                form.get("full_name")
                or form.get("name")
                or full_name
            )
            phone = (
                form.get("phone")
                or form.get("phone_number")
                or phone
            )
            account_type = (
                form.get("account_type")
                or form.get("role")
                or account_type
            )
        except Exception:
            pass

    return email, password, full_name, phone, account_type


def _normalize_role(account_type) -> UserRole:
    value = str(account_type or UserRole.BUYER.value).strip().lower()

    if value in {
        UserRole.ADMIN.value,
        UserRole.MERCHANT.value,
        UserRole.BUYER.value,
        UserRole.AGENT.value,
    }:
        return UserRole(value)

    # Compatibility with older frontend values.
    if "merchant" in value or "seller" in value:
        return UserRole.MERCHANT

    if "agent" in value:
        return UserRole.AGENT

    if "admin" in value:
        return UserRole.ADMIN

    return UserRole.BUYER


@router.post("/auth/login", operation_id="auth_login")
@router.post("/login", include_in_schema=False)
@router.post("/api/auth/login", include_in_schema=False)
async def login(
    request: Request,
    db: Session = Depends(get_db),
):
    email, password = await _read_credentials(request)

    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "الرجاء إدخال البريد الإلكتروني وكلمة المرور."
            },
        )

    normalized_email = str(email).strip().lower()

    user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if not user or not getattr(user, "is_active", True):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "البريد الإلكتروني أو كلمة المرور غير صحيحة."
            },
        )

    # password_hash is canonical.
    # hashed_password remains a legacy compatibility column.
    stored_hash = (
        getattr(user, "password_hash", None)
        or getattr(user, "hashed_password", None)
    )

    if not verify_password(str(password), stored_hash):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "البريد الإلكتروني أو كلمة المرور غير صحيحة."
            },
        )

    role = _role_value(user)
    redirect_url = _redirect_for_role(role)

    if redirect_url == "/login":
        return JSONResponse(
            status_code=403,
            content={
                "detail": "دور المستخدم غير صالح للوصول إلى المنصة."
            },
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "id": user.id,
            "email": user.email,
            "role": role,
        },
        expires_delta=timedelta(days=30),
    )

    response = JSONResponse(
        content={
            "status": "success",
            "message": "تم تسجيل الدخول بنجاح",
            "redirect": redirect_url,
            "access_token": access_token,
            "role": role,
        }
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=2592000,
        samesite="lax",
        secure=False,
    )

    return response


@router.post("/auth/register", operation_id="auth_register")
@router.post("/register", include_in_schema=False)
@router.post("/api/auth/register", include_in_schema=False)
async def register_user(
    request: Request,
    db: Session = Depends(get_db),
):
    (
        email,
        password,
        full_name,
        phone,
        account_type,
    ) = await _read_registration_data(request)

    if not email or not password or not full_name:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "الرجاء تعبئة كافة الحقول الإجبارية."
            },
        )

    normalized_email = str(email).strip().lower()
    normalized_name = str(full_name).strip()
    normalized_phone = str(phone or "").strip()

    if not normalized_phone:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "رقم الهاتف مطلوب."
            },
        )

    if not normalized_name:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "الاسم مطلوب."
            },
        )

    existing_email = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if existing_email:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "البريد الإلكتروني مستخدم مسبقاً."
            },
        )

    existing_phone = (
        db.query(User)
        .filter(User.phone == normalized_phone)
        .first()
    )

    if existing_phone:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "رقم الهاتف مستخدم مسبقاً."
            },
        )

    role_enum = _normalize_role(account_type)

    password_hash = get_password_hash(str(password))

    new_user = User(
        name=normalized_name,
        full_name=normalized_name,
        email=normalized_email,
        phone=normalized_phone,
        password_hash=password_hash,
        hashed_password=password_hash,
        role=role_enum,
        is_active=True,
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={
                "detail": "تعذر إنشاء الحساب. تحقق من البيانات وحاول مرة أخرى."
            },
        )

    return JSONResponse(
        content={
            "status": "success",
            "message": "تم إنشاء الحساب بنجاح",
            "redirect": "/login",
            "role": _role_value(new_user),
        }
    )
