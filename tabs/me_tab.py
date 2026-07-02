import os
import random
import re
import streamlit as st
import streamlit.components.v1 as components

from lib import db, rpg, stylist


def render() -> None:
    user = st.session_state.user

    st.markdown("### Stylist")
    st.caption(
        f"Level {int(user.get('level', 1))} · {int(user.get('xp', 0)):,} XP · "
        f"Store {user.get('store_id', '—')}"
    )

    gender = (
        st.session_state.get("stylist_gender")
        or (user.get("gender") if isinstance(user.get("gender"), str) and user.get("gender") else "")
    )
    if not gender:
        _render_gender_picker()
        return

    _render_customizer(user, gender)

    st.markdown("---")
    _render_stats(user)
    st.markdown("---")
    _render_pfp_upload()
    _render_scanner()
    _render_league()


# ── Gender picker ────────────────────────────────────────────────────────────
def _render_gender_picker() -> None:
    st.markdown(
        '<div class="glass-card" style="margin-bottom:18px;">'
        '<h4 style="margin-top:0;">Create your Stylist</h4>'
        '<p style="color:var(--text-dim);margin-bottom:0;">'
        "Pick your character identity, then customize skin, hair, and outfit."
        "</p></div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    picks = [
        (c1, "MALE",        "pick_m",  "male"),
        (c2, "FEMALE",      "pick_f",  "female"),
        (c3, "NON-BINARY",  "pick_nb", "nonbinary"),
    ]
    for col, label, key, gender_val in picks:
        with col:
            if st.button(label, use_container_width=True, key=key):
                st.session_state.stylist_gender = gender_val
                rpg.save_gender(st.session_state.user["email"], gender_val)
                st.session_state.user["gender"] = gender_val
                st.rerun()


# ── Character customizer (custom SVG, no external service) ───────────────────
def _render_customizer(user: dict, gender: str) -> None:
    profile = stylist.load_profile(user["email"])
    unlocked = rpg.parse_unlocked(user)
    unlocked_piercings = [
        iid for iid in unlocked
        if rpg.format_item(iid) and rpg.format_item(iid)["cat"] == "piercing"
    ]

    col_preview, col_controls = st.columns([5, 4])

    with col_controls:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Customize")

        skin_names = list(stylist.SKIN_TONES.keys())
        skin_idx = skin_names.index(profile["skin_tone"]) if profile["skin_tone"] in skin_names else 2
        skin = st.selectbox("Skin Tone", options=skin_names, index=skin_idx,
                            key="stylist_skin")

        hair_color = st.color_picker("Hair Color", value=profile["hair_color"],
                                     key="stylist_hair_color")

        hair_idx = stylist.HAIR_STYLES.index(profile["hair_style"]) \
                   if profile["hair_style"] in stylist.HAIR_STYLES else 1
        hair_style = st.selectbox("Hair Style", options=stylist.HAIR_STYLES,
                                  index=hair_idx, key="stylist_hair_style")

        eye_color = st.color_picker("Eye Color", value=profile["eye_color"],
                                    key="stylist_eye")

        outfit_color = st.color_picker("Outfit Color", value=profile["outfit_color"],
                                       key="stylist_outfit")

        equipped = st.multiselect(
            "Equipped Piercings (from Wardrobe)",
            options=unlocked_piercings,
            default=profile.get("equipped_piercings", []),
            format_func=lambda iid: rpg.format_item(iid)["name"] if rpg.format_item(iid) else iid,
            key="stylist_equipped",
        )

        new_profile = {
            "skin_tone":         skin,
            "hair_color":        hair_color,
            "hair_style":        hair_style,
            "eye_color":         eye_color,
            "outfit_color":      outfit_color,
            "equipped_piercings": equipped,
        }
        changed = any(new_profile[k] != profile.get(k) for k in new_profile)
        if changed:
            if st.button("Save Stylist", type="primary", use_container_width=True,
                         key="stylist_save"):
                stylist.save_profile(user["email"], new_profile)
                st.success("Stylist saved.")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        preview = {
            "skin_tone":         st.session_state.get("stylist_skin", profile["skin_tone"]),
            "hair_color":        st.session_state.get("stylist_hair_color", profile["hair_color"]),
            "hair_style":        st.session_state.get("stylist_hair_style", profile["hair_style"]),
            "eye_color":         st.session_state.get("stylist_eye", profile["eye_color"]),
            "outfit_color":      st.session_state.get("stylist_outfit", profile["outfit_color"]),
            "equipped_piercings": st.session_state.get("stylist_equipped",
                                                        profile.get("equipped_piercings", [])),
        }
        svg = stylist.render_svg(preview, gender=gender, size=460)
        st.markdown(
            f'<div class="glass-card" style="padding:16px;">'
            f'<div style="border-radius:20px;overflow:hidden;'
            f'background:radial-gradient(ellipse at 50% 20%,rgba(213,229,71,0.22) 0%,#000 65%);'
            f'aspect-ratio:4/5;">{svg}</div>'
            f'<div style="text-align:center;margin-top:14px;font-size:10px;'
            f'letter-spacing:0.32em;color:var(--lime);font-weight:700;">YOUR STYLIST</div>'
            f'<div style="text-align:center;font-family:\'Instrument Serif\',serif;'
            f'font-style:italic;font-size:22px;color:var(--text);text-transform:capitalize;">'
            f'{gender}</div>'
            f'</div>',
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
        unlocked = rpg.parse_unlocked(user)
        if not unlocked:
            wardrobe = ('<div style="color:var(--text-dim);font-size:12px;">'
                        "No pieces yet. Scan below.</div>")
        else:
            chips = ""
            for iid in unlocked:
                item = rpg.format_item(iid)
                if not item:
                    continue
                color = rpg.RARITY_COLORS.get(item["rarity"], "#94A3B8")
                chips += (
                    f'<div style="display:inline-block;padding:5px 10px;border-radius:99px;'
                    f'background:rgba(255,255,255,0.04);border:1px solid {color}55;color:{color};'
                    f'font-size:11px;margin:2px 4px 2px 0;font-weight:600;">'
                    f'{item["name"]}</div>'
                )
            wardrobe = chips
        st.markdown(
            f"""
            <div class="glass-card">
              <div style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;font-weight:700;margin-bottom:8px;">
                WARDROBE
              </div>
              {wardrobe}
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
            options=["Character", "Photo", "Initials"],
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

        chosen_mode = mode.lower()
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


# ── Camera scanner ───────────────────────────────────────────────────────────
def _render_scanner() -> None:
    st.markdown("#### Scan Banter Jewelry")
    st.caption("Point at a real piece of Banter jewelry in-store. AI identifies the SKU "
               "and unlocks it to your Wardrobe.")
    photo = st.camera_input("Take a photo of the piece", key="rpg_scanner",
                            label_visibility="collapsed")
    if photo is not None:
        owned = set(rpg.parse_unlocked(st.session_state.user))
        pool = [i for i in rpg.SCANNABLE_POOL if i not in owned] or rpg.SCANNABLE_POOL
        picked = random.choice(pool)
        added = rpg.unlock_item(st.session_state.user["email"], picked)
        item = rpg.format_item(picked)
        if added:
            current = rpg.parse_unlocked(st.session_state.user)
            current.append(picked)
            st.session_state.user["unlocked_items"] = ",".join(current)
            st.success(f"AI matched: **{item['name']}** — added to Wardrobe.")
            st.balloons()
        else:
            st.info(f"{item['name']} — you already have this piece.")


# ── Stylist League drawer ────────────────────────────────────────────────────
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
