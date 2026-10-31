"""Authentication endpoints — register, login, refresh, me."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from civicflow_contracts.application import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserProfile,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    decode_token,
)

router = APIRouter()

# In-memory user store for standalone development (replaced by PostgreSQL in Phase 3)
_users: dict[str, dict] = {}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    if body.email in _users:
        raise HTTPException(status_code=409, detail="Email already registered")
    import uuid
    user_id = f"user-{uuid.uuid4().hex[:12]}"
    _users[body.email] = {
        "id": user_id,
        "name": body.name,
        "email": body.email,
        "password_hash": hash_password(body.password),
        "phone": body.phone,
        "location": body.location,
    }
    access = create_access_token({"sub": user_id, "email": body.email})
    refresh = create_refresh_token({"sub": user_id, "email": body.email})
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    user = _users.get(body.email)
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token({"sub": user["id"], "email": body.email})
    refresh = create_refresh_token({"sub": user["id"], "email": body.email})
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(token: str):
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Not a refresh token")
        access = create_access_token({"sub": payload["sub"], "email": payload.get("email")})
        refresh = create_refresh_token({"sub": payload["sub"], "email": payload.get("email")})
        return TokenResponse(access_token=access, refresh_token=refresh)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.get("/me", response_model=UserProfile)
async def me():
    # TODO: extract user from Authorization header via dependency injection
    # For now, return a demo profile
    return UserProfile(
        id="user-aarav-patil",
        name="Aarav Patil",
        email="aarav@example.com",
        phone="+91 98765 43210",
        location="Pune, Maharashtra",
    )
