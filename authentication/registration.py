"""User registration and secure bcrypt password hashing for FitMotion AI."""

from __future__ import annotations

import re
from typing import Any

import bcrypt
from sqlalchemy.orm import Session, sessionmaker

from database.database import SessionLocal, get_db_session
from database.models import User

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using a salted bcrypt digest."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plain-text password against its stored bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False


def validate_registration_inputs(full_name: str, email: str, password: str) -> list[str]:
    """Validate registration fields and return human-readable error messages."""
    errors: list[str] = []
    if len(full_name.strip()) < 2:
        errors.append("Please enter your full name (at least 2 characters).")
    if not EMAIL_PATTERN.match(email.strip().lower()):
        errors.append("Please enter a valid email address.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    return errors


def register_user(
    full_name: str,
    email: str,
    password: str,
    session_factory: sessionmaker[Session] | None = None,
) -> tuple[bool, str, dict[str, Any] | None]:
    """Register a new user account in SQLite.

    Returns:
        (success, message, user_dict_or_none)
    """
    clean_name = full_name.strip()
    clean_email = email.strip().lower()
    errors = validate_registration_inputs(clean_name, clean_email, password)
    if errors:
        return False, " ".join(errors), None

    factory = session_factory or SessionLocal
    with get_db_session(factory) as session:
        existing = session.query(User).filter_by(email=clean_email).first()
        if existing is not None:
            return False, "An account with this email already exists. Please log in instead.", None

        user = User(
            full_name=clean_name,
            email=clean_email,
            password_hash=hash_password(password),
            onboarding_completed=False,
        )
        session.add(user)
        session.flush()
        user_payload = {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "onboarding_completed": user.onboarding_completed,
        }
    return True, "Account created successfully! Let's personalize your athlete profile.", user_payload
