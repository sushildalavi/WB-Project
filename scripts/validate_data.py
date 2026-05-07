"""Sanity check every canonical dataset.

Three layers of assertion:
  (1) Canonical (strict-headers) — files produced by the working pipeline.
      Asserts row counts, required columns, and clean column headers.
  (2) Original-headers — files that preserve original published phrasing
      (whitespace, embedded newlines). Headers are NOT asserted clean here;
      loaders apply ``clean_columns`` in memory at load time.
  (3) Gold byte-identity — every file declared in ``paths.GOLD_MIRROR`` is
      md5-checked against the upstream NLC-Datasets release.

Exits non-zero if any FAIL — suitable for CI / pre-merge gates.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import pandas as pd

from wbproj import paths

# Layer 1 — strict header cleanness asserted.
# (path, expected_rows_min, expected_rows_max, required_columns)
CANONICAL_CHECKS: list[tuple[Path, int, int, tuple[str, ...]]] = [
    # India
    (paths.INDIA.raw_full, 99000, 99100, ("author", "comment", "pageUrl")),
    (paths.INDIA.raw_videos, 390, 400, ("title", "url", "viewCount")),
    (paths.INDIA.cleaned, 4830, 4840, ()),
    (paths.INDIA.topic_relevant, 950, 952, ("comment", "themes", "sentiment")),
    (paths.INDIA.final_dataset, 970, 980, ("themes", "sentiment", "sexist_flag")),
    (paths.INDIA.virality, 390, 400, ("title", "ViralityScore", "viewCount")),
    # Kenya
    (paths.KENYA.raw_tweets, 9990, 10010, ("id", "text", "createdAt")),
    (paths.KENYA.raw_tiktok, 250, 260, ("text", "diggCount", "playCount")),
    (paths.KENYA.raw_yt, 15700, 15800, ("author", "comment", "videoID")),
    (paths.KENYA.raw_apify, 1170, 1180, ("text", "createdAt", "likeCount")),
    (paths.KENYA.topic_relevant, 3130, 3150, ("comment", "themes", "sentiment")),
    (paths.KENYA.relevant_comments, 410, 420, ()),
    (paths.KENYA.scored, 4100, 4110, ("Score_Local_Culture", "Score_Gender_Norms")),
    (paths.KENYA.videos_virality, 130, 140, ()),
    # Nigeria
    (paths.NIGERIA.raw_nairaland, 21000, 21200, ("Comment", "Username")),
    (paths.NIGERIA.sentiment_emotions, 21000, 21200, ("Sentiment", "Emotion")),
    (paths.NIGERIA.topic_relevant, 920, 925, ("comment", "themes", "sentiment")),
]

# Layer 2 — original headers preserved (whitespace allowed). Cleanness is not
# asserted; loaders normalize at load time.
ORIGINAL_HEADER_CHECKS: list[tuple[Path, int, int, tuple[str, ...]]] = [
    (paths.INDIA.human_coding, 114, 114, ("Comment Text",)),
    (paths.INDIA.human_coding_extended, 950, 952, ("Comment Text", "Themes", "Sentiment")),
    (paths.INDIA.for_llm_coding, 102, 102, ("Comment Text",)),
    (paths.KENYA.for_llm_coding, 103, 103, ("Comment Text",)),
    (paths.KENYA.human_coding, 115, 115, ("Comment Text",)),
    (paths.NIGERIA.for_llm_coding, 100, 100, ("Comment ID", "Comment Text")),
    (paths.NIGERIA.human_coding, 100, 100, ("Comment Text", "Themes", "Sentiment")),
]


_BAD_HEADER = re.compile(r"[\n\t]")


def _md5(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _check(
    path: Path, lo: int, hi: int, required: tuple[str, ...], strict_headers: bool
) -> list[str]:
    if not path.exists():
        return [f"missing: {path}"]
    try:
        df = pd.read_csv(path) if path.suffix == ".csv" else pd.read_excel(path)
    except Exception as e:
        return [f"read failed: {e}"]
    errs: list[str] = []
    n = len(df)
    if not (lo <= n <= hi):
        errs.append(f"row count {n} outside expected [{lo}, {hi}]")
    for col in required:
        if col not in df.columns:
            errs.append(f"missing required column: {col!r}")
    if strict_headers:
        for col in df.columns:
            s = str(col)
            if s != s.strip():
                errs.append(f"untrimmed column header: {s!r}")
            if _BAD_HEADER.search(s):
                errs.append(f"newline/tab in column header: {s!r}")
            if re.search(r"\.\d+$", s) and df[col].isna().all():
                errs.append(f"empty .N duplicate column not dropped: {s!r}")
    return errs


def main() -> int:
    n_ok = n_fail = n_skip = 0

    print("=== Layer 1: canonical files (strict headers) ===\n")
    for path, lo, hi, req in CANONICAL_CHECKS:
        errs = _check(path, lo, hi, req, strict_headers=True)
        rel = path.relative_to(paths.REPO_ROOT)
        if errs:
            n_fail += 1
            print(f"  FAIL  {rel}")
            for e in errs:
                print(f"        - {e}")
        else:
            n_ok += 1
            print(f"  OK    {rel}")

    print("\n=== Layer 2: original-header files (cleaned in memory by loaders) ===\n")
    for path, lo, hi, req in ORIGINAL_HEADER_CHECKS:
        errs = _check(path, lo, hi, req, strict_headers=False)
        rel = path.relative_to(paths.REPO_ROOT)
        if errs:
            n_fail += 1
            print(f"  FAIL  {rel}")
            for e in errs:
                print(f"        - {e}")
        else:
            n_ok += 1
            print(f"  OK    {rel}")

    print("\n=== Layer 3: byte-identity vs upstream gold release ===")
    print(f"     gold release at: {paths.GOLD_RELEASE}\n")
    for repo_path, gold_path in paths.GOLD_MIRROR.items():
        rel = repo_path.relative_to(paths.REPO_ROOT)
        if not repo_path.exists():
            n_fail += 1
            print(f"  FAIL  {rel}: missing in repo")
            continue
        if not gold_path.exists():
            n_skip += 1
            print(f"  SKIP  {rel}: gold not present at {gold_path}")
            continue
        rh = _md5(repo_path)
        gh = _md5(gold_path)
        if rh == gh:
            n_ok += 1
            print(f"  OK    {rel}  (md5 {rh[:12]}…)")
        else:
            n_fail += 1
            print(f"  FAIL  {rel}: md5 {rh[:12]}  vs gold {gh[:12]}")

    print(f"\n{n_ok} OK, {n_fail} FAIL, {n_skip} SKIP")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
