# Pipeline stages

The report (Section 2.2) describes a 5-stage standardized pipeline. This is
how each stage maps onto folders in this repo.

| Report stage | Folder | What lives here |
|--------------|--------|-----------------|
| **1. Raw** | `data/raw/{country}/` | Minimally processed platform output. Original fields preserved. Nothing in here is modified. |
| **2. Standardized + 3. Cleaned** | `data/interim/{country}/` | Schema-aligned + lightly normalized (URL strip, whitespace, dedup). Emojis, slang, and code-switching are *retained* — they encode tone and cultural context. |
| **4. Candidate / Shortlist** | `data/interim/{country}/` (rerank outputs) | High-recall shortlist via keyword families + semantic similarity (`text-embedding-3-large`, cosine). Permissive by design. |
| **5. Analysis-Ready** | `data/processed/{country}/` | Final curated subset for human / LLM coding. Fixed Top-N. |
| Reach layer (separate) | `data/reach/{country}/` | Per-video / per-clip engagement metrics for context. Not used for thematic coding. |
| Ground truth | `data/human_coded/{country}/` | Focused subsets coded by 3 trained human annotators. |

## Country-specific volumes

The report reports the *full pre-dedup scrape* counts; what's shipped in
this repo is the *deduplicated raw* layer (`data/raw/`). Both numbers
appear below for transparency.

| Country | Pre-dedup scrape (report §2.1) | Shipped raw rows | Analysis-Ready | Focused (LLM + Human) |
|---------|---|---|---|---|
| Nigeria | 32,383 Nairaland posts | 21,155 | 922 | 100 / 100 |
| India   | 99,049 YouTube comments | 99,049 | 951 | 102 / 102 |
| Kenya   | 19,394 tweets (file lines) | 10,000 records | 3,140 | 103 / 103 |

Notes on counts:
- Nigeria's raw scrape was 32,383 posts before deduplication; the shipped
  `BBNaija_nairaland.csv` contains 21,155 deduplicated records.
- Kenya's `RHONairobi_tweets.csv` is 19,394 file-lines but **10,000
  records** (some tweets contain embedded newlines that bloat the line count).
  pandas reads 10,000 rows. The report's "19,394 tweets" is the file line
  count.

## Models (from Appendix C7 + actual notebook usage)

- Embedding: `text-embedding-3-large` (3072 dimensions), cosine similarity
- **Production labeling** (`gpt-5.1`, temperature `0`, strict JSON output) — themes, sentiment, emotion, sexism flags. Validated against the closed-set country taxonomy in [`codebook/codebook_spec.md`](../codebook/codebook_spec.md).
- **Auxiliary lightweight** (`gpt-4o-mini`) — language tagging, coarse pre-filters, API health checks. Not part of the report's primary outputs; faster and cheaper for non-substantive tasks.

Both model names are pinned in [`src/wbproj/config.py`](../src/wbproj/config.py) (`OPENAI_MODEL` and `OPENAI_MODEL_LIGHT`).

## What each repo file is for

### India (`data/{stage}/india/`)

| File | Stage | What it is |
|------|-------|-----------|
| `MIH_S2_full_data.xlsx` | raw | 99,049 raw YouTube comments |
| `MIH_S2_yt_videos_data.xlsx` | raw | 396 video-level metadata records |
| `MIH_S2_cleaned.xlsx` | interim | Cleaned + deduped intermediate (4,837 rows) |
| `MIH_S2_final_topic_relevant.xlsx` | analysis-ready | 951 keyword + semantically filtered comments |
| `MIH_S2_for_llm_coding.xlsx` | focused-coding template | 102 rows for the LLM/human matched coding subset |
| `MIH_S2_final_dataset.xlsx` | LLM-coded full | 976 rows after thematic + sentiment + sexism labeling |
| `language_splits/` | analysis-ready breakouts | EN / Hindi / Hinglish CSVs |
| `MIH_S2_youtube_virality.csv` *(in `data/reach/`)* | reach | 396 clips with ReachFactor / EngagementEfficiency / VelocityFactor / ViralityScore |

### Kenya (`data/{stage}/kenya/`)

| File | Stage | What it is |
|------|-------|-----------|
| `RHONairobi_tweets.csv` | raw | 10,000 Twitter/X records |
| `RHONairobi_tiktok.csv` | raw | 253 TikTok records |
| `RHONairobi_yt_comments.xlsx` | raw (extended) | 15,745 YouTube comments — extension beyond pilot |
| `RHONairobi_apify_scraped.xlsx` | raw (extended) | 1,173 fresh Apify pull |
| `RHONairobi_*_cleaned.xlsx` / `*_merged_cleaned.xlsx` | interim | Cleaning & merge stages |
| `RHONairobi_ready_for_rerank.xlsx` | interim | Input to embedding rerank |
| `RHONairobi_gender_classified.xlsx` / `_filtered_rerank.xlsx` | interim | Rerank pipeline outputs |
| `RHONairobi_final_topic_relevant.xlsx` | analysis-ready | 3,140 rows |
| `RHONairobi_for_llm_coding.xlsx` | focused-coding template | 103 rows |
| `RHONairobi_relevant_comments.xlsx` | LLM-coded subset | 416 rows with themes + sentiment |
| `RHONairobi_scored.xlsx` | scored | 4,106 rows scored on Local Culture / Gender Norms / Empowerment axes |
| `RHONairobi_youtube_virality.csv` *(in `data/reach/`)* | reach | 137 clip-level engagement records |

### Nigeria (`data/{stage}/nigeria/`)

| File | Stage | What it is |
|------|-------|-----------|
| `BBNaija_nairaland.csv` | raw | 21,155 Nairaland posts |
| `BBNaija_sentiment_emotions.csv` | processed | 21,155 rows with sentiment + emotion labels |
| `BBNaija_final_topic_relevant.xlsx` | analysis-ready | 922 rows |
| `BBNaija_for_llm_coding.xlsx` | focused-coding template | 100 rows |

> The report references TikTok reach data for BBNaija (~60K comments / 372
> videos) but those data are not currently shipped with the repo. The
> Nigeria reach folder is empty as a placeholder; drop a file at
> `data/raw/nigeria/BBNaija_tiktok.xlsx` to enable the BBNaija TikTok
> dashboard tab.
