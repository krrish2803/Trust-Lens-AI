"""
TrustLens AI - Authentication API Endpoints
JWT-based signup, login, and profile management.
"""

import uuid
import hashlib
import hmac
import os
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional
from pydantic import BaseModel, Field
from jose import JWTError, jwt

from backend.config import settings
from backend.database.mongodb import db_manager

router = APIRouter(prefix="/api/auth")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt.hex() + ":" + dk.hex()


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, dk_hex = stored.split(":")
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(dk.hex(), dk_hex)
    except Exception:
        return False

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


# ── Request / Response Models ────────────────────────────────────────────────

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    created_at: str


# ── Helpers ──────────────────────────────────────────────────────────────────

def create_access_token(user_id: str, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


async def _get_user_by_email(email: str) -> Optional[dict]:
    if db_manager.is_connected and db_manager.db is not None:
        try:
            doc = await db_manager.db.users.find_one({"email": email}, {"_id": 0})
            if doc:
                return doc
        except Exception:
            pass

    # In-memory fallback
    for u in db_manager._memory_users:
        if u.get("email") == email:
            return u
    return None


async def _save_user(user: dict):
    if db_manager.is_connected and db_manager.db is not None:
        try:
            await db_manager.db.users.insert_one(dict(user))
            return
        except Exception:
            pass

    db_manager._memory_users.append(user)


async def _get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
        )

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        email = payload.get("email")
        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload.",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    user = await _get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return user


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/signup", response_model=TokenResponse)
async def signup(payload: SignupRequest):
    existing = await _get_user_by_email(payload.email.lower().strip())
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user_id = f"user-{uuid.uuid4().hex[:12]}"
    hashed_password = hash_password(payload.password)
    user = {
        "id": user_id,
        "name": payload.name.strip(),
        "email": payload.email.lower().strip(),
        "password_hash": hashed_password,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    await _save_user(user)
    token = create_access_token(user_id, user["email"])
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await _get_user_by_email(payload.email.lower().strip())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token(user["id"], user["email"])
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserProfile)
async def get_profile(user: dict = Depends(_get_current_user)):
    return UserProfile(
        id=user["id"],
        name=user.get("name", ""),
        email=user["email"],
        created_at=user.get("created_at", ""),
    )


@router.post("/profile", response_model=UserProfile)
async def update_profile(
    data: dict,
    user: dict = Depends(_get_current_user),
):
    if "name" in data:
        user["name"] = data["name"]

    if db_manager.is_connected and db_manager.db is not None:
        try:
            await db_manager.db.users.update_one(
                {"id": user["id"]},
                {"$set": {"name": user.get("name", "")}},
            )
        except Exception:
            pass

    return UserProfile(
        id=user["id"],
        name=user.get("name", ""),
        email=user["email"],
        created_at=user.get("created_at", ""),
    )
