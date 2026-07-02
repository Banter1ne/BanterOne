"""Banter FY27 standards and commission tiers, extracted from official PDFs."""
from __future__ import annotations

COMMISSION_TIERS = [
    {"level": 1, "annual_threshold": 50_000,  "rate": 0.005},
    {"level": 2, "annual_threshold": 100_000, "rate": 0.010},
    {"level": 3, "annual_threshold": 150_000, "rate": 0.015},
    {"level": 4, "annual_threshold": 250_000, "rate": 0.020},
    {"level": 5, "annual_threshold": 300_000, "rate": 0.025},
    {"level": 6, "annual_threshold": 400_000, "rate": 0.030},
    {"level": 7, "annual_threshold": 500_000, "rate": 0.0375},
]

MONTHLY_PERCENT = {
    "February": 0.090, "March": 0.075, "April": 0.085, "May": 0.080,
    "June": 0.070,     "July": 0.085,  "August": 0.075, "September": 0.065,
    "October": 0.075,  "November": 0.080, "December": 0.150, "January": 0.070,
}

PIERCING_COMMISSION_RATE = 0.02
ESA_COMMISSION_RATE = 0.05
ANNUAL_QUALIFY_THRESHOLD = 50_000

# Store Manager + Team Member Bonus payout scale.
# Keyed by lower bound of plan attainment %. `sm` = Store Manager / DTSM rate,
# `tm` = All Team Member pool %. From district roster reference sheet.
STORE_BONUS_SCALE = [
    (0.98,  {"sm": 0.0035, "tm": 0.0010}),
    (1.00,  {"sm": 0.0055, "tm": 0.0020}),
    (1.03,  {"sm": 0.0080, "tm": 0.0030}),
    (1.05,  {"sm": 0.0110, "tm": 0.0040}),
    (1.10,  {"sm": 0.0140, "tm": 0.0060}),
    (1.15,  {"sm": 0.0150, "tm": 0.0100}),
    (1.20,  {"sm": 0.0200, "tm": 0.0125}),
    (1.30,  {"sm": 0.0250, "tm": 0.0175}),
]


def store_bonus_rates(pct_of_plan: float) -> dict:
    """Return {'sm', 'tm'} bonus rates for a store's plan attainment %."""
    if pct_of_plan < 0.98:
        return {"sm": 0.0, "tm": 0.0}
    winner = {"sm": 0.0, "tm": 0.0}
    for threshold, rates in STORE_BONUS_SCALE:
        if pct_of_plan >= threshold:
            winner = rates
    return winner


def period_target_for(annual_threshold: int, fiscal_month: str) -> float:
    return annual_threshold * MONTHLY_PERCENT[fiscal_month]


def next_tier(current_period_sales: float, fiscal_month: str) -> dict | None:
    for tier in COMMISSION_TIERS:
        target = period_target_for(tier["annual_threshold"], fiscal_month)
        if current_period_sales < target:
            return {**tier, "period_target": target, "gap": target - current_period_sales}
    return None


def commission_dollars(period_merch_sales: float, tier_rate: float,
                       piercing_sales: float = 0, esa_sales: float = 0) -> dict:
    merch = period_merch_sales * tier_rate
    piercing = piercing_sales * PIERCING_COMMISSION_RATE
    esa = esa_sales * ESA_COMMISSION_RATE
    return {"merch": merch, "piercing": piercing, "esa": esa,
            "total": merch + piercing + esa}
