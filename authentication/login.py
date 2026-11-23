"""User login and session lookup utilities for FitMotion AI."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from authentication.registration import verify_password
from database.database import SessionLocal, get_db_session
from database.models import User


def authenticate_user(
    email: str,
    password: str,
    session_factory: sessionmaker[Session] | None = None,
) -> tuple[bool, str, dict[str, Any] | None]:
    """Authenticate an existing user by email and password."""
    clean_email = email.strip().lower()
    if not clean_email or not password:
        return False, "Please enter both your email address and password.", None

    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        user = session.query(User).filter_by(email=clean_email).first()
        if user is None or not verify_password(password, user.password_hash):
            return False, "Invalid email or password. Please check your credentials and try again.", None
        if not user.is_active:
            return False, "This account is currently inactive.", None

        user_payload = {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "onboarding_completed": user.onboarding_completed,
        }
    return True, f"Welcome back, {user_payload['full_name']}!", user_payload


def get_user_by_id(
    user_id: int,
    session_factory: sessionmaker[Session] | None = None,
) -> dict[str, Any] | None:
    """Fetch basic user session metadata by ID."""
    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        user = session.get(User, user_id)
        if user is None:
            return None
        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "onboarding_completed": user.onboarding_completed,
        }
