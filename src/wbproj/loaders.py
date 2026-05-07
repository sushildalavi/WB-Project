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
    """Kenya human-coded comments (115 rows — gold release).

    The Kenya v2 codebook does not have a top-level ``Sentiment`` column;
    sentiment-like signals live in attitude-toward-* columns. ``comment_text``
    is exposed for parity with the India and Nigeria loaders.
    """
    df = pd.read_csv(paths.KENYA.human_coding)
    df = clean_columns(df)
    if "Comment Text" in df.columns:
        df = df.rename(columns={"Comment Text": "comment_text"})
    return df


#: Columns the BBNaija TikTok loader knows how to handle. The file is optional;
#: if you supply one, it should contain at least these:
TIKTOK_REQUIRED_COLUMNS = ("video_url", "views", "likes", "comments", "shares")
#: Optional columns; if present, additional metrics will be computed.
TIKTOK_OPTIONAL_COLUMNS = (
    "created_at",
    "Author Username",
    "followers",
    "days_since_posted",
    "Hashtag1",
    "Hashtag2",
    "Hashtag3",
)


def load_bbnaija_tiktok() -> pd.DataFrame:
    """Optional BBNaija TikTok metrics.

    Returns an empty df if no file is shipped at ``paths.NIGERIA.tiktok``.
    If a file *is* present but the required columns are missing, this raises
    a ``ValueError`` rather than silently producing a half-loaded frame.

    Required columns: ``video_url, views, likes, comments, shares``.

    Optional columns that, if present, get used:
    ``created_at``, ``Author Username``, ``followers``, ``days_since_posted``,
    ``Hashtag1``, ``Hashtag2``, ``Hashtag3``.

    Computed when the underlying inputs exist:
    ``like_rate``, ``comment_rate``, ``share_rate``, ``engagement_rate``,
    ``amplification_rate``, ``reach_factor``, ``velocity``.
    """
    if not paths.NIGERIA.tiktok.exists():
        return pd.DataFrame()
    df = pd.read_excel(paths.NIGERIA.tiktok)
    missing = [c for c in TIKTOK_REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"BBNaija TikTok file at {paths.NIGERIA.tiktok} is missing required "
            f"columns {missing}. Required: {list(TIKTOK_REQUIRED_COLUMNS)}; "
            f"optional: {list(TIKTOK_OPTIONAL_COLUMNS)}."
        )
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
