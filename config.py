"""Centralized configuration and constants for FitMotion AI."""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Base project paths
BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
ASSETS_DIR: Path = BASE_DIR / "assets"

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

# Application metadata
APP_NAME: str = "FitMotion AI"
APP_TAGLINE: str = "AI-Powered Exercise Recommendation & Athlete Wellness Platform"
APP_VERSION: str = "1.0.0"
APP_ENV: str = os.getenv("APP_ENV", "development")

# Detect read-only serverless environment (e.g., Vercel)
IS_SERVERLESS: bool = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

if IS_SERVERLESS:
    DEFAULT_DB_PATH: Path = Path("/tmp/fitmotion.db")
else:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_DB_PATH = DATA_DIR / "fitmotion.db"

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DEFAULT_DB_PATH.as_posix()}",
)

# Optional external LLM settings (used in Phase 7 with offline fallback)
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "none")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# Domain constants shared across modules
SUPPORTED_SPORTS: list[str] = [
    "Badminton",
    "Football",
    "Cricket",
    "Basketball",
    "Tennis",
    "Swimming",
    "Running",
    "General Fitness",
]

EXPERIENCE_LEVELS: list[str] = [
    "Beginner",
    "Intermediate",
    "Advanced",
]

FITNESS_GOALS: list[str] = [
    "Improve flexibility",
    "Improve mobility",
    "Build strength",
    "Improve endurance",
    "Improve cardiovascular fitness",
    "Improve balance",
    "Improve athletic performance",
    "General fitness and wellness",
    "Recovery and active recovery",
]

EXERCISE_CATEGORIES: list[str] = [
    "Warm-up",
    "Mobility",
    "Stretching and Flexibility",
    "Strength Training",
    "Cardiovascular Training",
    "Balance and Stability",
    "Recovery and Cooldown",
    "Sport-Specific Conditioning",
]

INTENSITY_LEVELS: list[str] = [
    "Low",
    "Moderate",
    "High",
]

SAFETY_DISCLAIMER: str = (
    "FitMotion AI provides general fitness, exercise organization, and athletic "
    "conditioning guidance. It is not a medical service and does not diagnose injuries "
    "or medical conditions. If you experience pain, dizziness, or have an existing "
    "injury or health concern, please consult a qualified healthcare professional "
    "before exercising."
)
