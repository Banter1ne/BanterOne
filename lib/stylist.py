"""Stylist character system — DiceBear personas portraits + profile persistence.

DiceBear (opensource, free, no signup) renders professional illustrated portraits
via URL params. Users customize hair style, hair color, skin, outfit, and eye
color — every change flows into a URL that returns a fresh SVG.
"""
from __future__ import annotations
import json, os
from pathlib import Path
from urllib.parse import urlencode

PROFILES_PATH = "data/stylist_profiles.json"

# Skin tone labels → hex value (used for both the picker and the DiceBear URL).
SKIN_TONES = {
    "Porcelain": "#F2D3B1",
    "Light":     "#EDB98A",
    "Medium":    "#D08B5B",
    "Tan":       "#AE5D29",
    "Deep":      "#694D3D",
}

# Hair style labels → real DiceBear personas hair variants (validated against schema).
HAIR_STYLES = ["Buzz", "Short", "Bob", "Long", "Bun", "Curly"]
_DICEBEAR_HAIR = {
    "Buzz":   "buzzcut",
    "Short":  "shortCombover",
    "Bob":    "bobCut",
    "Long":   "long",
    "Bun":    "curlyBun",
    "Curly":  "curly",
}

DEFAULT_PROFILE = {
    "skin_tone":    "Medium",
    "hair_color":   "#D5E547",
    "hair_style":   "Short",
    "outfit_color": "#111111",
    "eye_color":    "#3A2A1A",
    "equipped_piercings": [],
}


# ── Profile persistence ──────────────────────────────────────────────────────
def _load_all() -> dict:
    p = Path(PROFILES_PATH)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def _save_all(data: dict) -> None:
    Path(PROFILES_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(PROFILES_PATH).write_text(json.dumps(data, indent=2))


def load_profile(email: str) -> dict:
    """Return this user's stylist profile merged over defaults."""
    all_profiles = _load_all()
    return {**DEFAULT_PROFILE, **all_profiles.get(email.lower(), {})}


def save_profile(email: str, updates: dict) -> None:
    """Merge updates into the user's profile and persist."""
    all_profiles = _load_all()
    current = all_profiles.get(email.lower(), {})
    current.update(updates)
    all_profiles[email.lower()] = current
    _save_all(all_profiles)


# ── DiceBear portrait URL ────────────────────────────────────────────────────
def dicebear_url(profile: dict, seed_key: str = "banterone") -> str:
    """Build the DiceBear personas URL from the user's profile choices."""
    skin_hex = SKIN_TONES.get(profile.get("skin_tone", "Medium"), "#D08B5B").lstrip("#")
    hair_hex = profile.get("hair_color", "#D5E547").lstrip("#")
    outfit_hex = profile.get("outfit_color", "#111111").lstrip("#")
    hair = _DICEBEAR_HAIR.get(profile.get("hair_style", "Short"), "shortRound")
    params = {
        "seed": seed_key,
        "backgroundColor": "0b0b0b",
        "hair": hair,
        "hairColor": hair_hex,
        "skinColor": skin_hex,
        "clothingColor": outfit_hex,
    }
    return f"https://api.dicebear.com/9.x/personas/svg?{urlencode(params)}"


def _fetch_svg(url: str) -> str | None:
    """Server-side HTTP fetch — bypasses browser cross-origin ORB blocking."""
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BanterONE/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            # Sanity: only trust SVG payloads
            if "<svg" in body:
                return body
    except Exception:
        return None
    return None


try:
    import streamlit as _st
    _fetch_svg = _st.cache_data(ttl=3600, show_spinner=False)(_fetch_svg)
except Exception:
    pass


def render_svg(profile: dict, gender: str = "male", size: int = 420,
               seed_key: str | None = None) -> str:
    """Return a fully-inlined DiceBear portrait — professional illustrated look.
    We fetch server-side to avoid Chrome's ERR_BLOCKED_BY_ORB when the SVG is
    loaded cross-origin via <img>."""
    seed = seed_key or profile.get("seed") or "banterone"
    url = dicebear_url(profile, seed_key=seed)
    svg = _fetch_svg(url)
    if svg:
        # Strip XML prolog if present so the inline SVG plays nice with our HTML.
        svg = svg.split("<svg", 1)
        if len(svg) == 2:
            svg = "<svg" + svg[1]
        else:
            svg = svg[0]
        return (
            '<div style="width:100%;height:100%;display:flex;align-items:center;'
            'justify-content:center;padding:24px;">'
            + svg +
            '</div>'
        )
    # Fallback if DiceBear is unreachable — a clean lime-outline silhouette.
    return _fallback_svg(profile)


def _fallback_svg(profile: dict) -> str:
    hair = profile.get("hair_color", "#D5E547")
    return (
        '<div style="width:100%;height:100%;display:flex;align-items:center;'
        'justify-content:center;flex-direction:column;color:var(--text-dim);'
        'font-family:\'DM Sans\',sans-serif;">'
        f'<svg viewBox="0 0 24 24" style="width:120px;height:120px;color:{hair};" '
        'fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
        '<circle cx="12" cy="8" r="4"/>'
        '<path d="M4 22 C4 15, 8 13, 12 13 C16 13, 20 15, 20 22 L20 24 L4 24 Z"/>'
        '</svg>'
        '<div style="margin-top:14px;font-size:11px;letter-spacing:0.22em;font-weight:700;">'
        'PORTRAIT LOADING'
        '</div>'
        '</div>'
    )


# ── (Legacy hand-crafted SVG kept for reference in case DiceBear is offline) ─
def _legacy_render_svg(profile: dict, gender: str = "male", size: int = 420) -> str:
    skin = SKIN_TONES.get(profile.get("skin_tone", "Medium"), "#D08B5B")
    hair_color = profile.get("hair_color", "#D5E547")
    hair_style = profile.get("hair_style", "Short")
    outfit = profile.get("outfit_color", "#111111")
    eye_color = profile.get("eye_color", "#3A2A1A")
    piercings = profile.get("equipped_piercings", []) or []

    # Viewbox 0 0 400 500. Head centered around (200, 150).
    cx, cy = 200, 150
    rx, ry = 66, 78

    # ── Body / outfit ────────────────────────────────────────────────────────
    body = (
        f'<path d="M{cx-72},{cy+64} '
        f'Q{cx-72},{cy+70} {cx-90},{cy+120} '
        f'L{cx-110},{cy+340} L{cx+110},{cy+340} '
        f'L{cx+90},{cy+120} Q{cx+72},{cy+70} {cx+72},{cy+64} '
        f'L{cx+30},{cy+64} Q{cx+30},{cy+80} {cx},{cy+80} Q{cx-30},{cy+80} {cx-30},{cy+64} Z" '
        f'fill="{outfit}"/>'
    )
    # Neck
    neck = (
        f'<path d="M{cx-22},{cy+60} L{cx+22},{cy+60} L{cx+22},{cy+80} L{cx-22},{cy+80} Z" '
        f'fill="{skin}" opacity="0.9"/>'
    )

    # ── Hair back (behind head) ──────────────────────────────────────────────
    hair_back = ""
    if hair_style == "Long":
        hair_back = (
            f'<path d="M{cx-rx-10},{cy-10} '
            f'L{cx-rx-16},{cy+340} L{cx-rx+8},{cy+340} '
            f'L{cx-rx+4},{cy-30} Q{cx},{cy-ry-8} {cx+rx-4},{cy-30} '
            f'L{cx+rx-8},{cy+340} L{cx+rx+16},{cy+340} L{cx+rx+10},{cy-10} Z" '
            f'fill="{hair_color}"/>'
        )
    elif hair_style == "Medium":
        hair_back = (
            f'<path d="M{cx-rx-6},{cy-10} '
            f'L{cx-rx-6},{cy+110} L{cx-rx+14},{cy+114} '
            f'L{cx-rx+4},{cy-30} Q{cx},{cy-ry-8} {cx+rx-4},{cy-30} '
            f'L{cx+rx-14},{cy+114} L{cx+rx+6},{cy+110} L{cx+rx+6},{cy-10} Z" '
            f'fill="{hair_color}"/>'
        )
    elif hair_style == "Braids":
        hair_back = (
            f'<rect x="{cx-rx-10}" y="{cy-10}" width="18" height="230" rx="9" fill="{hair_color}"/>'
            f'<rect x="{cx+rx-8}" y="{cy-10}" width="18" height="230" rx="9" fill="{hair_color}"/>'
        )

    # ── Head ─────────────────────────────────────────────────────────────────
    head = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{skin}"/>'

    # ── Facial features ──────────────────────────────────────────────────────
    eyes = (
        f'<ellipse cx="{cx-22}" cy="{cy-4}" rx="4.5" ry="6" fill="{eye_color}"/>'
        f'<ellipse cx="{cx+22}" cy="{cy-4}" rx="4.5" ry="6" fill="{eye_color}"/>'
        f'<circle cx="{cx-21}" cy="{cy-6}" r="1.4" fill="#fff"/>'
        f'<circle cx="{cx+23}" cy="{cy-6}" r="1.4" fill="#fff"/>'
    )
    brows = (
        f'<path d="M{cx-33},{cy-22} Q{cx-22},{cy-27} {cx-11},{cy-22}" stroke="{_darken(hair_color)}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        f'<path d="M{cx+11},{cy-22} Q{cx+22},{cy-27} {cx+33},{cy-22}" stroke="{_darken(hair_color)}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    )
    nose = f'<path d="M{cx},{cy+2} Q{cx-4},{cy+18} {cx+2},{cy+22}" stroke="{_darken(skin)}" stroke-width="2" fill="none" stroke-linecap="round"/>'
    lips = (
        f'<path d="M{cx-14},{cy+36} Q{cx},{cy+44} {cx+14},{cy+36} Q{cx},{cy+40} {cx-14},{cy+36} Z" '
        f'fill="{_lip_color(skin)}"/>'
    )

    # ── Hair front (over head) ───────────────────────────────────────────────
    hair_front = ""
    if hair_style == "Buzz":
        hair_front = (
            f'<path d="M{cx-rx+2},{cy-30} Q{cx},{cy-ry-2} {cx+rx-2},{cy-30} '
            f'L{cx+rx-2},{cy-46} Q{cx},{cy-ry-6} {cx-rx+2},{cy-46} Z" '
            f'fill="{hair_color}" opacity="0.85"/>'
        )
    elif hair_style == "Short":
        hair_front = (
            f'<path d="M{cx-rx-2},{cy-20} '
            f'Q{cx-rx-4},{cy-ry+20} {cx-30},{cy-ry-10} '
            f'Q{cx},{cy-ry-14} {cx+30},{cy-ry-10} '
            f'Q{cx+rx+4},{cy-ry+20} {cx+rx+2},{cy-20} '
            f'L{cx+rx-4},{cy-40} Q{cx},{cy-ry+4} {cx-rx+4},{cy-40} Z" '
            f'fill="{hair_color}"/>'
        )
    elif hair_style == "Curly":
        # Bumpy curly hairline via multiple circles
        curls = ""
        for i, (dx, dy, r) in enumerate([
            (-rx+4, -ry+30, 22), (-rx+30, -ry+8, 20), (-rx+56, -ry-2, 22),
            (cx-cx-4, -ry-6, 24), (rx-56, -ry-2, 22), (rx-30, -ry+8, 20),
            (rx-4, -ry+30, 22),
        ]):
            curls += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{hair_color}"/>'
        hair_front = curls
    elif hair_style == "Medium":
        hair_front = (
            f'<path d="M{cx-rx-4},{cy-20} '
            f'Q{cx-rx-6},{cy-ry+10} {cx-24},{cy-ry-12} '
            f'Q{cx},{cy-ry-16} {cx+24},{cy-ry-12} '
            f'Q{cx+rx+6},{cy-ry+10} {cx+rx+4},{cy-20} '
            f'L{cx+rx-6},{cy-38} Q{cx},{cy-ry+2} {cx-rx+6},{cy-38} Z" '
            f'fill="{hair_color}"/>'
        )
    elif hair_style == "Long":
        hair_front = (
            f'<path d="M{cx-rx-2},{cy-16} '
            f'Q{cx-rx-4},{cy-ry+16} {cx-26},{cy-ry-10} '
            f'Q{cx},{cy-ry-14} {cx+26},{cy-ry-10} '
            f'Q{cx+rx+4},{cy-ry+16} {cx+rx+2},{cy-16} '
            f'L{cx+rx-8},{cy-38} Q{cx},{cy-ry+2} {cx-rx+8},{cy-38} Z" '
            f'fill="{hair_color}"/>'
        )
    elif hair_style == "Braids":
        hair_front = (
            f'<path d="M{cx-rx-2},{cy-20} '
            f'Q{cx-rx-4},{cy-ry+8} {cx-24},{cy-ry-8} '
            f'Q{cx},{cy-ry-12} {cx+24},{cy-ry-8} '
            f'Q{cx+rx+4},{cy-ry+8} {cx+rx+2},{cy-20} '
            f'L{cx+rx-6},{cy-36} Q{cx},{cy-ry+4} {cx-rx+6},{cy-36} Z" '
            f'fill="{hair_color}"/>'
        )

    # ── Piercings ────────────────────────────────────────────────────────────
    pierce_svg = ""
    for pid in piercings:
        pierce_svg += _piercing_svg(pid, cx, cy, rx, ry)

    return (
        f'<svg viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;height:100%;">'
        f'{hair_back}{body}{neck}{head}{brows}{eyes}{nose}{lips}{hair_front}{pierce_svg}'
        f'</svg>'
    )


# ── Piercing positions (relative to head center) ─────────────────────────────
def _piercing_svg(pid: str, cx: int, cy: int, rx: int, ry: int) -> str:
    silver = "#E5E4E2"
    lime = "#D5E547"
    positions = {
        "nose_stud":      (cx - 8, cy + 18, 3, silver),
        "septum_ring":    (cx, cy + 26, 4, silver, "ring"),
        "helix_hoop":     (cx - rx + 4, cy - 34, 5, lime, "ring"),
        "cartilage_stud": (cx + rx - 6, cy - 24, 3, silver),
        "tragus_diamond": (cx - rx + 8, cy - 8, 3, lime),
        "eyebrow_bar":    (cx + 22, cy - 30, 3, silver, "bar"),
        "lip_ring":       (cx - 16, cy + 44, 3, silver, "ring"),
        "industrial_bar": (cx - rx + 4, cy - 40, 3, silver, "long-bar"),
        "belly_ring":     (cx, cy + 200, 4, silver, "ring"),
        "conch_diamond":  (cx + rx - 8, cy - 6, 3, lime),
    }
    if pid not in positions:
        return ""
    pos = positions[pid]
    x, y, r, color = pos[0], pos[1], pos[2], pos[3]
    kind = pos[4] if len(pos) > 4 else "stud"
    if kind == "ring":
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-width="1.5"/>'
    if kind == "bar":
        return f'<rect x="{x-4}" y="{y-1}" width="10" height="2" rx="1" fill="{color}"/>'
    if kind == "long-bar":
        return f'<rect x="{x-2}" y="{y}" width="4" height="18" fill="{color}"/>'
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def _darken(hex_color: str, amount: float = 0.4) -> str:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return "#000"
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r, g, b = int(r * (1 - amount)), int(g * (1 - amount)), int(b * (1 - amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def _lip_color(skin_hex: str) -> str:
    """Warmer lip tone based on skin."""
    hex_color = skin_hex.lstrip("#")
    if len(hex_color) != 6:
        return "#B87070"
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(255, int(r * 0.9) + 20)
    g = int(g * 0.55)
    b = int(b * 0.55)
    return f"#{r:02x}{g:02x}{b:02x}"
