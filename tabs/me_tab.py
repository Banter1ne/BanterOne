import os
import re
import streamlit as st

from lib import buddy, db, rpg


def render() -> None:
    user = st.session_state.user

    st.markdown("### My Banter Buddy")
    st.caption(
        f"Level {int(user.get('level', 1))} · {int(user.get('xp', 0)):,} XP · "
        f"Store {user.get('store_id', '—')}"
    )

    buddy_profile = buddy.load_profile(user["email"])
    if not buddy_profile.get("starter"):
        _render_buddy_starter_picker(user)
        return

    _render_buddy(user, buddy_profile)

    st.markdown("---")
    _render_stats(user)
    st.markdown("---")
    _render_pfp_upload()
    _render_league()


# ── First-time starter picker ────────────────────────────────────────────────
def _render_buddy_starter_picker(user: dict) -> None:
    st.markdown(
        '<div class="glass-card" style="margin-bottom:18px;">'
        '<h4 style="margin-top:0;">Choose your starter</h4>'
        '<p style="color:var(--text-dim);margin-bottom:0;">'
        "Your Banter Buddy grows with your daily rhythm: sales momentum, "
        "product knowledge, team energy, and consistency."
        "</p></div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for col, starter_id in zip(cols, buddy.STARTERS):
        meta = buddy.STARTERS[starter_id]
        with col:
            creature = buddy.render_creature(starter_id, 0, size=220)
            st.markdown(
                (
                    f'<div class="glass-card" style="min-height:390px;text-align:center;">'
                    f'<div style="height:210px;border-radius:18px;overflow:hidden;'
                    f'background:radial-gradient(circle at 50% 35%, {meta["accent"]}44 0%, #000 64%);">'
                    f'{creature}</div>'
                    f'<div style="font-family:\'Instrument Serif\',serif;font-style:italic;'
                    f'font-size:28px;color:var(--text);margin-top:14px;">{meta["name"]}</div>'
                    f'<div style="color:var(--lime);font-size:10px;letter-spacing:0.2em;'
                    f'text-transform:uppercase;font-weight:800;margin:6px 0;">{meta["role"]}</div>'
                    f'<div style="color:var(--text-dim);font-size:13px;line-height:1.45;">'
                    f'{meta["tagline"]}</div></div>'
                ),
                unsafe_allow_html=True,
            )
            if st.button(f"Choose {meta['name']}", use_container_width=True, key=f"choose_buddy_{starter_id}"):
                buddy.choose_starter(user["email"], starter_id)
                rpg.save_gender(user["email"], "buddy")
                user["gender"] = "buddy"
                st.rerun()


# ── Banter Buddy dashboard ───────────────────────────────────────────────────
def _render_buddy(user: dict, profile: dict) -> None:
    starter = profile.get("starter") or "spark"
    meta = buddy.STARTERS.get(starter, buddy.STARTERS["spark"])
    stage_index, stage = buddy.stage_for(user, profile)
    next_stage = buddy.next_stage(user, profile)
    progress = buddy.progress_to_next(user, profile)
    col_preview, col_controls = st.columns([5, 4])

    with col_preview:
        creature = buddy.render_creature(starter, stage_index, size=420)
        st.markdown(
            f'<div class="glass-card" style="padding:16px;">'
            f'<div style="border-radius:20px;overflow:hidden;'
            f'background:radial-gradient(ellipse at 50% 20%,{meta["accent"]}44 0%,#000 65%);'
            f'aspect-ratio:4/5;">{creature}</div>'
            f'<div style="text-align:center;margin-top:14px;font-size:10px;'
            f'letter-spacing:0.32em;color:var(--lime);font-weight:700;">YOUR BANTER BUDDY</div>'
            f'<div style="text-align:center;font-family:\'Instrument Serif\',serif;'
            f'font-style:italic;font-size:22px;color:var(--text);text-transform:capitalize;">'
            f'{profile.get("nickname") or meta["name"]}</div>'
            f'<div style="text-align:center;color:var(--text-dim);font-size:12px;margin-top:4px;">'
            f'{stage["name"]} · {meta["role"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_controls:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Care")
        _meter("Care", int(profile.get("care", 70)), meta["accent"])
        _meter("Spark", int(profile.get("spark", 60)), meta["secondary"])
        _meter("Bond", int(profile.get("bond", 50)), "#D5E547")
        st.markdown(
            f'<div style="color:var(--text-dim);font-size:12px;margin:12px 0;">'
            f'Last action: <b style="color:var(--text);">{profile.get("last_action") or "None yet"}</b></div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        actions = [(c1, "feed", "Feed"), (c2, "train", "Train"), (c3, "cheer", "Cheer")]
        for col, action, label in actions:
            with col:
                if st.button(label, use_container_width=True, key=f"buddy_{action}"):
                    buddy.apply_care_action(user["email"], action)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card" style="margin-top:14px;">', unsafe_allow_html=True)
        st.markdown("#### Evolution")
        if next_stage:
            st.markdown(
                f'<div style="color:var(--text-dim);font-size:12px;">Next form</div>'
                f'<div style="font-family:\'Instrument Serif\',serif;font-style:italic;'
                f'font-size:30px;color:var(--lime);">{next_stage["name"]}</div>'
                f'<div style="background:rgba(255,255,255,0.06);border-radius:99px;height:9px;'
                f'margin:10px 0;overflow:hidden;">'
                f'<div style="background:linear-gradient(90deg,var(--lime),var(--lime-2));'
                f'height:100%;width:{progress}%;"></div></div>'
                f'<div style="color:var(--text-dim);font-size:12px;">'
                f'Needs Level {next_stage["min_level"]} and {next_stage["min_xp"]:,} XP</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="font-family:\'Instrument Serif\',serif;font-style:italic;'
                'font-size:30px;color:var(--lime);">Legend form reached</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


def _meter(label: str, value: int, color: str) -> None:
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;font-size:12px;'
        f'color:var(--text-dim);margin-top:10px;"><span>{label}</span><span>{value}%</span></div>'
        f'<div style="background:rgba(255,255,255,0.06);border-radius:99px;height:8px;overflow:hidden;">'
        f'<div style="height:100%;width:{value}%;background:{color};"></div></div>',
        unsafe_allow_html=True,
    )


# ── Stats column ─────────────────────────────────────────────────────────────
def _render_stats(user: dict) -> None:
    ranked = rpg.league_ranking()
    idx = ranked.index[ranked["email"].str.lower() == user["email"].lower()].tolist()
    rank = idx[0] + 1 if idx else "—"
    total = len(ranked)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="glass-card">
              <div style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;font-weight:700;">LEVEL</div>
              <div style="font-family:'Instrument Serif',serif;font-style:italic;
                          font-size:52px;font-weight:400;color:var(--lime);line-height:1;">
                {int(user.get("level", 1))}
              </div>
              <div style="color:var(--text-dim);font-size:12px;margin-top:6px;">
                {int(user.get("xp", 0)):,} XP · Rank #{rank} of {total}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    cc = rpg.commission_countdown(user, "July")
    with c2:
        if cc.get("at_top"):
            body = (
                f'<div style="color:var(--text-dim);font-size:12px;">Max tier reached</div>'
                f'<div style="font-family:\'Instrument Serif\',serif;font-style:italic;'
                f'font-size:24px;color:var(--lime);">3.75%</div>'
                f'<div style="color:var(--text-dim);font-size:12px;margin-top:6px;">'
                f'Projected: <b style="color:var(--text);">${cc["current_commission"]:,.0f}</b></div>'
            )
        else:
            pct = min(cc["pct_to_next"], 100)
            body = (
                f'<div style="color:var(--text-dim);font-size:11px;letter-spacing:0.14em;">JULY MTD MERCH</div>'
                f'<div style="font-family:\'Instrument Serif\',serif;font-style:italic;'
                f'font-size:32px;font-weight:400;color:var(--text);">${cc["merch_sales"]:,.0f}</div>'
                f'<div style="background:rgba(255,255,255,0.06);border-radius:99px;height:8px;margin:10px 0;overflow:hidden;">'
                f'<div style="background:linear-gradient(90deg,var(--lime),var(--lime-2));height:100%;width:{pct:.1f}%;"></div>'
                f'</div>'
                f'<div style="color:var(--text-dim);font-size:12px;">'
                f'<b style="color:var(--text);">${cc["gap"]:,.0f}</b> to L{cc["next_level"]}</div>'
            )
        st.markdown(
            f"""
            <div class="glass-card">
              <div style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;font-weight:700;margin-bottom:8px;">
                COMMISSION
              </div>
              {body}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        buddy_profile = buddy.load_profile(user["email"])
        starter = buddy_profile.get("starter") or "spark"
        meta = buddy.STARTERS.get(starter, buddy.STARTERS["spark"])
        path = (
            f'<div style="font-family:\'Instrument Serif\',serif;font-style:italic;'
            f'font-size:28px;color:var(--lime);line-height:1;">{meta["trait"]}</div>'
            f'<div style="color:var(--text-dim);font-size:12px;margin-top:8px;">'
            f'{meta["tagline"]}</div>'
        )
        st.markdown(
            f"""
            <div class="glass-card">
              <div style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;font-weight:700;margin-bottom:8px;">
                BUDDY PATH
              </div>
              {path}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Profile picture upload + representation mode ─────────────────────────────
def _render_pfp_upload() -> None:
    with st.expander("Profile Representation", expanded=False):
        user = st.session_state.user
        st.caption("Choose how you show up everywhere — store badge, feed, league board.")

        current_mode = (user.get("avatar_mode") or "").strip().lower() or "character"
        idx = ["character", "photo", "initials"].index(current_mode) \
              if current_mode in ("character", "photo", "initials") else 0
        mode = st.radio(
            "Show up as",
            options=["Banter Buddy", "Photo", "Initials"],
            horizontal=True,
            index=idx,
            key="avatar_mode_radio",
        )

        st.markdown("---")
        st.caption("Upload a photo (used when Photo mode is selected).")
        uploaded = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg"],
            key="pfp_uploader",
            label_visibility="collapsed",
        )

        chosen_mode = "character" if mode == "Banter Buddy" else mode.lower()
        needs_save = chosen_mode != current_mode

        if uploaded is not None:
            email = user["email"]
            safe = re.sub(r"[^a-z0-9]+", "_", email.lower())
            ext = ".png" if uploaded.type == "image/png" else ".jpg"
            path = f"assets/avatars/{safe}{ext}"
            os.makedirs("assets/avatars", exist_ok=True)
            with open(path, "wb") as f:
                f.write(uploaded.getvalue())
            users = db.read("users").copy()
            mask = users["email"].str.lower() == email.lower()
            users.loc[mask, "avatar_url"] = path
            users.loc[mask, "avatar_mode"] = "photo"
            db.write("users", users)
            user["avatar_url"] = path
            user["avatar_mode"] = "photo"
            st.success("Photo saved — showing you as Photo now.")
            st.image(path, width=140)
            return

        if needs_save:
            users = db.read("users").copy()
            mask = users["email"].str.lower() == user["email"].lower()
            users.loc[mask, "avatar_mode"] = chosen_mode
            db.write("users", users)
            user["avatar_mode"] = chosen_mode
            st.success(f"Now showing as **{mode}**.")


# ── Bantagachi League drawer ────────────────────────────────────────────────────
def _render_league() -> None:
    with st.expander("The League — District Rankings", expanded=False):
        ranked = rpg.league_ranking()
        me = st.session_state.user["email"].lower()
        rows = ""
        for i, row in ranked.iterrows():
            rank_cell = f"#{i+1}"
            you_tag = ('  <span style="color:var(--lime);font-weight:800;">'
                       '· YOU</span>') if row["email"].lower() == me else ""
            rows += (
                f'<tr style="border-top:1px solid rgba(229,228,226,0.06);">'
                f'<td style="padding:10px 12px;color:var(--text-dim);">{rank_cell}</td>'
                f'<td style="padding:10px 12px;color:var(--text);font-weight:600;">'
                f'{row["full_name"]}{you_tag}</td>'
                f'<td style="padding:10px 12px;color:var(--text-dim);">Store {row["store_id"]}</td>'
                f'<td style="padding:10px 12px;color:var(--text-dim);">{row["role"]}</td>'
                f'<td style="padding:10px 12px;text-align:right;color:var(--lime);'
                f'font-weight:800;">L{int(row["level"])}</td>'
                f'</tr>'
            )
        st.markdown(
            f'''
            <table style="width:100%;border-collapse:collapse;margin-top:8px;">
              <thead>
                <tr style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;text-align:left;font-weight:700;">
                  <th style="padding:10px 12px;">RANK</th>
                  <th style="padding:10px 12px;">NAME</th>
                  <th style="padding:10px 12px;">STORE</th>
                  <th style="padding:10px 12px;">ROLE</th>
                  <th style="padding:10px 12px;text-align:right;">LVL</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
            ''',
            unsafe_allow_html=True,
        )
