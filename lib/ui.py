"""Global BanterONE theme — Banter FY26 rebrand palette + dark/light modes.

- Wordmark: Instrument Serif (matches the new Banter logo character).
- Body: DM Sans (clean editorial pairing).
- Accent: lime chartreuse #D5E547 (Banter's new brand accent).
- Dark:  near-black bg, cream text, lime accents.
- Light: cream bg, near-black text, lime accents.
"""
from __future__ import annotations
import streamlit as st


FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Instrument+Serif:ital@0;1&"
    "family=DM+Sans:wght@400;500;600;700;800&display=swap');"
)


def _theme_vars(mode: str) -> str:
    if mode == "light":
        # "Light" = softer dark gray (still very dark, still lime accents).
        # User: not charcoal, not bright — dark-medium gray that shows the green.
        return """
        --bg: #2A2A2A;
        --bg-2: #333333;
        --panel: #3A3A3A;
        --panel-2: #444444;
        --text: #F5F3EE;
        --text-dim: #B8B8B8;
        --border: rgba(245,243,238,0.10);
        --border-strong: rgba(213,229,71,0.35);
        --lime: #D5E547;
        --lime-2: #E4F26A;
        --lime-dim: #A8B937;
        --ink: #0B0B0B;
        --cream: #FBF8F1;
        --shadow-glow: 0 0 32px rgba(213,229,71,0.28);
        """
    return """
    --bg: #000000;
    --bg-2: #0B0B0B;
    --panel: #111111;
    --panel-2: #1A1A1A;
    --text: #F5F3EE;
    --text-dim: #8B8B8B;
    --border: rgba(245,243,238,0.10);
    --border-strong: rgba(213,229,71,0.35);
    --lime: #D5E547;
    --lime-2: #E4F26A;
    --lime-dim: #A8B937;
    --ink: #0B0B0B;
    --cream: #FBF8F1;
    --shadow-glow: 0 0 40px rgba(213,229,71,0.22);
    """


def _base_css(mode: str) -> str:
    return f"""
<style>
{FONT_IMPORT}
:root {{ {_theme_vars(mode)} }}

html, body, [data-testid="stAppViewContainer"] {{
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg) !important;
  color: var(--text);
}}
html, body {{
  margin: 0 !important;
  padding: 0 !important;
  min-height: 100vh !important;
  overflow-x: hidden !important;
}}
[data-testid="stAppViewContainer"] {{
  background:
    radial-gradient(ellipse at 50% -10%, rgba(213,229,71,0.10) 0%, transparent 40%),
    var(--bg) !important;
  min-height: 100vh !important;
}}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer {{
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
}}
[data-testid="stMain"] {{
  padding: 0 0 120px 0 !important;
  min-height: 100vh !important;
}}
[data-testid="stMainBlockContainer"],
.block-container {{
  max-width: none !important;
  width: 100% !important;
  padding: 10px clamp(12px, 2.6vw, 42px) 0 !important;
}}
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {{
  display: none !important;
}}
@media (max-width: 760px) {{
  [data-testid="stMainBlockContainer"],
  .block-container {{
    padding-left: 10px !important;
    padding-right: 10px !important;
  }}
  [data-testid="stMain"] {{
    padding-bottom: 104px !important;
  }}
}}

/* Major headers = lime italic serif — matching the "Banter" wordmark on the masthead.
   !important defeats Streamlit default bold on h3 which triggers synthetic-bold
   rendering of Instrument Serif (only ships in weight 400) and looks chunky. */
h1, h2, h3,
[data-testid="stMarkdown"] h1,
[data-testid="stMarkdown"] h2,
[data-testid="stMarkdown"] h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
  font-family: 'Instrument Serif', 'Cormorant Garamond', Georgia, serif !important;
  font-style: italic !important;
  font-weight: 400 !important;
  letter-spacing: -0.015em !important;
  color: var(--text) !important;
}}
h1, [data-testid="stMarkdown"] h1 {{ font-size: 48px !important; line-height: 1 !important; }}
h2, [data-testid="stMarkdown"] h2 {{ font-size: 36px !important; line-height: 1.05 !important; }}
h3, [data-testid="stMarkdown"] h3 {{ font-size: 30px !important; line-height: 1.1 !important; }}
h4 {{
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--text-dim);
}}
p, div, span, li, label {{ color: var(--text); font-family: 'DM Sans', sans-serif; }}

/* ── Masthead (end-to-end BanterONE header) ─────────────────────────────── */
.masthead-brand {{
  font-family: 'Instrument Serif', Georgia, serif;
  font-weight: 400;
  font-size: clamp(56px, 9vw, 96px);
  letter-spacing: -0.028em;
  line-height: 0.95;
  color: var(--text);
  text-align: center;
  margin: 12px 0 4px 0;
}}
.masthead-brand em {{ font-style: italic; color: var(--lime); font-weight: 400; }}
.masthead-sub {{
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: var(--text-dim);
  text-align: center;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  margin: 0 0 20px 0;
}}
.masthead-sub b {{ color: var(--text); }}
.hub-user {{ color: var(--text-dim); font-size: 13px; text-align: right; }}
.hub-user b {{ color: var(--text); }}

/* ── Store badge (Home Feed) ────────────────────────────────────────────── */
.store-badge {{
  position: relative;
  padding: 22px 26px 22px 30px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(213,229,71,0.10) 0%, var(--panel) 60%);
  border: 1px solid var(--border);
  backdrop-filter: blur(12px);
  overflow: hidden;
  margin-bottom: 18px;
  cursor: pointer;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}}
.store-badge:hover {{
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.4), 0 0 20px rgba(213,229,71,0.18);
  border-color: rgba(213,229,71,0.35);
}}
/* Full-badge clickable overlay — CSS grid places button + markdown in the SAME
   cell so the invisible button fills the visible badge exactly. */
.st-key-clickable_badge_container {{
  display: grid !important;
  grid-template-columns: 1fr !important;
  grid-template-rows: 1fr !important;
}}
.st-key-clickable_badge_container > * {{
  grid-column: 1 !important;
  grid-row: 1 !important;
  width: 100% !important;
}}
.st-key-clickable_badge_container [data-testid="stElementContainer"]:has([data-testid="stButton"]) {{
  z-index: 20 !important;
}}
.st-key-clickable_badge_container [data-testid="stButton"],
.st-key-clickable_badge_container [data-testid="stButton"] button {{
  width: 100% !important;
  height: 100% !important;
  min-height: 220px !important;
}}
.st-key-clickable_badge_container [data-testid="stButton"] button {{
  background: transparent !important;
  border: none !important;
  opacity: 0 !important;
  cursor: pointer !important;
  padding: 0 !important;
  border-radius: 22px !important;
  box-shadow: none !important;
  transform: none !important;
}}
.st-key-clickable_badge_container [data-testid="stButton"] button:hover {{
  transform: none !important;
  background: transparent !important;
  box-shadow: none !important;
}}

/* Feed post: entire card clickable → Arena tab */
[class*="st-key-clickable_post_"] {{
  display: grid !important;
  grid-template-columns: 1fr !important;
  grid-template-rows: 1fr !important;
  cursor: pointer;
}}
[class*="st-key-clickable_post_"] > * {{
  grid-column: 1 !important;
  grid-row: 1 !important;
  width: 100% !important;
}}
[class*="st-key-clickable_post_"] [data-testid="stElementContainer"]:has([data-testid="stButton"]) {{
  z-index: 20 !important;
}}
[class*="st-key-clickable_post_"] [data-testid="stButton"],
[class*="st-key-clickable_post_"] [data-testid="stButton"] button {{
  width: 100% !important;
  height: 100% !important;
  min-height: 120px !important;
}}
[class*="st-key-clickable_post_"] [data-testid="stButton"] button {{
  background: transparent !important;
  border: none !important;
  opacity: 0 !important;
  cursor: pointer !important;
  padding: 0 !important;
  border-radius: 16px !important;
  box-shadow: none !important;
  transform: none !important;
}}
[class*="st-key-clickable_post_"] [data-testid="stButton"] button:hover {{
  transform: none !important;
  background: transparent !important;
  box-shadow: none !important;
}}
[class*="st-key-clickable_post_"] .feed-post {{
  transition: transform .15s ease, border-color .15s ease;
}}
[class*="st-key-clickable_post_"]:hover .feed-post {{
  transform: translateY(-1px);
  border-color: rgba(213,229,71,0.25) !important;
}}

/* Feed reaction chips: small pill buttons under each post */
[class*="st-key-reactions_"] {{
  margin-top: -8px !important;
  margin-bottom: 14px !important;
  padding: 0 6px !important;
}}
[class*="st-key-reactions_"] .stButton button {{
  padding: 4px 12px !important;
  min-height: auto !important;
  height: auto !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  border-radius: 999px !important;
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(213,229,71,0.15) !important;
  color: var(--text) !important;
  transition: all .15s ease;
}}
[class*="st-key-reactions_"] .stButton button:hover {{
  background: rgba(213,229,71,0.10) !important;
  border-color: var(--lime) !important;
  color: var(--lime) !important;
  transform: translateY(-1px);
}}
.store-badge-arrow {{
  color: var(--lime); font-size: 22px; opacity: 0.55;
  transition: opacity .18s ease, transform .18s ease;
}}
.store-badge:hover .store-badge-arrow {{ opacity: 1; transform: translateX(4px); }}
.store-badge::before {{
  content: ""; position: absolute; top: 0; bottom: 0; left: 0; width: 5px;
  background: linear-gradient(180deg, var(--lime-2), var(--lime-dim));
  border-radius: 5px 0 0 5px;
}}
.store-badge-top {{
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 4px;
}}
.store-badge-id {{
  font-family: 'DM Sans', sans-serif; font-weight: 800;
  font-size: 12px; letter-spacing: 0.32em;
  color: var(--lime);
}}
.store-badge-diamond {{ font-size: 20px; opacity: 0.75; }}
.store-badge-name {{
  font-family: 'Instrument Serif', Georgia, serif;
  font-style: italic;
  font-weight: 400; font-size: 34px; letter-spacing: -0.02em;
  color: var(--text); margin-bottom: 3px; line-height: 1;
}}
.store-badge-mall {{ font-size: 13px; color: var(--text-dim); margin-bottom: 14px; }}
.store-badge-emp {{
  display: flex; align-items: center; gap: 12px;
  padding-top: 12px; border-top: 1px solid var(--border);
}}
.store-badge-avatar {{
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--lime), var(--lime-2));
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; color: var(--ink); font-size: 15px;
  font-family: 'DM Sans', sans-serif;
}}
.store-badge-emp-name {{ font-weight: 700; color: var(--text); font-size: 15px; }}
.store-badge-emp-role {{ color: var(--text-dim); font-size: 12px; }}

/* ── Perf island + glass cards ──────────────────────────────────────────── */
.perf-island {{
  padding: 26px; border-radius: 24px;
  background: linear-gradient(135deg, rgba(213,229,71,0.10), var(--panel));
  border: 1px solid var(--border);
  animation: pulseGlow 4s ease-in-out infinite;
}}
@keyframes pulseGlow {{
  0%, 100% {{ box-shadow: 0 0 20px rgba(213,229,71,0.10); }}
  50%      {{ box-shadow: 0 0 48px rgba(213,229,71,0.35); }}
}}
.glass-card {{
  padding: 20px; border-radius: 18px;
  background: var(--panel);
  border: 1px solid var(--border);
  backdrop-filter: blur(8px);
}}

/* ── Buttons (default): all black with lime accents ─────────────────────── */
.stButton button {{
  background: #000000 !important;
  color: var(--text) !important;
  border: 1px solid rgba(213,229,71,0.28) !important;
  border-radius: 12px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  transition: all .15s ease;
}}
.stButton button:hover {{
  background: #0B0B0B !important;
  border-color: var(--lime) !important;
  color: var(--lime) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(213,229,71,0.18);
}}
.stButton button[kind="primary"] {{
  background: linear-gradient(135deg, var(--lime), var(--lime-2)) !important;
  color: #0B0B0B !important;
  border: none !important;
}}

/* ── Bottom Nav Island (Apple-Music-inspired: sleek, round, lime dividers) */
.st-key-bottom_nav {{
  position: fixed !important;
  bottom: 22px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background: rgba(0,0,0,0.92);
  border: 1px solid rgba(213,229,71,0.32);
  border-radius: 999px;
  padding: 6px 10px;
  backdrop-filter: blur(28px);
  box-shadow:
    0 24px 60px rgba(0,0,0,0.55),
    0 0 40px rgba(213,229,71,0.20),
    inset 0 1px 0 rgba(255,255,255,0.04);
  width: auto !important;
  max-width: 96vw;
}}
.st-key-bottom_nav [data-testid="stHorizontalBlock"] {{
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  gap: 0 !important;
  align-items: center !important;
  width: auto !important;
}}
.st-key-bottom_nav [data-testid="stColumn"] {{
  min-width: 0 !important;
  width: auto !important;
  flex: 0 0 auto !important;
  padding: 0 !important;
  position: relative;
}}
/* Neon lime vertical spacer between tabs */
.st-key-bottom_nav [data-testid="stColumn"]:not(:last-child)::after {{
  content: "";
  position: absolute;
  right: 0;
  top: 26%;
  bottom: 26%;
  width: 1px;
  background: linear-gradient(180deg, transparent 0%, #D5E547 50%, transparent 100%);
  opacity: 0.65;
  box-shadow: 0 0 6px #D5E547, 0 0 12px rgba(213,229,71,0.45);
  pointer-events: none;
}}
.st-key-bottom_nav [data-testid="stElementContainer"] {{ margin: 0 !important; }}
.st-key-bottom_nav .stButton {{ margin: 0 !important; }}
.st-key-bottom_nav .stButton button {{
  background: transparent !important;
  color: var(--lime) !important;
  border: none !important;
  border-radius: 999px !important;
  padding: 9px 18px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em !important;
  min-width: auto !important;
  white-space: nowrap !important;
  height: auto !important;
  line-height: 1.1 !important;
  transition: color .18s ease, background .18s ease;
  box-shadow: none !important;
  transform: none !important;
}}
.st-key-bottom_nav .stButton button p {{ color: var(--lime) !important; }}
.st-key-bottom_nav .stButton button:hover {{
  color: var(--lime-2) !important;
  background: rgba(213,229,71,0.08) !important;
  transform: none !important;
  box-shadow: none !important;
}}
.st-key-bottom_nav .stButton button:hover p {{ color: var(--lime-2) !important; }}
.st-key-bottom_nav .stButton button[kind="primary"],
.st-key-bottom_nav .stButton button[kind="primary"] p,
.st-key-bottom_nav .stButton button[kind="primary"] div,
.st-key-bottom_nav .stButton button[kind="primary"] * {{
  background: linear-gradient(135deg, var(--lime), var(--lime-2)) !important;
  color: #000000 !important;
  font-weight: 800 !important;
  box-shadow: 0 4px 16px rgba(213,229,71,0.42) !important;
}}
.st-key-bottom_nav .stButton button[kind="primary"] p {{
  background: transparent !important;
  box-shadow: none !important;
}}

/* ── Center "B" — branded profile mark ─────────────────────────────────── */
.st-key-bottom_nav [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) .stButton button,
.st-key-bottom_nav [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) .stButton button p {{
  font-family: 'Instrument Serif', Georgia, serif !important;
  font-style: italic !important;
  font-weight: 400 !important;
  font-size: 24px !important;
  letter-spacing: -0.01em !important;
  -webkit-text-stroke: 0.35px currentColor !important;
  text-shadow: 0 0 0 currentColor, 0 0 12px rgba(213,229,71,0.28) !important;
}}
.st-key-bottom_nav [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) .stButton button {{
  padding-left: 22px !important;
  padding-right: 22px !important;
}}

/* Ensure light mode overrides the dark nav bg */
:root[data-theme="light"] .st-key-bottom_nav,
body[data-theme="light"] .st-key-bottom_nav {{
  background: rgba(11,11,11,0.92);
}}

/* ── Feed post cards ────────────────────────────────────────────────────── */
.feed-post {{
  padding: 16px 20px;
  border-radius: 16px;
  background: var(--panel);
  border: 1px solid var(--border);
  margin-bottom: 12px;
}}
.feed-post.pinned {{
  border: 1px solid var(--lime);
  background: linear-gradient(135deg, rgba(213,229,71,0.08), var(--panel));
}}
.feed-post-head {{
  display: flex; align-items: center; gap: 10px; margin-bottom: 8px;
}}
.feed-post-author {{ font-weight: 700; color: var(--text); font-size: 14px; }}
.feed-post-time {{ color: var(--text-dim); font-size: 12px; }}
.feed-post-pin {{
  color: var(--lime); font-size: 11px; font-weight: 800;
  letter-spacing: 0.14em; margin-left: auto;
}}
.feed-post-body {{ color: var(--text); font-size: 14px; line-height: 1.5; }}
.feed-post-body b {{ color: var(--lime); }}
.feed-post-reacts {{
  margin-top: 10px; display: flex; gap: 10px;
  color: var(--text-dim); font-size: 12px;
}}
.feed-post-reacts span {{ background: var(--panel-2); padding: 3px 8px; border-radius: 999px; }}

/* ── Tabs (for nested tabs inside content, e.g. leaderboard) ────────────── */
[data-testid="stTabs"] button {{ font-family: 'DM Sans', sans-serif; font-weight: 600; }}
[data-testid="stTabs"] button[aria-selected="true"] {{
  color: var(--lime) !important;
  border-bottom-color: var(--lime) !important;
}}

/* ── Popover (settings) ─────────────────────────────────────────────────── */
[data-testid="stPopover"] button {{
  background: #000000 !important;
  color: var(--text) !important;
  border: 1px solid rgba(213,229,71,0.28) !important;
  border-radius: 12px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  padding: 8px 14px !important;
  min-height: 36px !important;
}}
[data-testid="stPopover"] button:hover {{
  border-color: var(--lime) !important;
  color: var(--lime) !important;
}}
[data-testid="stPopover"] button svg {{ color: var(--lime) !important; }}
/* Popover content: compact */
[data-baseweb="popover"] > div,
[data-testid="stPopoverContent"], [data-testid="stPopoverBody"] {{
  background: #0B0B0B !important;
  border: 1px solid rgba(213,229,71,0.28) !important;
  border-radius: 14px !important;
  padding: 14px !important;
  min-width: 220px !important;
  max-width: 280px !important;
}}
[data-testid="stPopoverContent"] [data-testid="stVerticalBlock"] {{
  gap: 8px !important;
}}
[data-testid="stPopoverContent"] p {{
  margin: 0 0 4px 0 !important;
  font-size: 11px !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: var(--text-dim) !important;
}}
[data-testid="stPopoverContent"] hr {{ margin: 6px 0 !important; border-color: rgba(213,229,71,0.15) !important; }}
[data-testid="stPopoverContent"] label {{ font-size: 12px !important; }}

/* ── Fixed round gear icon top-right ───────────────────────────────────── */
.st-key-settings_gear {{
  position: fixed !important;
  top: 14px;
  right: 14px;
  z-index: 900;
  width: 44px !important;
  max-width: 44px !important;
}}
.st-key-settings_gear [data-testid="stPopover"] > div,
.st-key-settings_gear [data-testid="stElementContainer"] {{
  width: 44px !important;
  min-width: 44px !important;
  margin: 0 !important;
}}
.st-key-settings_gear [data-testid="stPopover"] button {{
  width: 44px !important;
  height: 44px !important;
  min-width: 44px !important;
  padding: 0 !important;
  border-radius: 50% !important;
  font-size: 18px !important;
  background: #000000 !important;
  color: var(--lime) !important;
  border: 1px solid rgba(213,229,71,0.42) !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.55), 0 0 20px rgba(213,229,71,0.18);
}}
.st-key-settings_gear [data-testid="stPopover"] button:hover {{
  color: var(--lime-2) !important;
  border-color: var(--lime) !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.55), 0 0 28px rgba(213,229,71,0.42);
}}
/* Hide the popover chevron so it's a clean icon-only button */
.st-key-settings_gear [data-testid="stPopover"] button svg,
.st-key-settings_gear [data-testid="stPopover"] button [data-testid="stIconMaterial"] {{
  display: none !important;
}}

/* ── Radio dots + toggle knob → lime (override Streamlit primary) ───────── */
[data-baseweb="radio"] div[role="radio"][aria-checked="true"] {{
  border-color: var(--lime) !important;
  background-color: transparent !important;
}}
[data-baseweb="radio"] div[role="radio"][aria-checked="true"] > div {{
  background-color: var(--lime) !important;
}}
[data-baseweb="radio"] div[role="radio"] {{ border-color: rgba(213,229,71,0.5) !important; }}
/* Toggle */
[data-baseweb="checkbox"] [role="checkbox"][aria-checked="true"],
[data-testid="stCheckbox"] label > div[data-baseweb="checkbox"] > div[aria-checked="true"] {{
  background-color: var(--lime) !important;
  border-color: var(--lime) !important;
}}
label[data-baseweb="checkbox"] > div:first-child {{ background: var(--panel-2) !important; }}
label[data-baseweb="checkbox"] > div[aria-checked="true"] {{ background: var(--lime) !important; }}
/* Toggle track (st.toggle) */
[data-testid="stToggle"] label > div > div[role="switch"] {{ background: rgba(213,229,71,0.15) !important; }}
[data-testid="stToggle"] label > div > div[role="switch"][aria-checked="true"] {{ background: var(--lime) !important; }}
[data-testid="stToggle"] label > div > div[role="switch"] > div {{ background: var(--text) !important; }}
[data-testid="stToggle"] label > div > div[role="switch"][aria-checked="true"] > div {{ background: var(--ink) !important; }}

/* ── Weekly Targets editor: pure black inputs, lime-glow save ───────────── */
.st-key-weekly_targets_editor [data-testid="stNumberInput"] {{
  background: #000000 !important;
  border-radius: 12px !important;
  border: 1px solid rgba(213,229,71,0.20) !important;
  padding: 4px !important;
}}
.st-key-weekly_targets_editor [data-testid="stNumberInput"] input,
.st-key-weekly_targets_editor [data-testid="stNumberInput"] [data-baseweb="input"],
.st-key-weekly_targets_editor [data-testid="stNumberInput"] > div,
.st-key-weekly_targets_editor [data-testid="stNumberInput"] > div > div {{
  background: #000000 !important;
  color: var(--text) !important;
  border-color: transparent !important;
}}
.st-key-weekly_targets_editor [data-testid="stNumberInput"] button {{
  background: #000000 !important;
  color: var(--lime) !important;
  border: none !important;
}}
.st-key-weekly_targets_editor label {{ color: var(--lime) !important;
  font-size: 11px !important; letter-spacing: 0.16em !important;
  text-transform: uppercase !important; font-weight: 700 !important; }}
.st-key-weekly_targets_editor .stButton button[kind="primary"],
.st-key-weekly_targets_editor .stButton button[kind="primary"] p,
.st-key-weekly_targets_editor .stButton button[kind="primary"] * {{
  background: linear-gradient(135deg, var(--lime), var(--lime-2)) !important;
  color: #000000 !important;
  border: none !important;
  font-weight: 800 !important;
  box-shadow: 0 8px 24px rgba(213,229,71,0.32);
}}
.st-key-weekly_targets_editor .stButton button[kind="primary"] p {{
  background: transparent !important;
  box-shadow: none !important;
  height: auto !important;
}}
.st-key-weekly_targets_editor .stButton button[kind="primary"] {{ height: 48px !important; }}

/* Banter Buddy customizer: lime primary button with readable black text */
.st-key-avatar_customizer .stButton button[kind="primary"],
.st-key-avatar_customizer .stButton button[kind="primary"] p,
.st-key-avatar_customizer .stButton button[kind="primary"] * {{
  color: #000000 !important;
  font-weight: 800 !important;
}}
.st-key-avatar_customizer .stButton button[kind="primary"] p {{
  background: transparent !important;
}}

/* Playbook search — pure black bg */
.st-key-playbook_search_wrap [data-testid="stTextInput"] input {{
  background: #000000 !important;
  color: var(--text) !important;
  border: 1px solid rgba(213,229,71,0.28) !important;
  border-radius: 12px !important;
  padding: 12px 16px !important;
  font-size: 14px !important;
}}
.st-key-playbook_search_wrap [data-testid="stTextInput"] input:focus {{
  border-color: var(--lime) !important;
  box-shadow: 0 0 0 2px rgba(213,229,71,0.25) !important;
}}

/* File uploader accent */
[data-testid="stFileUploader"] section {{
  border-color: rgba(213,229,71,0.28) !important;
  background: transparent !important;
}}
[data-testid="stFileUploader"] section:hover {{ border-color: var(--lime) !important; }}
</style>
"""


def inject_theme() -> None:
    mode = st.session_state.get("theme", "dark")
    st.markdown(_base_css(mode), unsafe_allow_html=True)


def render_header() -> None:
    user = st.session_state.user
    # Settings gear — fixed top-right via CSS on .st-key-settings_gear
    with st.container(key="settings_gear"):
        _render_settings_popover()
    # Full-width centered masthead + subtitle
    st.markdown(
        '<div class="masthead-brand"><em>Banter</em>ONE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="masthead-sub">'
        f'<b>{user["full_name"]}</b> · Store <b>{user["store_id"]}</b> · <b>{user["role"]}</b>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_settings_popover() -> None:
    with st.popover("⚙", use_container_width=True):
        current_theme = st.session_state.get("theme", "dark")
        theme = st.radio(
            "Theme",
            options=["Dark", "Light"],
            horizontal=True,
            index=0 if current_theme == "dark" else 1,
        )
        sound = st.toggle(
            "Click sound",
            value=st.session_state.get("sound_enabled", True),
        )
        if st.button("Sign out", use_container_width=True):
            from . import auth
            auth.logout()

        theme_val = theme.lower()
        changed = (theme_val != current_theme
                   or sound != st.session_state.get("sound_enabled", True))
        if changed:
            st.session_state.theme = theme_val
            st.session_state.sound_enabled = sound
            st.rerun()


def _character_img(user: dict, size: int) -> str:
    """Return the user's Banter Buddy creature chip."""
    from . import buddy
    profile = buddy.load_profile(user.get("email", "banterone@local"))
    starter = profile.get("starter") or "spark"
    stage_index, _ = buddy.stage_for(user, profile)
    meta = buddy.STARTERS.get(starter, buddy.STARTERS["spark"])
    creature = buddy.render_creature(starter, stage_index, size=max(54, size * 2))
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;'
        f'overflow:hidden;background:radial-gradient(circle at 50% 35%, {meta["accent"]}44 0%, #000 70%);'
        f'border:2px solid var(--lime);box-shadow:0 0 12px rgba(213,229,71,0.35);'
        f'display:flex;align-items:center;justify-content:center;">'
        f'<div style="width:{int(size * 1.8)}px;height:{int(size * 1.8)}px;'
        f'display:flex;align-items:center;justify-content:center;">{creature}</div></div>'
    )


def _resolve_avatar_mode(user: dict) -> str:
    """Pick which representation the user wants: 'photo', 'character', or 'initials'.
    Falls back to 'auto' logic if the user hasn't chosen explicitly."""
    mode = (user.get("avatar_mode") or "").strip().lower()
    if mode in ("photo", "character", "initials"):
        return mode
    # Auto: prefer whatever the user has set up.
    from pathlib import Path
    url = user.get("avatar_url")
    if isinstance(url, str) and url and Path(url).exists():
        return "photo"
    if isinstance(user.get("gender"), str) and user.get("gender"):
        return "character"
    return "initials"


def _avatar_html(user: dict, size: int = 40) -> str:
    """Return an avatar chip: photo, Banter Buddy, or initials — user's choice."""
    import base64
    from pathlib import Path
    mode = _resolve_avatar_mode(user)

    if mode == "photo":
        url = user.get("avatar_url")
        if isinstance(url, str) and url:
            path = Path(url)
            if path.exists() and path.is_file():
                try:
                    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
                    b64 = base64.b64encode(path.read_bytes()).decode()
                    return (
                        f'<img src="data:{mime};base64,{b64}" '
                        f'style="width:{size}px;height:{size}px;border-radius:50%;'
                        f'object-fit:cover;border:2px solid var(--lime);" />'
                    )
                except Exception:
                    pass  # fall through to initials

    if mode == "character":
        return _character_img(user, size)

    # initials fallback
    name = user.get("full_name", "?")
    initials = "".join(p[0] for p in str(name).split()[:2]).upper() or "?"
    font = max(11, int(size * 0.38))
    return (
        f'<div class="store-badge-avatar" '
        f'style="width:{size}px;height:{size}px;font-size:{font}px;">'
        f'{initials}</div>'
    )


def render_store_badge() -> None:
    from . import db
    user = st.session_state.user
    name = user["full_name"]
    role = user["role"]

    if user["store_id"] == "DISTRICT":
        store_id_line = "DISTRICT"
        store_name = "All 11 Stores"
        mall_line = "Colorado · New Mexico"
    else:
        try:
            stores = db.read("stores")
            row = stores[stores["store_id"].astype(str) == str(user["store_id"])].iloc[0]
            store_id_line = f"STORE {row['store_id']}"
            store_name = str(row["store_name"])
            mall_line = f"{row['mall']} · {row['city']}, {row['state']}"
        except (IndexError, KeyError, FileNotFoundError):
            store_id_line = f"STORE {user['store_id']}"
            store_name = "—"
            mall_line = ""

    avatar = _avatar_html(user, size=44)
    # Wrap in a keyed container so we can overlay a transparent button that
    # captures clicks anywhere on the badge and routes to the Store tab.
    with st.container(key="clickable_badge_container"):
        if st.button(" ", key="badge_click_to_me", help="Open Bantagachi"):
            st.session_state["current_tab"] = "me"
            st.rerun()
        st.markdown(
            (
                '<div class="store-badge">'
                '<div class="store-badge-top">'
                f'<div class="store-badge-id">{store_id_line}</div>'
                '<div class="store-badge-arrow">→</div>'
                '</div>'
                f'<div class="store-badge-name">{store_name}</div>'
                f'<div class="store-badge-mall">{mall_line}</div>'
                '<div class="store-badge-emp">'
                f'{avatar}'
                '<div>'
                f'<div class="store-badge-emp-name">{name}</div>'
                f'<div class="store-badge-emp-role">{role}</div>'
                '</div>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


NAV_ITEMS = [
    ("home",     "Home"),
    ("store",    "Store"),
    ("me",       "B"),          # center — Bantagachi mark, Instrument Serif italic
    ("playbook", "Playbook"),
    ("arena",    "Arena"),
]


def render_bottom_nav() -> None:
    """Fixed floating island navigation. Sets st.session_state.current_tab."""
    current = st.session_state.get("current_tab", "home")
    with st.container(key="bottom_nav"):
        cols = st.columns(len(NAV_ITEMS))
        for col, (key, label) in zip(cols, NAV_ITEMS):
            with col:
                is_active = current == key
                btn_type = "primary" if is_active else "secondary"
                if st.button(label, key=f"nav_{key}", type=btn_type,
                             use_container_width=True):
                    st.session_state.current_tab = key
                    st.rerun()


def maybe_play_click_sound() -> None:
    """If the current tab changed since last render and sound is on,
    emit a Web-Audio click. Idempotent per render."""
    import streamlit.components.v1 as components
    current = st.session_state.get("current_tab", "home")
    last = st.session_state.get("_last_tab", None)
    if last is None:
        st.session_state._last_tab = current
        return
    if last == current:
        return
    st.session_state._last_tab = current
    if not st.session_state.get("sound_enabled", True):
        return
    # Real mouse click = short broadband noise burst with fast decay (not a tone).
    components.html(
        """
        <script>
        (function() {
          try {
            const Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            const ctx = new Ctx();
            const dur = 0.018;              // 18ms — clicky, not beepy
            const size = Math.floor(ctx.sampleRate * dur);
            const buf = ctx.createBuffer(1, size, ctx.sampleRate);
            const data = buf.getChannelData(0);
            for (let i = 0; i < size; i++) {
              const t = i / size;
              // white noise * fast exponential decay + slight low-pass via averaging
              data[i] = (Math.random() * 2 - 1) * Math.exp(-t * 14);
            }
            const src = ctx.createBufferSource();
            src.buffer = buf;
            const g = ctx.createGain();
            g.gain.value = 0.09;             // subtle
            // Soft high-cut so it sounds warmer, less "hiss"
            const lp = ctx.createBiquadFilter();
            lp.type = 'lowpass';
            lp.frequency.value = 4200;
            src.connect(lp); lp.connect(g); g.connect(ctx.destination);
            src.start();
          } catch(e) {}
        })();
        </script>
        """,
        height=0,
    )
