from datetime import date
import pandas as pd
import streamlit as st
from lib import db, ui


def render() -> None:
    ui.render_store_badge()

    st.markdown("### District Arena")

    today, monthly, ytd = st.tabs(["Today", "Monthly", "Yearly (YTD)"])
    with today:
        _render_timeframe("today")
    with monthly:
        _render_timeframe("monthly")
    with ytd:
        _render_timeframe("ytd")


def _render_timeframe(scope: str) -> None:
    st.markdown("#### Store Leaderboard")
    store_board = _build_store_board(scope)
    _render_store_table(store_board)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    st.markdown("#### Individual Leaderboard")
    sales_tab, ep_tab, esa_tab = st.tabs(["Sales", "Ear Piercings", "ESA"])
    ind = _build_individual_board(scope)
    with sales_tab:
        _render_individual_table(ind.sort_values("sales_total", ascending=False), "sales_total", "Sales", money=True)
    with ep_tab:
        _render_individual_table(ind.sort_values("piercings_count", ascending=False), "piercings_count", "Piercings", money=False)
    with esa_tab:
        _render_individual_table(ind.sort_values("esa_sales", ascending=False), "esa_sales", "ESA $", money=True)


# ── Store board ──────────────────────────────────────────────────────────────
def _build_store_board(scope: str) -> pd.DataFrame:
    try:
        stores = db.read("stores").copy()
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()

    try:
        subs = db.read("daily_submissions").copy()
        subs["timestamp"] = pd.to_datetime(subs["timestamp"])
        subs["store_id"] = subs["store_id"].astype(str)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        subs = pd.DataFrame(columns=["store_id", "timestamp", "bold"])

    # Aggregate by scope.
    if scope == "today":
        today_str = pd.Timestamp(date.today())
        agg_src = subs[subs["timestamp"].dt.date == today_str.date()]
        col_label = "Today $"
    elif scope == "monthly":
        agg_src = subs[subs["timestamp"].dt.month == date.today().month]
        col_label = "MTD $"
    else:
        agg_src = subs
        col_label = "YTD $"

    if not agg_src.empty:
        by_store = agg_src.groupby("store_id")["bold"].sum().reset_index()
    else:
        by_store = pd.DataFrame({"store_id": [], "bold": []})

    stores["store_id"] = stores["store_id"].astype(str)
    board = stores.merge(by_store, on="store_id", how="left")
    board["bold"] = board["bold"].fillna(0.0)
    board["pct_of_plan"] = (board["bold"] / (board["daily_plan"] * _plan_multiplier(scope)) * 100).round(1)
    board = board.sort_values("bold", ascending=False).reset_index(drop=True)
    board["col_label"] = col_label
    return board


def _plan_multiplier(scope: str) -> int:
    if scope == "today":  return 1
    if scope == "monthly": return date.today().day  # planned days elapsed
    return date.today().timetuple().tm_yday          # YTD days


def _render_store_table(board: pd.DataFrame) -> None:
    if board.empty:
        st.info("No store data yet.")
        return
    col_label = board["col_label"].iloc[0] if "col_label" in board else "$"
    rows_html = ""
    me_store = str(st.session_state.user.get("store_id", ""))
    for i, r in board.iterrows():
        you = ('<span style="color:var(--lime);font-weight:800;"> · YOU</span>'
               if str(r["store_id"]) == me_store else "")
        pct_style = "color:var(--lime);font-weight:800;" if r["pct_of_plan"] >= 100 else "color:var(--text-dim);"
        rows_html += (
            f'<tr style="border-top:1px solid rgba(229,228,226,0.06);">'
            f'<td style="padding:10px 12px;color:var(--text-dim);">#{i+1}</td>'
            f'<td style="padding:10px 12px;color:var(--text);font-weight:700;">{r["store_name"]}{you}</td>'
            f'<td style="padding:10px 12px;color:var(--text-dim);">{r["mall"]}</td>'
            f'<td style="padding:10px 12px;color:var(--text-dim);">Store {r["store_id"]}</td>'
            f'<td style="padding:10px 12px;text-align:right;color:var(--text);font-weight:700;">${r["bold"]:,.0f}</td>'
            f'<td style="padding:10px 12px;text-align:right;{pct_style}">{r["pct_of_plan"]:.0f}%</td>'
            f'</tr>'
        )
    st.markdown(
        f'''
        <table style="width:100%;border-collapse:collapse;margin-top:6px;">
          <thead>
            <tr style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;text-align:left;font-weight:700;">
              <th style="padding:10px 12px;">RANK</th>
              <th style="padding:10px 12px;">STORE</th>
              <th style="padding:10px 12px;">MALL</th>
              <th style="padding:10px 12px;">ID</th>
              <th style="padding:10px 12px;text-align:right;">{col_label}</th>
              <th style="padding:10px 12px;text-align:right;">% PLAN</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        ''',
        unsafe_allow_html=True,
    )


# ── Individual board ─────────────────────────────────────────────────────────
def _build_individual_board(scope: str) -> pd.DataFrame:
    try:
        m = db.read("individual_metrics").copy()
        m["date"] = pd.to_datetime(m["date"])
    except (FileNotFoundError, pd.errors.EmptyDataError):
        m = pd.DataFrame(columns=["employee_email", "date", "sales_total",
                                  "piercing_sales", "esa_sales",
                                  "piercings_count", "esa_count"])
    try:
        users = db.read("users").copy()
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()

    if scope == "today":
        m = m[m["date"].dt.date == date.today()]
    elif scope == "monthly":
        m = m[m["date"].dt.month == date.today().month]

    agg = m.groupby("employee_email", as_index=False).agg(
        sales_total=("sales_total", "sum"),
        piercing_sales=("piercing_sales", "sum"),
        esa_sales=("esa_sales", "sum"),
        piercings_count=("piercings_count", "sum"),
        esa_count=("esa_count", "sum"),
    )
    agg = agg.merge(
        users[["email", "full_name", "store_id", "role"]],
        left_on="employee_email", right_on="email", how="left",
    )
    return agg.fillna({"full_name": "—", "store_id": "—", "role": "—"})


def _render_individual_table(df: pd.DataFrame, sort_col: str,
                              value_label: str, money: bool) -> None:
    if df.empty:
        st.info("No individual metrics for this timeframe yet.")
        return
    me_email = st.session_state.user["email"].lower()
    df = df.reset_index(drop=True)
    rows_html = ""
    for i, r in df.iterrows():
        you = ('<span style="color:var(--lime);font-weight:800;"> · YOU</span>'
               if str(r.get("email", "")).lower() == me_email else "")
        val = r[sort_col]
        val_str = f"${val:,.0f}" if money else f"{int(val)}"
        rows_html += (
            f'<tr style="border-top:1px solid rgba(229,228,226,0.06);">'
            f'<td style="padding:10px 12px;color:var(--text-dim);">#{i+1}</td>'
            f'<td style="padding:10px 12px;color:var(--text);font-weight:700;">{r["full_name"]}{you}</td>'
            f'<td style="padding:10px 12px;color:var(--text-dim);">Store {r["store_id"]}</td>'
            f'<td style="padding:10px 12px;color:var(--text-dim);">{r["role"]}</td>'
            f'<td style="padding:10px 12px;text-align:right;color:var(--lime);font-weight:800;">{val_str}</td>'
            f'</tr>'
        )
    st.markdown(
        f'''
        <table style="width:100%;border-collapse:collapse;margin-top:6px;">
          <thead>
            <tr style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;text-align:left;font-weight:700;">
              <th style="padding:10px 12px;">RANK</th>
              <th style="padding:10px 12px;">NAME</th>
              <th style="padding:10px 12px;">STORE</th>
              <th style="padding:10px 12px;">ROLE</th>
              <th style="padding:10px 12px;text-align:right;">{value_label}</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        ''',
        unsafe_allow_html=True,
    )
