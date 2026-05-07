"""Rewrite hardcoded absolute paths in the legacy notebooks to point at the
canonical files in the current repo layout. Also:

  * Insert a header markdown cell describing the pipeline.
  * Replace `pip install ...` code cells with a markdown pointer to requirements.txt.

This script is idempotent — re-running on an already-patched notebook is a
no-op.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

INDIA_HEADER = (
    "# India — *Made in Heaven* S2 (YouTube) pipeline\n\n"
    "End-to-end pipeline used to produce the canonical India datasets:\n\n"
    "1. **Filter** raw YouTube comments → `data/interim/india/MIH_S2_cleaned.xlsx`\n"
    "2. **Embedding-based rerank** for gender relevance → interim files in `archive/india/test_*`\n"
    "3. **LLM coding** (themes, sentiment, emotions, sexism) → `data/processed/india/MIH_S2_final_dataset.xlsx`\n"
    "4. **Virality scoring** of YT clips → `data/processed/india/MIH_S2_virality_report.csv`\n"
    "5. **Human-coded ground truth** lives at `data/human_coded/india/MIH_S2_human_coding_extended.xlsx`\n\n"
    "Path constants in legacy cells have been rewritten to point at the canonical\n"
    "locations in this repo. Cells assume the notebook is run from `notebooks/`.\n"
    "Install dependencies once: `pip install -r requirements.txt` (from repo root)."
)

KENYA_HEADER = (
    "# Kenya — *Real Housewives of Nairobi* (Twitter/X + YouTube + TikTok) pipeline\n\n"
    "End-to-end pipeline used to produce the canonical Kenya datasets:\n\n"
    "1. **Merge** raw scrapes from Twitter/X, YouTube, TikTok → `data/interim/kenya/RHONairobi_merged_cleaned.xlsx`\n"
    "2. **Rerank** for relevance → `data/interim/kenya/RHONairobi_ready_for_rerank.xlsx`\n"
    "3. **Gender classification** + filter → `data/interim/kenya/RHONairobi_gender_*`\n"
    "4. **Relevant subset** → `data/processed/kenya/RHONairobi_relevant_comments.xlsx`\n"
    "5. **Final scoring** (Local Culture / Gender Norms / Empowerment) → `data/processed/kenya/RHONairobi_scored.xlsx`\n"
    "6. **Human-coded ground truth** lives at `data/human_coded/kenya/RHONairobi_human_coding_dataset.csv`\n\n"
    "Path constants in legacy cells have been rewritten to point at the canonical\n"
    "locations in this repo. Cells assume the notebook is run from `notebooks/`.\n"
    "Install dependencies once: `pip install -r requirements.txt` (from repo root)."
)

PATH_MAP_INDIA = {
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_FINa.xlsx": "../data/raw/india/MIH_S2_full_data.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_filtered.xlsx": "../data/interim/india/MIH_S2_cleaned.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/mih_s2_yt_filtered.xlsx": "../data/interim/india/MIH_S2_cleaned.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_gender_filtered_rerank.xlsx": "../archive/india/test_MIH_S2_gender_filtered_rerank.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_gender_classified.xlsx": "../archive/india/test_MIH_S2_gender_classified.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_gender_classified_fixed.xlsx": "../archive/india/test_MIH_S2_gender_classified_fixed.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/WB Social Media Coding.xlsx": "../archive/misc/wb_social_media_coding_45rows.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_codebook_ready.xlsx": "../data/interim/india/MIH_S2_codebook_ready.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2 YT Human Coding Results.xlsx": "../data/human_coded/india/MIH_S2_human_coding_extended.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2 YT Human Coding Results - Final.xlsx": "../data/human_coded/india/MIH_S2_human_coding_extended.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_YT_Human_Coding_with_Emotions.xlsx": "../data/interim/india/MIH_S2_yt_human_coding_with_emotions.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/mih_s2_virality_report_improved.csv": "../data/processed/india/MIH_S2_virality_report.csv",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_FinalDataset_no_duplicates.xlsx": "../archive/india/MIH_S2_final_dataset__no_dup.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_FinalDataset_with_sexism.xlsx": "../archive/india/MIH_S2_final_dataset__with_sexism_pre_merge.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_FinalDataset_with_sexism_merged.xlsx": "../data/processed/india/MIH_S2_final_dataset.xlsx",
    "/Users/sushildalavi/Desktop/MIH_S2/MIH_S2_Final_200_Mix.xlsx": "../archive/india/MIH_S2_final_200_mix.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/MIH_S2 YT Human Coding Results - Final.xlsx": "../data/human_coded/india/MIH_S2_human_coding_extended.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/MIH_S2 YT for LLM Coding.xlsx": "../archive/india/MIH_S2_yt_for_llm_coding__193rows.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/MIH_S2 YT Human Coding Results - Final____lang.xlsx": "../archive/india/MIH_S2_yt_human_coding_results__lang.xlsx",
}

PATH_MAP_KENYA = {
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhonairobi_scored.xlsx": "../data/processed/kenya/RHONairobi_scored.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhon_YTcomments.xlsx": "../data/raw/kenya/RHONairobi_yt_comments.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhon_apify_scraped_cleaned.xlsx": "../data/interim/kenya/RHONairobi_apify_scraped_cleaned.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhon_merged_cleaned.xlsx": "../data/interim/kenya/RHONairobi_merged_cleaned.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhon_ready_for_rerank.xlsx": "../data/interim/kenya/RHONairobi_ready_for_rerank.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhon_gender_filtered_rerank.xlsx": "../data/interim/kenya/RHONairobi_gender_filtered_rerank.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhon_gender_classified.xlsx": "../data/interim/kenya/RHONairobi_gender_classified.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/rhon_relevant_comments.xlsx": "../data/processed/kenya/RHONairobi_relevant_comments.xlsx",
    "/Users/sushildalavi/Desktop/NLC/WBProj/RHON YT & X for LLM Coding.xlsx": "../archive/kenya/RHON_yt_x_for_llm_coding.xlsx",
}

PIP_RE = re.compile(r"^\s*(?:!|%)?\s*pip\s+install\b", re.MULTILINE)
HEADER_MARKER = "<!-- WBPROJ_PATCHED -->"


def _md_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True) or [text],
    }


def _is_pip_install(cell: dict) -> bool:
    if cell.get("cell_type") != "code":
        return False
    src = "".join(cell.get("source", [])).strip()
    if not src:
        return False
    # treat as pip-install cell only if EVERY non-empty line is a pip-install line
    lines = [ln for ln in src.splitlines() if ln.strip()]
    return all(PIP_RE.match(ln) for ln in lines)


def patch(path: Path, header: str, mapping: dict[str, str]) -> None:
    nb = json.loads(path.read_text())

    # Idempotency: header already inserted?
    first = nb["cells"][0] if nb["cells"] else None
    already = first and first.get("cell_type") == "markdown" and HEADER_MARKER in "".join(first.get("source", []))

    new_cells: list[dict] = []
    if not already:
        new_cells.append(_md_cell(f"{HEADER_MARKER}\n{header}\n"))

    for cell in nb["cells"]:
        # Skip the old "# Rhon Data Cleaning & Keyword Filter" markdown — superseded
        if cell.get("cell_type") == "markdown":
            txt = "".join(cell.get("source", [])).strip()
            if HEADER_MARKER in txt:
                continue  # drop stale header
            if txt in {"# Rhon Data Cleaning & Keyword Filter"}:
                continue

        if _is_pip_install(cell):
            new_cells.append(
                _md_cell(
                    "Dependencies are pinned in `requirements.txt`. "
                    "Install once from the repo root:\n\n"
                    "```bash\npip install -r requirements.txt\n```\n"
                )
            )
            continue

        if cell.get("cell_type") == "code":
            src = "".join(cell.get("source", []))
            for old, new in mapping.items():
                src = src.replace(old, new)
            cell = {**cell, "source": src.splitlines(keepends=True) or [""]}

        new_cells.append(cell)

    nb["cells"] = new_cells
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
    print(f"  patched: {path.relative_to(REPO)}  ({len(new_cells)} cells)")


def main() -> int:
    patch(REPO / "notebooks/01_india_mih_pipeline.ipynb", INDIA_HEADER, PATH_MAP_INDIA)
    patch(REPO / "notebooks/02_kenya_rhon_pipeline.ipynb", KENYA_HEADER, PATH_MAP_KENYA)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
