"""Streamlit UI smoke tests verifying all 16 FitMotion AI pages boot cleanly."""

from __future__ import annotations

from streamlit.testing.v1 import AppTest

import config
from dashboard.navigation import PAGES


def test_navigation_registry_has_all_16_active_pages() -> None:
    """All 16 platform pages should be registered, unique, and Active."""
    assert len(PAGES) == 16
    assert len({p.key for p in PAGES}) == 16
    assert all(p.status == "Active" for p in PAGES)


def test_all_16_pages_render_without_uncaught_exceptions() -> None:
    """Clicking every 1-click sidebar nav button should render all 16 pages cleanly."""
    app_path = str(config.BASE_DIR / "app.py")
    at = AppTest.from_file(app_path, default_timeout=20).run()
    assert not at.exception, f"Initial dashboard exception: {at.exception}"

    visited = 0
    for page in PAGES:
        btn = at.sidebar.button(key=f"snav_{page.key}")
        btn.click().run()
        assert not at.exception, f"Page '{page.title}' raised exception: {at.exception}"
        visited += 1

    assert visited == 16
