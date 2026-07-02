"""Local CSV storage adapter.

Same call surface we'll use when we swap to Google Sheets — only this file changes.
"""
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent.parent / "data"


def _path(table: str) -> Path:
    return DATA_DIR / f"{table}.csv"


@st.cache_data(ttl=30)
def read(table: str) -> pd.DataFrame:
    return pd.read_csv(_path(table))


def write(table: str, df: pd.DataFrame) -> None:
    df.to_csv(_path(table), index=False)
    read.clear()


def append(table: str, row: dict) -> None:
    df = read(table)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    write(table, df)


def purge_feed_older_than(hours: int = 48) -> None:
    try:
        df = read("home_feed")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return
    if df.empty:
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    pinned = df["is_pinned"].astype(str).str.lower().isin(["true", "1", "yes"])
    cutoff = datetime.now() - timedelta(hours=hours)
    fresh = df["timestamp"] >= cutoff
    kept = df[fresh | pinned].copy()
    if len(kept) != len(df):
        write("home_feed", kept)
