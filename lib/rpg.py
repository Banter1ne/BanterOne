"""Bantagachi RPG mechanics — jewelry catalog, wardrobe, XP, and league ranking."""
from __future__ import annotations
import pandas as pd
from . import db, standards


JEWELRY_CATALOG = {
    # St. Jude tier jewels — assigned by donation amount
    "sj_diamond":   {"name": "St. Jude Diamond Champion Pin", "cat": "pin",     "emoji": "💎🎗️", "rarity": "legendary"},
    "sj_gold":      {"name": "St. Jude Gold Pin",             "cat": "pin",     "emoji": "🏅🎗️", "rarity": "epic"},
    "sj_silver":    {"name": "St. Jude Silver Pin",           "cat": "pin",     "emoji": "🥈🎗️", "rarity": "rare"},
    "sj_red":       {"name": "St. Jude Red Ribbon",           "cat": "pin",     "emoji": "🎗️",   "rarity": "uncommon"},
    "sj_supporter": {"name": "St. Jude Supporter Charm",      "cat": "charm",   "emoji": "🌟",   "rarity": "common"},
    # Banter jewelry — unlocked by scanning real product in-store
    "diamond_stud":  {"name": "Diamond Stud Earring", "cat": "earring",  "emoji": "💎", "rarity": "epic"},
    "rose_chain":    {"name": "Rose Gold Chain",      "cat": "necklace", "emoji": "📿", "rarity": "rare"},
    "signet_ring":   {"name": "Signet Ring",          "cat": "ring",     "emoji": "💍", "rarity": "rare"},
    "hoop_earring":  {"name": "Gold Hoop Earring",    "cat": "earring",  "emoji": "⭕", "rarity": "common"},
    "cross_pendant": {"name": "Cross Pendant",        "cat": "necklace", "emoji": "✝️",  "rarity": "uncommon"},
    # Body & facial piercings (Banter's core service line)
    "nose_stud":       {"name": "Nose Stud",             "cat": "piercing", "emoji": "✨", "rarity": "common"},
    "septum_ring":     {"name": "Septum Ring",           "cat": "piercing", "emoji": "🌙", "rarity": "rare"},
    "helix_hoop":      {"name": "Helix Hoop",            "cat": "piercing", "emoji": "⭕", "rarity": "uncommon"},
    "cartilage_stud":  {"name": "Cartilage Stud",        "cat": "piercing", "emoji": "💠", "rarity": "common"},
    "tragus_diamond":  {"name": "Tragus Diamond Stud",   "cat": "piercing", "emoji": "💎", "rarity": "epic"},
    "eyebrow_bar":     {"name": "Eyebrow Bar",           "cat": "piercing", "emoji": "➖", "rarity": "rare"},
    "lip_ring":        {"name": "Lip Ring",              "cat": "piercing", "emoji": "💋", "rarity": "uncommon"},
    "industrial_bar":  {"name": "Industrial Bar",        "cat": "piercing", "emoji": "⚡", "rarity": "epic"},
    "belly_ring":      {"name": "Belly Button Ring",     "cat": "piercing", "emoji": "🔗", "rarity": "rare"},
    "conch_diamond":   {"name": "Conch Diamond Ring",    "cat": "piercing", "emoji": "🌟", "rarity": "legendary"},
}

RARITY_COLORS = {
    "legendary": "#E4F26A",  # bright banter lime
    "epic":      "#D5E547",  # banter lime
    "rare":      "#8FA5FF",  # sapphire
    "uncommon":  "#5EEAD4",  # mint
    "common":    "#8B8B8B",  # slate
}

SCANNABLE_POOL = [
    "diamond_stud", "rose_chain", "signet_ring", "hoop_earring", "cross_pendant",
    "nose_stud", "septum_ring", "helix_hoop", "cartilage_stud", "tragus_diamond",
    "eyebrow_bar", "lip_ring", "industrial_bar", "belly_ring", "conch_diamond",
]


def parse_unlocked(user: dict) -> list[str]:
    raw = user.get("unlocked_items")
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return []
    s = str(raw).strip()
    if not s or s.lower() == "nan":
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


def format_item(item_id: str) -> dict | None:
    return JEWELRY_CATALOG.get(item_id)


def unlock_item(email: str, item_id: str) -> bool:
    """Append item to user's unlocked_items. Returns True if newly added."""
    users = db.read("users").copy()
    mask = users["email"].str.lower() == email.lower()
    if not mask.any():
        return False
    row = users[mask].iloc[0]
    current = parse_unlocked(row.to_dict())
    if item_id in current:
        return False
    current.append(item_id)
    users.loc[mask, "unlocked_items"] = ",".join(current)
    db.write("users", users)
    return True


def save_gender(email: str, gender: str) -> None:
    users = db.read("users").copy()
    mask = users["email"].str.lower() == email.lower()
    if mask.any():
        users.loc[mask, "gender"] = gender
        db.write("users", users)


def league_ranking() -> pd.DataFrame:
    users = db.read("users")
    return users.sort_values(["level", "xp"], ascending=[False, False]).reset_index(drop=True)


def personal_period_sales(email: str) -> dict:
    try:
        m = db.read("individual_metrics")
        rows = m[m["employee_email"].str.lower() == email.lower()]
        return {
            "sales_total":    float(rows["sales_total"].sum()),
            "piercing_sales": float(rows["piercing_sales"].sum()),
            "esa_sales":      float(rows["esa_sales"].sum()),
        }
    except (FileNotFoundError, KeyError):
        return {"sales_total": 0.0, "piercing_sales": 0.0, "esa_sales": 0.0}


def commission_countdown(user: dict, fiscal_month: str = "July") -> dict:
    """FY27-compliant countdown: what tier this user is chasing right now."""
    sales = personal_period_sales(user["email"])
    merch = max(sales["sales_total"] - sales["piercing_sales"] - sales["esa_sales"], 0.0)
    piercing_c = sales["piercing_sales"] * standards.PIERCING_COMMISSION_RATE
    esa_c      = sales["esa_sales"]      * standards.ESA_COMMISSION_RATE
    tier = standards.next_tier(merch, fiscal_month)
    if tier is None:
        return {
            "at_top": True,
            "merch_sales": merch,
            "current_rate": 0.0375,
            "current_commission": merch * 0.0375 + piercing_c + esa_c,
        }
    return {
        "at_top": False,
        "merch_sales": merch,
        "next_level":  tier["level"],
        "next_rate":   tier["rate"],
        "period_target": tier["period_target"],
        "gap":         tier["gap"],
        "pct_to_next": (merch / tier["period_target"] * 100.0) if tier["period_target"] else 0.0,
        "piercing_commission": piercing_c,
        "esa_commission":      esa_c,
        "projected_commission_at_next": tier["period_target"] * tier["rate"] + piercing_c + esa_c,
    }
