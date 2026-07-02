"""BanterONE — main entry point.

Custom bottom-nav routing. `st.session_state.current_tab` picks the view.
"""
import streamlit as st

from lib import auth, db, ui
from tabs import home, my_store, leaderboard, playbook, me_tab

st.set_page_config(
    page_title="BanterONE",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 48-hour TTL purge on cold start.
db.purge_feed_older_than(48)

# ── Session defaults ─────────────────────────────────────────────────────────
st.session_state.setdefault("current_tab", "home")
st.session_state.setdefault("theme", "dark")
st.session_state.setdefault("sound_enabled", True)

# ── Theme shell ──────────────────────────────────────────────────────────────
ui.inject_theme()

# ── Auth gate ────────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    auth.restore_remembered_user()

if "user" not in st.session_state:
    auth.render_login_page()
    st.stop()

# ── Header ──────────────────────────────────────────────────────────────────
ui.render_header()

# ── Tab dispatch (no st.tabs — custom bottom nav owns routing) ──────────────
tab = st.session_state.current_tab
if   tab == "home":     home.render()
elif tab == "store":    my_store.render()
elif tab == "arena":    leaderboard.render()
elif tab == "playbook": playbook.render()
elif tab == "me":       me_tab.render()

# ── Bottom nav + click sound ─────────────────────────────────────────────────
ui.render_bottom_nav()
ui.maybe_play_click_sound()
