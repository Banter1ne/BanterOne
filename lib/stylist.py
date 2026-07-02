"""Banter profile avatar system — stylized human portraits via DiceBear.

Every user gets a unique human-style avatar seeded by their email. Users can
pick a DiceBear style and tune colors without needing paid 3D generation.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlencode

PROFILES_PATH = "data/stylist_profiles.json"

# Persona palettes for the avatar frame/background.
PALETTES = {
    "Lime":      "D5E547",
    "Gold":      "FFB900",
    "Rose":      "B76E79",
    "Blue":      "0078D4",
    "Copper":    "C46A3A",
    "Graphite":  "6B7280",
}

AVATAR_STYLES = {
    "Personas": "personas",
    "Adventurer": "adventurer-neutral",
    "Lorelei": "lorelei",
    "Classic": "avataaars",
}

SKIN_TONES = {
    "Light": "F8D7B1",
    "Medium": "D08B5B",
    "Tan": "B56F45",
    "Deep": "6B3F2A",
}

HAIR_COLORS = {
    "Black": "0B0B0B",
    "Brown": "6B4530",
    "Blonde": "D6B370",
    "Auburn": "8A3D2B",
    "Gray": "9CA3AF",
    "Banter Lime": "D5E547",
}

# Backward-compatible alias for older imports.
TYPES = PALETTES
HAIR_STYLES = list(AVATAR_STYLES.keys())

DEFAULT_PROFILE = {
    "style":             "Personas",
    "palette":           "Lime",
    "primary_color":     "D5E547",
    "skin_tone":         "Medium",
    "skin_color":        "D08B5B",
    "hair_color_name":   "Brown",
    "hair_color":        "6B4530",
    "outfit_color":      "0B0B0B",
    "seed":              "banterone",
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
    all_profiles = _load_all()
    stored = all_profiles.get(email.lower(), {})
    merged = {**DEFAULT_PROFILE, **stored}
    # Auto-seed by email so each user has a unique avatar by default.
    if merged.get("seed") == "banterone":
        merged["seed"] = email.split("@")[0]
    if merged.get("type") and not stored.get("palette"):
        merged["palette"] = merged["type"] if merged["type"] in PALETTES else "Lime"
    if merged.get("palette") in PALETTES:
        merged["primary_color"] = merged.get("primary_color") or PALETTES[merged["palette"]]
    if merged.get("skin_tone") in SKIN_TONES:
        merged["skin_color"] = SKIN_TONES[merged["skin_tone"]]
    if str(merged.get("hair_color", "")).startswith("#"):
        merged["hair_color"] = merged["hair_color"].lstrip("#")
    return merged


def save_profile(email: str, updates: dict) -> None:
    all_profiles = _load_all()
    current = all_profiles.get(email.lower(), {})
    current.update(updates)
    all_profiles[email.lower()] = current
    _save_all(all_profiles)


# ── DiceBear human avatar URL ────────────────────────────────────────────────
def dicebear_url(profile: dict, seed_key: str = "banterone") -> str:
    style_label = profile.get("style", "Personas")
    style = AVATAR_STYLES.get(style_label, style_label)
    primary = profile.get("primary_color", PALETTES["Lime"]).lstrip("#")
    skin = profile.get("skin_color", SKIN_TONES["Medium"]).lstrip("#")
    hair = profile.get("hair_color", HAIR_COLORS["Brown"]).lstrip("#")
    outfit = profile.get("outfit_color", "0B0B0B").lstrip("#")
    seed = seed_key or profile.get("seed") or "banterone"
    params = {
        "seed": seed,
        "backgroundColor": primary,
        "radius": "50",
    }
    # Style-specific options are ignored harmlessly by styles that do not use
    # them, but give stronger customization in Classic/Avataaars.
    if style == "avataaars":
        params.update({
            "skinColor": skin,
            "hairColor": hair,
            "clothingColor": outfit,
        })
    return f"https://api.dicebear.com/9.x/{style}/svg?{urlencode(params)}"


def _fetch_svg(url: str) -> str | None:
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BanterONE/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
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
    """Return an inlined DiceBear human avatar SVG."""
    seed = seed_key or profile.get("seed") or "banterone"
    url = dicebear_url(profile, seed_key=seed)
    svg = _fetch_svg(url)
    if svg:
        svg_parts = svg.split("<svg", 1)
        if len(svg_parts) == 2:
            svg = "<svg" + svg_parts[1]
        else:
            svg = svg_parts[0]
        return (
            '<div style="width:100%;height:100%;display:flex;align-items:center;'
            'justify-content:center;padding:24px;">'
            + svg +
            '</div>'
        )
    return _fallback_svg(profile)


def _fallback_svg(profile: dict) -> str:
    primary = "#" + profile.get("primary_color", "D5E547").lstrip("#")
    return (
        '<div style="width:100%;height:100%;display:flex;align-items:center;'
        'justify-content:center;flex-direction:column;color:var(--text-dim);'
        'font-family:\'DM Sans\',sans-serif;">'
        f'<svg viewBox="0 0 24 24" style="width:140px;height:140px;color:{primary};" '
        'fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
        '<circle cx="12" cy="8" r="4"/>'
        '<path d="M4.5 22 C4.5 15.5 8 13 12 13 C16 13 19.5 15.5 19.5 22 L19.5 24 L4.5 24 Z"/>'
        '</svg>'
        '<div style="margin-top:14px;font-size:11px;letter-spacing:0.22em;font-weight:700;">'
        'AVATAR LOADING'
        '</div>'
        '</div>'
    )
