"""Column-header normalization and theme-list expansion.

`clean_columns` is idempotent. It only touches the column index, never values.
"""
from __future__ import annotations

import ast
import re

import pandas as pd

_WS_RUNS = re.compile(r"\s+")


def clean_columns(df: pd.DataFrame, drop_empty_dups: bool = True) -> pd.DataFrame:
    """Strip whitespace and embedded newlines/tabs from column names.

    - Collapses runs of whitespace inside the name to a single space.
    - When two columns share a normalized name, pandas appends `.1`, `.2`...
      If `drop_empty_dups`, those suffixed columns are dropped *only* when
      they are entirely empty (all-NaN).
    """
    df = df.copy()
    new_cols = [_WS_RUNS.sub(" ", str(c)).strip() for c in df.columns]
    df.columns = new_cols

    if drop_empty_dups:
        keep = []
        for i, c in enumerate(df.columns):
            if re.search(r"\.\d+$", c) and df.iloc[:, i].isna().all():
                continue
            keep.append(i)
        df = df.iloc[:, keep]
    return df


def expand_themes_column(df: pd.DataFrame, col: str = "themes") -> pd.DataFrame:
    """Explode a `themes` column into one row per theme.

    Accepts plain strings, comma-separated strings, or python-list-like strings
    (e.g. ``"['Marriage/Husband-Wife', 'Money/Prize/Votes']"``).
    """

    def to_list(val):
        if pd.isna(val):
            return []
        s = str(val).strip()
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return [str(t).strip().strip("[]'\" ") for t in parsed if str(t).strip()]
        except (ValueError, SyntaxError):
            pass
        parts = [p.strip().strip("[]'\" ") for p in s.split(",") if p.strip()]
        if parts:
            return parts
        return [s.strip("[]'\" ")]

    out = df.copy()
    out["_themes_list"] = out[col].apply(to_list)
    out = out.explode("_themes_list")
    out[col] = out["_themes_list"].astype(str).str.strip()
    return out.drop(columns=["_themes_list"])
