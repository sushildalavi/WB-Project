"""Typed loaders for the canonical datasets used by analysis & dashboard.

The on-disk human-coding files preserve their original published headers (with
whitespace and embedded newlines from the question-bank phrasing). Loaders
apply ``clean_columns`` in memory at load time so downstream code sees clean
column names without any on-disk modification to the source data.
"""
from __future__ import annotations

import pandas as pd

from wbproj import paths
from wbproj.clean import clean_columns, expand_themes_column

_VIRAL_DATE_FORMAT = "%m/%d/%y %H:%M"
_VIRAL_NUMERIC_COLS = (
    "viewCount",
    "likes",
    "numberOfSubscribers",
    "ReachFactor",
    "EngagementEfficiency",
    "VelocityFactor",
    "ViralityScore",
)


def load_mih_human_coding() -> pd.DataFrame:
    """India human-coded YouTube comments (114 rows, codebook v2 — gold release).

    Loaded from the byte-identical mirror of the published pilot dataset.
    """
    df = pd.read_excel(paths.INDIA.human_coding)
    return clean_columns(df)


def load_mih_human_coding_extended() -> pd.DataFrame:
    """India *extended* human-coded YouTube comments (951 rows, codebook v1).

    A larger working sample produced after the pilot release. Returns one row
    per (comment, theme) pair after exploding the ``themes`` column.
    """
    df = pd.read_excel(paths.INDIA.human_coding_extended)
    df = clean_columns(df)
    df = df.rename(
        columns={"Comment Text": "comment_text", "Themes": "themes", "Sentiment": "sentiment"}
    )
    df = df.dropna(subset=["themes", "sentiment"]).reset_index(drop=True)
    return expand_themes_column(df, col="themes")


def load_mih_virality() -> pd.DataFrame:
    """India clip-level virality metrics (396 clips)."""
    df = pd.read_csv(paths.INDIA.virality)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format=_VIRAL_DATE_FORMAT, errors="coerce")
    for col in _VIRAL_NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_bbnaija_human_coding() -> pd.DataFrame:
    """Nigeria human-coded Nairaland comments (100 rows)."""
    df = pd.read_excel(paths.NIGERIA.human_coding)
    df = clean_columns(df)
    df = df.rename(
        columns={"Comment Text": "comment_text", "Themes": "themes", "Sentiment": "sentiment"}
    )
    df = df.dropna(subset=["comment_text", "themes", "sentiment"])
    for c in ("comment_text", "themes", "sentiment"):
        df[c] = df[c].astype(str)
    return df


def load_rhon_human_coding() -> pd.DataFrame:
    """Kenya human-coded comments (115 rows — gold release)."""
    df = pd.read_csv(paths.KENYA.human_coding)
    return clean_columns(df)


def load_bbnaija_tiktok() -> pd.DataFrame:
    """Optional BBNaija TikTok metrics. Returns empty df if file isn't present."""
    if not paths.NIGERIA.tiktok.exists():
        return pd.DataFrame()
    df = pd.read_excel(paths.NIGERIA.tiktok)
    for col in ("views", "likes", "comments", "shares", "followers", "days_since_posted"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    views = df["views"].replace(0, 1) if "views" in df.columns else 1
    followers = df["followers"].replace(0, 1) if "followers" in df.columns else 1
    days = df["days_since_posted"].replace(0, 1) if "days_since_posted" in df.columns else 1

    if "likes" in df.columns:
        df["like_rate"] = df["likes"] / views
    if "comments" in df.columns:
        df["comment_rate"] = df["comments"] / views
    if "shares" in df.columns:
        df["share_rate"] = df["shares"] / views
    if {"likes", "comments", "shares"}.issubset(df.columns):
        df["engagement_rate"] = (df["likes"] + df["comments"] + df["shares"]) / views
        df["velocity"] = (df["likes"] + df["comments"] + df["shares"]) / days
    if "shares" in df.columns:
        df["amplification_rate"] = df["shares"] / followers
    if "views" in df.columns:
        df["reach_factor"] = df["views"] / followers
    return df
