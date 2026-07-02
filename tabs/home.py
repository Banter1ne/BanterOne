from datetime import date, datetime
import pandas as pd
import streamlit as st
from lib import ui, db


def render() -> None:
    ui.render_store_badge()
    _render_perf_island()
    st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)
    st.markdown("### Daily Feed")
    _render_feed()


# ── Performance Island (real numbers) ────────────────────────────────────────
def _render_perf_island() -> None:
    user = st.session_state.user
    store_id = str(user.get("store_id", ""))

    try:
        stores = db.read("stores").copy()
        stores["store_id"] = stores["store_id"].astype(str)
        district_plan = float(stores["daily_plan"].sum())
    except (FileNotFoundError, pd.errors.EmptyDataError):
        stores = pd.DataFrame()
        district_plan = 0.0

    if store_id == "DISTRICT" or store_id not in stores["store_id"].values:
        store_plan = district_plan if store_id == "DISTRICT" else 0.0
        store_name_short = "District"
    else:
        row = stores[stores["store_id"] == store_id].iloc[0]
        store_plan = float(row["daily_plan"])
        store_name_short = str(row["store_name"])

    try:
        subs = db.read("daily_submissions").copy()
        subs["timestamp"] = pd.to_datetime(subs["timestamp"])
        today_subs = subs[subs["timestamp"].dt.date == date.today()]
        today_subs["store_id"] = today_subs["store_id"].astype(str)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        today_subs = pd.DataFrame(columns=["store_id", "bold"])

    district_actual = float(today_subs["bold"].sum()) if not today_subs.empty else 0.0
    if store_id == "DISTRICT":
        store_actual = district_actual
    elif not today_subs.empty:
        store_actual = float(today_subs[today_subs["store_id"] == store_id]["bold"].sum())
    else:
        store_actual = 0.0

    district_pct = (district_actual / district_plan * 100) if district_plan else 0
    store_pct = (store_actual / store_plan * 100) if store_plan else 0

    html = (
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">'
        + _island_card("District · Today", district_actual, district_plan, district_pct)
        + _island_card(store_name_short + " · Today", store_actual, store_plan, store_pct)
        + '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def _island_card(label: str, actual: float, plan: float, pct: float) -> str:
    pct_color = "var(--lime)" if pct >= 100 else "var(--text)"
    bar_pct = min(pct, 100)
    return (
        '<div class="perf-island">'
        f'<div style="font-size:10px;letter-spacing:0.32em;color:var(--lime);font-weight:700;">{label.upper()}</div>'
        f'<div style="font-family:\'Instrument Serif\',serif;font-style:italic;font-size:44px;color:var(--text);line-height:1.05;margin-top:4px;">${actual:,.0f}</div>'
        f'<div style="color:var(--text-dim);font-size:12px;margin-top:2px;">of <b style="color:var(--text);">${plan:,.0f}</b> plan &nbsp;·&nbsp; <b style="color:{pct_color};">{pct:.0f}%</b></div>'
        '<div style="background:rgba(255,255,255,0.06);border-radius:99px;height:8px;margin-top:12px;overflow:hidden;">'
        f'<div style="background:linear-gradient(90deg,var(--lime),var(--lime-2));height:100%;width:{bar_pct:.1f}%;"></div>'
        '</div>'
        '</div>'
    )


# ── Feed ─────────────────────────────────────────────────────────────────────
def _render_feed() -> None:
    try:
        df = db.read("home_feed").copy()
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.info("No posts yet.")
        return
    if df.empty:
        st.info("No posts yet.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["is_pinned"] = df["is_pinned"].astype(str).str.lower().isin(["true", "1", "yes"])
    df = df.sort_values(["is_pinned", "timestamp"], ascending=[False, False])

    for _, row in df.iterrows():
        _render_post(row)


def _render_post(row) -> None:
    name = str(row["author_name"])
    email = str(row.get("author_email") or "")
    when = _fmt_rel(row["timestamp"])
    body = str(row["content"]).replace("<", "&lt;").replace(">", "&gt;")
    import re
    body = re.sub(r"(\$[\d,]+(?:\.\d+)?)", r"<b>\1</b>", body)
    body = re.sub(r"(Store \d+)", r"<b>\1</b>", body)

    is_system = email == "system@banter.com"
    if is_system:
        avatar_html = (
            '<div class="store-badge-avatar" '
            'style="width:34px;height:34px;font-size:14px;font-family:\'Instrument Serif\',serif;'
            'font-style:italic;background:#000;color:var(--lime);'
            'border:1px solid var(--lime);">B</div>'
        )
    else:
        avatar_html = _author_avatar_html(email, name)

    pin_tag = '<div class="feed-post-pin">PINNED</div>' if row["is_pinned"] else ""
    cls = "feed-post pinned" if row["is_pinned"] else "feed-post"

    post_id = str(row.get("post_id") or f"p_{when}")

    with st.container(key=f"feed_post_{post_id}"):
        st.markdown(
            f"""
            <div class="{cls}">
              <div class="feed-post-head">
                {avatar_html}
                <div>
                  <div class="feed-post-author">{name}</div>
                  <div class="feed-post-time">{when}</div>
                </div>
                {pin_tag}
              </div>
              <div class="feed-post-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_reactions(post_id, row)


def _render_reactions(post_id: str, row) -> None:
    """4 clickable reaction chips. Click increments the count in home_feed.csv."""
    likes  = int(row.get("likes", 0) or 0)
    laughs = int(row.get("laughs", 0) or 0)
    fires  = int(row.get("fires", 0) or 0)
    party  = int(row.get("party", 0) or 0)

    with st.container(key=f"reactions_{post_id}"):
        c1, c2, c3, c4, spacer = st.columns([1, 1, 1, 1, 6])
        with c1:
            if st.button(f"👍 {likes}", key=f"r_like_{post_id}", use_container_width=True):
                _bump(post_id, "likes"); st.rerun()
        with c2:
            if st.button(f"😂 {laughs}", key=f"r_laugh_{post_id}", use_container_width=True):
                _bump(post_id, "laughs"); st.rerun()
        with c3:
            if st.button(f"🔥 {fires}", key=f"r_fire_{post_id}", use_container_width=True):
                _bump(post_id, "fires"); st.rerun()
        with c4:
            if st.button(f"🎉 {party}", key=f"r_party_{post_id}", use_container_width=True):
                _bump(post_id, "party"); st.rerun()


def _bump(post_id: str, col: str) -> None:
    df = db.read("home_feed").copy()
    if col not in df.columns:
        df[col] = 0
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    mask = df["post_id"].astype(str) == post_id
    if mask.any():
        df.loc[mask, col] = df.loc[mask, col] + 1
        db.write("home_feed", df)


def _author_avatar_html(email: str, fallback_name: str) -> str:
    try:
        users = db.read("users")
        hit = users[users["email"].str.lower() == email.lower()]
        if not hit.empty:
            return ui._avatar_html(hit.iloc[0].to_dict(), size=34)
    except Exception:
        pass
    initials = "".join(p[0] for p in fallback_name.split()[:2]).upper() or "?"
    return (
        f'<div class="store-badge-avatar" '
        f'style="width:34px;height:34px;font-size:13px;">{initials}</div>'
    )


def _fmt_rel(ts: pd.Timestamp) -> str:
    now = datetime.now()
    delta = now - ts.to_pydatetime()
    secs = int(delta.total_seconds())
    if secs < 60:  return "just now"
    if secs < 3600:  return f"{secs // 60}m ago"
    if secs < 86400: return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"
