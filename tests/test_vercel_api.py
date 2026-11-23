"""End-to-end tests for the Vercel-native FastAPI serverless backend and web frontend."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


def test_vercel_api_health_meta_and_frontend_shell() -> None:
    """Health, metadata, static frontend, and animated SVG asset endpoints must return 200."""
    r_home = client.get("/")
    assert r_home.status_code == 200
    assert "FITMOTION AI" in r_home.text

    r_health = client.get("/api/health")
    assert r_health.status_code == 200
    assert r_health.json()["exercise_count"] >= 90

    r_meta = client.get("/api/meta")
    assert r_meta.status_code == 200
    meta = r_meta.json()
    assert meta["counts"]["Advanced"] >= 20
    assert len(meta["sports"]) == 8

    r_svg = client.get("/assets/images/st-nordic-hamstring.svg")
    assert r_svg.status_code == 200
    assert "image/svg+xml" in r_svg.headers["content-type"]
    assert "<animate " in r_svg.text


def test_vercel_api_full_athlete_demo_flow() -> None:
    """Demo athlete login, sport-specific filtering, ML recommendations, plans, assistant & analytics."""
    r_demo = client.post("/api/auth/demo")
    assert r_demo.status_code == 200
    uid = r_demo.json()["user"]["id"]

    # Sport-specific & Advanced filters
    r_swim = client.get("/api/exercises", params={"sport": "Swimming", "user_id": uid})
    assert r_swim.status_code == 200
    assert "Dryland Swim-Cord" in r_swim.json()["exercises"][0]["name"]

    r_adv = client.get("/api/exercises", params={"difficulty": "Advanced"})
    assert r_adv.status_code == 200
    assert r_adv.json()["total"] >= 20

    # Hybrid ML recommendations
    r_rec = client.post("/api/recommendations", json={"user_id": uid, "top_n": 6})
    assert r_rec.status_code == 200
    rec_data = r_rec.json()
    assert rec_data["ml_active"] is True
    assert len(rec_data["recommendations"]) == 6

    # Workout generator & 4-week plans
    r_gen = client.post(
        "/api/routines/generate",
        json={"user_id": uid, "routine_type": "Pre-sports warm-up", "duration_min": 10, "primary_sport": "Badminton"},
    )
    assert r_gen.status_code == 200
    assert len(r_gen.json()["routine"]["exercises"]) >= 2

    r_plans = client.get("/api/plans")
    assert r_plans.status_code == 200
    assert len(r_plans.json()["plans"]) >= 9

    # AI Assistant + safety guardrail
    r_ask = client.post("/api/assistant/ask", json={"question": "Suggest a cooldown after running.", "user_id": uid})
    assert r_ask.status_code == 200
    assert r_ask.json()["safety_triggered"] is False

    r_safe = client.post("/api/assistant/ask", json={"question": "I have sharp pain and swelling in my knee, diagnose it."})
    assert r_safe.status_code == 200
    assert r_safe.json()["safety_triggered"] is True

    # Planner & Analytics
    r_plan = client.get(f"/api/planner/{uid}")
    assert r_plan.status_code == 200
    assert len(r_plan.json()["week"]) == 7

    r_ana = client.get(f"/api/analytics/{uid}")
    assert r_ana.status_code == 200
    assert r_ana.json()["total_workouts"] >= 5
