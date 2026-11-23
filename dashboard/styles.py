"""WHOOP × Nike Training Club × Strava × GOWOD × Darebee Design System for FitMotion AI."""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --fm-bg: #09090B;
    --fm-surface: #121318;
    --fm-surface-2: #181A22;
    --fm-surface-hover: #1E202A;
    --fm-border: rgba(255, 255, 255, 0.085);
    --fm-border-strong: rgba(255, 255, 255, 0.18);
    --fm-text: #FAFAFA;
    --fm-text-muted: #9CA3AF;
    --fm-orange: #FC4C02;        /* Strava Blaze Orange */
    --fm-green: #00E676;         /* WHOOP Recovery Neon Green */
    --fm-cyan: #00D4FF;          /* GOWOD / Nike Electric Cyan */
    --fm-amber: #FFB020;         /* Warm-up / Intensity Amber */
}

/* Hide Streamlit chrome & Deploy button */
.stAppDeployButton, [data-testid="stAppDeployButton"], footer, #MainMenu {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: rgba(9, 9, 11, 0.72) !important;
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--fm-bg);
    color: var(--fm-text);
}

h1, h2, h3, .fm-display {
    font-family: 'Barlow Condensed', 'Inter', sans-serif !important;
    letter-spacing: 0.015em;
    text-transform: uppercase;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3.5rem;
    max-width: 1260px;
}

/* ===== SIDEBAR (WHOOP / NIKE PRECISION NAV) ===== */
[data-testid="stSidebar"] {
    background: #0C0D11 !important;
    border-right: 1px solid var(--fm-border) !important;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.1rem;
    padding-left: 0.85rem;
    padding-right: 0.85rem;
}

.fm-brand-box {
    padding: 0.9rem 1rem;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(252, 76, 2, 0.16) 0%, rgba(18, 19, 24, 0.96) 70%);
    border: 1px solid rgba(252, 76, 2, 0.35);
    margin-bottom: 0.9rem;
}

.fm-brand-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.05;
}

.fm-brand-sub {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin: 0.25rem 0 0 0;
}

.fm-nav-group {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6B7280;
    margin: 0.95rem 0 0.35rem 0.3rem;
}

/* Sleek sidebar nav buttons */
[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    text-align: left !important;
    justify-content: flex-start !important;
    background: transparent !important;
    color: #D1D5DB !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    padding: 0.44rem 0.72rem !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
    margin-bottom: -0.35rem !important;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #FFFFFF !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(252, 76, 2, 0.22) 0%, rgba(252, 76, 2, 0.06) 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(252, 76, 2, 0.48) !important;
    border-left: 3px solid var(--fm-orange) !important;
    font-weight: 700 !important;
}

/* ===== HERO BANNER (WHOOP / NIKE STUDIO) ===== */
.fm-hero {
    position: relative;
    background: radial-gradient(circle at 88% 18%, rgba(252, 76, 2, 0.18), transparent 42%),
                radial-gradient(circle at 12% 90%, rgba(0, 212, 255, 0.10), transparent 44%),
                linear-gradient(135deg, #121318 0%, #0C0D12 100%);
    border: 1px solid var(--fm-border);
    border-radius: 20px;
    padding: 1.85rem 2.1rem;
    margin-bottom: 1.35rem;
    overflow: hidden;
}

.fm-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--fm-orange), var(--fm-cyan), var(--fm-green));
    opacity: 0.85;
}

.fm-hero h1 {
    font-size: 2.55rem;
    font-weight: 800;
    margin: 0.6rem 0 0.35rem 0;
    color: #FFFFFF;
    line-height: 1.04;
}

.fm-hero p {
    color: #A1A1AA;
    font-size: 0.95rem;
    line-height: 1.55;
    max-width: 780px;
    margin: 0;
}

/* ===== PILLS & BADGES ===== */
.fm-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.24rem 0.7rem;
    border-radius: 999px;
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.fm-pill-live {
    background: rgba(0, 230, 118, 0.12);
    color: var(--fm-green);
    border: 1px solid rgba(0, 230, 118, 0.34);
}

.fm-pill-phase {
    background: rgba(252, 76, 2, 0.14);
    color: #FF7A45;
    border: 1px solid rgba(252, 76, 2, 0.38);
}

.fm-pill-cyan {
    background: rgba(0, 212, 255, 0.12);
    color: var(--fm-cyan);
    border: 1px solid rgba(0, 212, 255, 0.34);
}

.fm-pill-upcoming {
    background: rgba(255, 255, 255, 0.06);
    color: #D4D4D8;
    border: 1px solid rgba(255, 255, 255, 0.14);
}

/* ===== CARDS & KPI TILES (WHOOP / STRAVA) ===== */
.fm-card {
    background: var(--fm-surface);
    border: 1px solid var(--fm-border);
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    height: 100%;
    transition: border-color 0.2s ease, transform 0.2s ease, background 0.2s ease;
}

.fm-card:hover {
    border-color: var(--fm-border-strong);
    background: var(--fm-surface-2);
}

.fm-metric-label {
    font-size: 0.70rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    color: #71717A;
    margin-bottom: 0.38rem;
}

.fm-metric-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.15rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.05;
    letter-spacing: 0.02em;
}

.fm-metric-sub {
    font-size: 0.80rem;
    color: #A1A1AA;
    margin-top: 0.32rem;
}

.fm-section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #FFFFFF;
    margin: 1.55rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.fm-section-title::before {
    content: "";
    width: 4px;
    height: 1.1rem;
    border-radius: 99px;
    background: var(--fm-orange);
    display: inline-block;
}

/* ===== GOWOD-STYLE MUSCLE & SPORT CHIPS ===== */
.fm-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.42rem;
    margin-top: 0.5rem;
}

.fm-chip {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.10);
    color: #E4E4E7;
    padding: 0.24rem 0.62rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.fm-chip-accent {
    background: rgba(0, 212, 255, 0.10);
    border: 1px solid rgba(0, 212, 255, 0.28);
    color: #67E8F9;
}

.fm-chip-orange {
    background: rgba(252, 76, 2, 0.12);
    border: 1px solid rgba(252, 76, 2, 0.34);
    color: #FF8A5B;
}

.fm-chip-green {
    background: rgba(0, 230, 118, 0.11);
    border: 1px solid rgba(0, 230, 118, 0.30);
    color: #69F0AE;
}

/* ===== DAREBEE-STYLE 7-DAY PROGRAM POSTER GRID ===== */
.fm-poster-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 0.55rem;
    margin: 0.8rem 0 0.4rem 0;
}

@media (max-width: 980px) {
    .fm-poster-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

.fm-day-tile {
    background: #0D0E13;
    border: 1px solid var(--fm-border);
    border-radius: 12px;
    padding: 0.75rem 0.7rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 118px;
}

.fm-day-tile-high { border-top: 3px solid var(--fm-orange); }
.fm-day-tile-mod  { border-top: 3px solid var(--fm-cyan); }
.fm-day-tile-low  { border-top: 3px solid var(--fm-green); }
.fm-day-tile-rest { border-top: 3px solid #3F3F46; opacity: 0.85; }

.fm-day-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #A1A1AA;
}

.fm-day-title {
    font-size: 0.80rem;
    font-weight: 700;
    color: #FAFAFA;
    line-height: 1.28;
    margin: 0.32rem 0;
}

.fm-day-meta {
    font-size: 0.70rem;
    font-weight: 600;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ===== NATIVE STREAMLIT WIDGET OVERRIDES (SEAMLESS SAAS LOOK) ===== */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--fm-surface) !important;
    border: 1px solid var(--fm-border) !important;
    border-radius: 16px !important;
    padding: 0.25rem 0.35rem !important;
    transition: border-color 0.2s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(255, 255, 255, 0.16) !important;
}

[data-testid="stMetric"] {
    background: var(--fm-surface) !important;
    border: 1px solid var(--fm-border) !important;
    border-radius: 14px !important;
    padding: 0.95rem 1.1rem !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    color: #71717A !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.95rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
}

/* Primary & Secondary CTA Buttons */
div.stButton > button[kind="primary"],
div.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FC4C02 0%, #E03E00 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 4px 16px rgba(252, 76, 2, 0.25) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(252, 76, 2, 0.40) !important;
}

div.stButton > button[kind="secondary"] {
    background: var(--fm-surface-2) !important;
    color: #E4E4E7 !important;
    border: 1px solid var(--fm-border-strong) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

div.stButton > button[kind="secondary"]:hover {
    background: var(--fm-surface-hover) !important;
    border-color: rgba(255, 255, 255, 0.30) !important;
    color: #FFFFFF !important;
}

/* Sleek Tabs */
button[data-baseweb="tab"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #9CA3AF !important;
    padding: 0.6rem 1.1rem !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: var(--fm-orange) !important;
    height: 3px !important;
    border-radius: 99px !important;
}

/* Expanders */
details[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid var(--fm-border) !important;
    border-radius: 12px !important;
}

/* Progress bar */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--fm-orange), var(--fm-green)) !important;
    border-radius: 99px !important;
}

/* Safety Notice Box */
.fm-safety-box {
    background: rgba(255, 176, 32, 0.06);
    border: 1px solid rgba(255, 176, 32, 0.24);
    border-left: 3px solid var(--fm-amber);
    border-radius: 12px;
    padding: 0.9rem 1.15rem;
    margin-top: 1.6rem;
    color: #FDE68A;
    font-size: 0.84rem;
    line-height: 1.55;
}

.fm-safety-box strong {
    color: var(--fm-amber);
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--fm-border);
    border-radius: 12px;
    overflow: hidden;
}
</style>
"""


def inject_custom_css() -> None:
    """Inject the WHOOP × Strava × Nike × GOWOD design system CSS."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
