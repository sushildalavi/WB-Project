# WB Gender Norms in Reality-TV Social Media Commentary

Research project (World Bank) analysing how viewers discuss gender norms,
gender-based violence, and women's empowerment in social-media commentary
on three reality / drama shows across three countries.

| Country | Show | Platforms |
|---------|------|-----------|
| India | *Made in Heaven* Season 2 (MIH_S2) | YouTube |
| Kenya | *Real Housewives of Nairobi* (RHONairobi) | YouTube, Twitter/X, TikTok |
| Nigeria | *Big Brother Naija* (BBNaija) | Nairaland forum |

## Relationship to the upstream gold release

This repo extends the **NLC-Datasets** pilot release. 16 files in `data/`
are byte-identical mirrors of the gold release (md5-pinned by the validator)
and are the canonical reference data for downstream analysis. Working
extensions (larger samples, additional LLM coding, reranking outputs) live
alongside them with descriptive filenames — they are clearly distinguishable
from gold.

See [`data/GOLD_MANIFEST.md`](data/GOLD_MANIFEST.md) for the full mirror
table and the list of files that are NOT in the gold release.

## Pipeline

```
scrape  →  clean  →  topic-filter  →  LLM coding  →  human coding (sample)  →  analysis & viz
 raw       interim      processed       processed       human_coded            reports/
```

1. **Scrape** raw comments per platform (Apify, etc.).
2. **Clean** (deduplicate, language-detect, strip).
3. **Topic-filter** against the keyword codebook in [`codebook/keywords.docx`](codebook/keywords.docx).
4. **LLM coding** (GPT-4o / 4o-mini) for themes, sentiment, emotions, sexism flags.
5. **Human coding** on a sample using the WB instrument
   ([`codebook/codebook_spec.md`](codebook/codebook_spec.md)) for ground truth.
6. **Analysis** in `notebooks/`; dashboard in `src/app.py`; figures in `reports/`.

## Layout

```
WB-Project/
├── README.md
├── requirements.txt
├── .env.example                    # template for OPENAI_API_KEY
├── .gitignore
├── codebook/
│   ├── keywords.docx               # keyword sets per theme (EN + Hindi/Hinglish)
│   └── codebook_spec.md            # human-coding column spec (v1 + v2)
├── data/
│   ├── GOLD_MANIFEST.md            # gold-release mirror table & checks
│   ├── raw/{india,kenya,nigeria}/        # original scrapes — do not modify
│   ├── interim/{india,kenya,nigeria}/    # cleaned / embedded / reranked
│   ├── processed/{india,kenya,nigeria}/  # final coded datasets used in analysis
│   └── human_coded/{india,kenya,nigeria}/# ground-truth coded samples
├── notebooks/
│   ├── 01_india_mih_pipeline.ipynb
│   ├── 02_kenya_rhon_pipeline.ipynb
│   └── test/test_mih_s2.ipynb
├── src/
│   ├── app.py                            # Streamlit dashboard
│   └── wbproj/                           # shared package
│       ├── paths.py                      # canonical file paths + GOLD_MIRROR
│       ├── clean.py                      # column normalization, theme expansion
│       └── loaders.py                    # typed dataset loaders
├── scripts/
│   ├── patch_notebooks.py                # rewrite legacy paths in notebooks
│   └── validate_data.py                  # 3-layer sanity-check + gold byte-identity
├── reports/
│   ├── figures/{india,kenya}/            # publication PNGs
│   └── docs/{india,kenya}/               # bundled .docx visual reports
└── archive/                              # superseded / older / sample files
    ├── india/  kenya/  nigeria/  misc/
    └── _pre_clean/                       # pre-cleanup snapshots
```

## Human-coded datasets (3 primary + 1 India extension)

| Country | File | Rows × Cols | Source |
|---------|------|-------------|--------|
| India | [`data/human_coded/india/MIH_S2_human_coding_dataset.xlsx`](data/human_coded/india/MIH_S2_human_coding_dataset.xlsx) | 114 × 42 | gold pilot, codebook v2 |
| India *(extension)* | [`data/human_coded/india/MIH_S2_human_coding_extended.xlsx`](data/human_coded/india/MIH_S2_human_coding_extended.xlsx) | 951 × 51 | working extension, codebook v1 |
| Kenya | [`data/human_coded/kenya/RHONairobi_human_coding_dataset.csv`](data/human_coded/kenya/RHONairobi_human_coding_dataset.csv) | 115 × 43 | gold pilot |
| Nigeria | [`data/human_coded/nigeria/BBNaija_human_coding_dataset.xlsx`](data/human_coded/nigeria/BBNaija_human_coding_dataset.xlsx) | 100 × 49 | working extension (not in pilot) |

## "For-LLM-coding" templates (3 datasets, all gold)

| Country | File | Rows × Cols |
|---------|------|-------------|
| India | [`data/processed/india/MIH_S2_for_llm_coding.xlsx`](data/processed/india/MIH_S2_for_llm_coding.xlsx) | 102 × 47 |
| Kenya | [`data/processed/kenya/RHONairobi_for_llm_coding.xlsx`](data/processed/kenya/RHONairobi_for_llm_coding.xlsx) | 103 × 48 |
| Nigeria | [`data/processed/nigeria/BBNaija_for_llm_coding.xlsx`](data/processed/nigeria/BBNaija_for_llm_coding.xlsx) | 100 × 47 |

## Other canonical datasets

Row counts verified by `scripts/validate_data.py`. **Gold ✓** = byte-identical
to the upstream NLC-Datasets pilot release (md5-pinned by Layer 3).

### India (Made in Heaven S2 — YouTube)
| Stage | File | Rows × Cols | Gold |
|-------|------|-------------|:----:|
| Raw (comments) | [`data/raw/india/MIH_S2_full_data.xlsx`](data/raw/india/MIH_S2_full_data.xlsx) | 99,049 × 8 | ✓ |
| Raw (videos) | [`data/raw/india/MIH_S2_yt_videos_data.xlsx`](data/raw/india/MIH_S2_yt_videos_data.xlsx) | 396 × 10 | ✓ |
| Interim (cleaned) | [`data/interim/india/MIH_S2_cleaned.xlsx`](data/interim/india/MIH_S2_cleaned.xlsx) | 4,837 × 9 | |
| Topic-relevant | [`data/processed/india/MIH_S2_final_topic_relevant.xlsx`](data/processed/india/MIH_S2_final_topic_relevant.xlsx) | 951 × 3 | ✓ |
| LLM-coded final | [`data/processed/india/MIH_S2_final_dataset.xlsx`](data/processed/india/MIH_S2_final_dataset.xlsx) | 976 × 15 | |
| Virality | [`data/processed/india/MIH_S2_virality_report.csv`](data/processed/india/MIH_S2_virality_report.csv) | 396 × 15 | ✓ |
| Language splits | [`data/processed/india/language_splits/`](data/processed/india/language_splits/) | EN/HI/Hinglish | |

### Kenya (Real Housewives of Nairobi)
| Stage | File | Rows × Cols | Gold |
|-------|------|-------------|:----:|
| Raw (Twitter/X) | [`data/raw/kenya/RHONairobi_tweets.csv`](data/raw/kenya/RHONairobi_tweets.csv) | 10,000 × 10 | ✓ |
| Raw (TikTok) | [`data/raw/kenya/RHONairobi_tiktok.csv`](data/raw/kenya/RHONairobi_tiktok.csv) | 253 × 13 | ✓ |
| Raw (YouTube — extended) | [`data/raw/kenya/RHONairobi_yt_comments.xlsx`](data/raw/kenya/RHONairobi_yt_comments.xlsx) | 15,745 × 9 | |
| Raw (Apify — extended) | [`data/raw/kenya/RHONairobi_apify_scraped.xlsx`](data/raw/kenya/RHONairobi_apify_scraped.xlsx) | 1,173 × 12 | |
| Interim (rerank pipeline) | `data/interim/kenya/RHONairobi_*` | 5 files | |
| Topic-relevant | [`data/processed/kenya/RHONairobi_final_topic_relevant.xlsx`](data/processed/kenya/RHONairobi_final_topic_relevant.xlsx) | 3,140 × 3 | ✓ |
| Relevant subset | [`data/processed/kenya/RHONairobi_relevant_comments.xlsx`](data/processed/kenya/RHONairobi_relevant_comments.xlsx) | 416 × 4 | |
| Scored | [`data/processed/kenya/RHONairobi_scored.xlsx`](data/processed/kenya/RHONairobi_scored.xlsx) | 4,106 × 14 | |
| Videos virality | [`data/processed/kenya/RHONairobi_videos_virality.csv`](data/processed/kenya/RHONairobi_videos_virality.csv) | 137 × 14 | ✓ |

### Nigeria (Big Brother Naija)
| Stage | File | Rows × Cols | Gold |
|-------|------|-------------|:----:|
| Raw | [`data/raw/nigeria/BBNaija_nairaland.csv`](data/raw/nigeria/BBNaija_nairaland.csv) | 21,155 × 13 | ✓ |
| Sentiment + emotions | [`data/processed/nigeria/BBNaija_sentiment_emotions.csv`](data/processed/nigeria/BBNaija_sentiment_emotions.csv) | 21,155 × 16 | ✓ |
| Topic-relevant | [`data/processed/nigeria/BBNaija_final_topic_relevant.xlsx`](data/processed/nigeria/BBNaija_final_topic_relevant.xlsx) | 922 × 3 | ✓ |

## Setup & reproduction

```bash
# 1. install deps
pip install -r requirements.txt

# 2. configure secrets (only needed if you re-run the LLM coding cells)
cp .env.example .env       # then edit and add OPENAI_API_KEY

# 3. validate the data layout (40+ assertions; non-zero exit on failure)
python scripts/validate_data.py

# 4. run the dashboard
streamlit run src/app.py
```

The Streamlit app reads files relative to the repo root via `pathlib`, so it
runs from any working directory. The BBNaija TikTok tab is empty unless you
drop an `xlsx` at `data/raw/nigeria/BBNaija_tiktok.xlsx` (BBNaija raw data is
Nairaland forum posts, not TikTok — that tab is a placeholder).

## Validator (3 layers)

`scripts/validate_data.py` runs three independent layers on every invocation:

| Layer | What it checks | Files |
|-------|----------------|-------|
| 1 — canonical | row counts, required columns, **strict** header cleanness | 17 working / scrape / pipeline files |
| 2 — original-headers | row counts, required columns (headers preserved as-published) | 7 human-coded + for-LLM templates |
| 3 — byte-identity | md5 vs upstream `NLC-Datasets-main/` | 16 gold-mirror files |

The on-disk human-coding files preserve their original published headers
(with whitespace, embedded newlines, and Q-bank phrasing). Loaders apply
`clean_columns` in memory at load time, so downstream code sees clean
column names without any on-disk modification.

Layer 3 reports `SKIP` (not `FAIL`) when the upstream gold directory is
absent, so the validator is portable.

## archive/

Holds language variants, older codebook revisions, and small subsamples kept
for provenance. `archive/_pre_clean/` snapshots from a brief experiment with
on-disk header normalization (which has since been reverted in favour of
load-time normalization). Nothing in the active pipeline reads from
`archive/`.
