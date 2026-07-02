"""Banter Buddy starter creatures, care meters, and evolution rules."""
from __future__ import annotations

from datetime import datetime
import base64
import json
from pathlib import Path


PROFILES_PATH = Path("data/buddy_profiles.json")
ASSET_DIR = Path(__file__).parent.parent / "assets" / "buddies"

STARTERS = {
    "spark": {
        "name": "Spark Buddy",
        "role": "Sales Energy",
        "tagline": "Fast, bold, and built for conversion streaks.",
        "accent": "#D5E547",
        "secondary": "#4F6BFF",
        "trait": "Momentum",
        "image": "spark-starter.png",
    },
    "gem": {
        "name": "Gem Buddy",
        "role": "Style Expert",
        "tagline": "Calm, polished, and powered by product knowledge.",
        "accent": "#B76E79",
        "secondary": "#D5E547",
        "trait": "Taste",
        "image": "gem-starter.png",
    },
    "glow": {
        "name": "Glow Buddy",
        "role": "Team Leader",
        "tagline": "Warm, steady, and strongest when the team levels up.",
        "accent": "#FFB900",
        "secondary": "#D5E547",
        "trait": "Care",
        "image": "glow-starter.png",
    },
}

STAGES = [
    {"name": "Starter", "min_level": 1, "min_xp": 0},
    {"name": "Styled", "min_level": 3, "min_xp": 250},
    {"name": "Icon", "min_level": 7, "min_xp": 900},
    {"name": "Legend", "min_level": 15, "min_xp": 2400},
]

DEFAULT_PROFILE = {
    "starter": "",
    "nickname": "Banter Buddy",
    "care": 70,
    "spark": 60,
    "bond": 50,
    "last_action": "",
    "updated_at": "",
}


def _load_all() -> dict:
    if not PROFILES_PATH.exists():
        return {}
    try:
        return json.loads(PROFILES_PATH.read_text())
    except Exception:
        return {}


def _save_all(data: dict) -> None:
    PROFILES_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILES_PATH.write_text(json.dumps(data, indent=2))


def load_profile(email: str) -> dict:
    data = _load_all()
    profile = {**DEFAULT_PROFILE, **data.get(email.lower(), {})}
    return profile


def save_profile(email: str, updates: dict) -> None:
    data = _load_all()
    current = {**DEFAULT_PROFILE, **data.get(email.lower(), {})}
    current.update(updates)
    current["updated_at"] = datetime.now().isoformat(timespec="seconds")
    data[email.lower()] = current
    _save_all(data)


def choose_starter(email: str, starter: str) -> None:
    if starter not in STARTERS:
        return
    save_profile(
        email,
        {
            "starter": starter,
            "nickname": STARTERS[starter]["name"],
            "care": 75,
            "spark": 65,
            "bond": 55,
            "last_action": "Starter chosen",
        },
    )


def apply_care_action(email: str, action: str) -> None:
    profile = load_profile(email)
    changes = {
        "feed": {"care": 12, "spark": 2, "bond": 4, "last_action": "Fed"},
        "train": {"care": -3, "spark": 12, "bond": 5, "last_action": "Trained"},
        "cheer": {"care": 4, "spark": 4, "bond": 12, "last_action": "Cheered"},
    }.get(action)
    if not changes:
        return
    updates = {}
    for key in ("care", "spark", "bond"):
        updates[key] = max(0, min(100, int(profile.get(key, 0)) + changes.get(key, 0)))
    updates["last_action"] = changes["last_action"]
    save_profile(email, updates)


def stage_for(user: dict, profile: dict) -> tuple[int, dict]:
    level = int(user.get("level", 1) or 1)
    xp = int(user.get("xp", 0) or 0)
    unlocked = 0
    for i, stage in enumerate(STAGES):
        if level >= stage["min_level"] and xp >= stage["min_xp"]:
            unlocked = i
    return unlocked, STAGES[unlocked]


def next_stage(user: dict, profile: dict) -> dict | None:
    idx, _ = stage_for(user, profile)
    if idx + 1 >= len(STAGES):
        return None
    return STAGES[idx + 1]


def progress_to_next(user: dict, profile: dict) -> int:
    nxt = next_stage(user, profile)
    if not nxt:
        return 100
    level = int(user.get("level", 1) or 1)
    xp = int(user.get("xp", 0) or 0)
    level_progress = min(level / nxt["min_level"], 1.0)
    xp_progress = min(xp / max(nxt["min_xp"], 1), 1.0)
    return int(((level_progress + xp_progress) / 2) * 100)


def render_creature(starter: str, stage_index: int, size: int = 320) -> str:
    meta = STARTERS.get(starter, STARTERS["spark"])
    asset = ASSET_DIR / meta.get("image", "")
    if asset.exists():
        b64 = base64.b64encode(asset.read_bytes()).decode("ascii")
        scale = 1 + stage_index * 0.06
        return (
            '<div style="width:100%;height:100%;display:flex;align-items:center;'
            'justify-content:center;">'
            f'<img src="data:image/png;base64,{b64}" alt="{meta["name"]}" '
            f'style="width:{size}px;max-width:100%;height:auto;transform:scale({scale});'
            'object-fit:contain;filter:drop-shadow(0 18px 38px rgba(0,0,0,.45));" />'
            '</div>'
        )
    accent = meta["accent"]
    secondary = meta["secondary"]
    scale = 1 + stage_index * 0.08
    horn = "" if starter == "glow" else f'<path d="M74 68 L98 26 L112 76 Z" fill="{secondary}"/>'
    gem = f'<path d="M150 76 L174 104 L150 132 L126 104 Z" fill="{secondary}" opacity="0.95"/>'
    tail = {
        "spark": f'<path d="M236 170 L282 130 L260 176 L296 170 L238 226 Z" fill="{accent}"/>',
        "gem": f'<path d="M238 176 C280 146 300 182 264 214 C254 224 242 228 230 226" fill="none" stroke="{secondary}" stroke-width="18" stroke-linecap="round"/>',
        "glow": f'<circle cx="260" cy="178" r="34" fill="{accent}" opacity="0.32"/>',
    }[starter]
    crown = ""
    if stage_index >= 2:
        crown = f'<path d="M104 42 L126 18 L150 42 L176 18 L198 42 L190 66 L112 66 Z" fill="{accent}" opacity="0.9"/>'
    aura = 0.18 + stage_index * 0.08
    return "".join([
        '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;">',
        f'<svg viewBox="0 0 320 320" style="width:{size}px;max-width:100%;transform:scale({scale});filter:drop-shadow(0 18px 38px rgba(0,0,0,.45));" xmlns="http://www.w3.org/2000/svg">',
        f'<circle cx="160" cy="160" r="128" fill="{accent}" opacity="{aura}"/>',
        tail,
        crown,
        horn,
        '<ellipse cx="156" cy="178" rx="94" ry="88" fill="#F5F3EE"/>',
        '<ellipse cx="118" cy="168" rx="18" ry="24" fill="#0B0B0B"/>',
        '<ellipse cx="196" cy="168" rx="18" ry="24" fill="#0B0B0B"/>',
        '<circle cx="124" cy="158" r="5" fill="#FFFFFF"/>',
        '<circle cx="202" cy="158" r="5" fill="#FFFFFF"/>',
        '<path d="M138 210 C150 222 170 222 182 210" fill="none" stroke="#0B0B0B" stroke-width="8" stroke-linecap="round"/>',
        gem,
        f'<ellipse cx="92" cy="210" rx="18" ry="12" fill="{accent}" opacity="0.5"/>',
        f'<ellipse cx="220" cy="210" rx="18" ry="12" fill="{accent}" opacity="0.5"/>',
        '</svg></div>',
    ])
