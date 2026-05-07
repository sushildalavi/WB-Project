# Gold-release alignment manifest

This repo extends the published pilot release **NLC-Datasets** with working
data, code, and visualizations. The 16 files listed below are byte-identical
to the upstream gold release; their md5 hashes are pinned by
`scripts/validate_data.py` (Layer 3).

**Upstream gold release**: `/Users/sushildalavi/Desktop/NLC/NLC-Datasets-main`

## Mirror table

| Gold release path | Repo path |
|-------------------|-----------|
| `India_MIH_S2/MIH_S2_FullData.xlsx` | [`data/raw/india/MIH_S2_full_data.xlsx`](raw/india/MIH_S2_full_data.xlsx) |
| `India_MIH_S2/MIH_S2_YTvidsdata.xlsx` | [`data/raw/india/MIH_S2_yt_videos_data.xlsx`](raw/india/MIH_S2_yt_videos_data.xlsx) |
| `India_MIH_S2/MIH_S2_Final_Topic Relevant.xlsx` | [`data/processed/india/MIH_S2_final_topic_relevant.xlsx`](processed/india/MIH_S2_final_topic_relevant.xlsx) |
| `India_MIH_S2/MIH_S2 for LLM Coding.xlsx` | [`data/processed/india/MIH_S2_for_llm_coding.xlsx`](processed/india/MIH_S2_for_llm_coding.xlsx) |
| `India_MIH_S2/MIH_S2_Virality Report.csv` | [`data/processed/india/MIH_S2_virality_report.csv`](processed/india/MIH_S2_virality_report.csv) |
| `India_MIH_S2/MIH_S2 YT Human Coding Dataset.xlsx` | [`data/human_coded/india/MIH_S2_human_coding_dataset.xlsx`](human_coded/india/MIH_S2_human_coding_dataset.xlsx) |
| `Kenya_RHONairobi/RHONairobi.csv` | [`data/raw/kenya/RHONairobi_tweets.csv`](raw/kenya/RHONairobi_tweets.csv) |
| `Kenya_RHONairobi/RHO Nairobi Tiktok.csv` | [`data/raw/kenya/RHONairobi_tiktok.csv`](raw/kenya/RHONairobi_tiktok.csv) |
| `Kenya_RHONairobi/RHONairobi_Final Topic Relevant.xlsx` | [`data/processed/kenya/RHONairobi_final_topic_relevant.xlsx`](processed/kenya/RHONairobi_final_topic_relevant.xlsx) |
| `Kenya_RHONairobi/RHONairobi for LLM Coding.xlsx` | [`data/processed/kenya/RHONairobi_for_llm_coding.xlsx`](processed/kenya/RHONairobi_for_llm_coding.xlsx) |
| `Kenya_RHONairobi/rhonairobi_videos virality.csv` | [`data/processed/kenya/RHONairobi_videos_virality.csv`](processed/kenya/RHONairobi_videos_virality.csv) |
| `Kenya_RHONairobi/RHONairobi Human Coding Dataset.csv` | [`data/human_coded/kenya/RHONairobi_human_coding_dataset.csv`](human_coded/kenya/RHONairobi_human_coding_dataset.csv) |
| `Nigeria_BBNaija/BBNaija.csv` | [`data/raw/nigeria/BBNaija_nairaland.csv`](raw/nigeria/BBNaija_nairaland.csv) |
| `Nigeria_BBNaija/BBNaija Sentiment & Emotions.csv` | [`data/processed/nigeria/BBNaija_sentiment_emotions.csv`](processed/nigeria/BBNaija_sentiment_emotions.csv) |
| `Nigeria_BBNaija/BBNaija_Final Topic Relevant.xlsx` | [`data/processed/nigeria/BBNaija_final_topic_relevant.xlsx`](processed/nigeria/BBNaija_final_topic_relevant.xlsx) |
| `Nigeria_BBNaija/BBNaija for LLM Coding.xlsx` | [`data/processed/nigeria/BBNaija_for_llm_coding.xlsx`](processed/nigeria/BBNaija_for_llm_coding.xlsx) |

## Files in this repo that are NOT in the gold release

These are working extensions produced after the pilot release — clearly
distinguishable from gold by descriptive filenames:

- [`data/raw/kenya/RHONairobi_yt_comments.xlsx`](raw/kenya/RHONairobi_yt_comments.xlsx) — 15,745 YouTube comments (extended scrape)
- [`data/raw/kenya/RHONairobi_apify_scraped.xlsx`](raw/kenya/RHONairobi_apify_scraped.xlsx) — 1,173-row Apify pull (extended)
- [`data/interim/india/MIH_S2_cleaned.xlsx`](interim/india/MIH_S2_cleaned.xlsx) — interim cleaning output
- [`data/interim/kenya/`](interim/kenya/) — five rerank-pipeline interim files
- [`data/processed/india/MIH_S2_final_dataset.xlsx`](processed/india/MIH_S2_final_dataset.xlsx) — LLM-coded extension
- [`data/processed/kenya/RHONairobi_relevant_comments.xlsx`](processed/kenya/RHONairobi_relevant_comments.xlsx)
- [`data/processed/kenya/RHONairobi_scored.xlsx`](processed/kenya/RHONairobi_scored.xlsx)
- [`data/human_coded/india/MIH_S2_human_coding_extended.xlsx`](human_coded/india/MIH_S2_human_coding_extended.xlsx) — 951 rows, codebook v1
- [`data/human_coded/nigeria/BBNaija_human_coding_dataset.xlsx`](human_coded/nigeria/BBNaija_human_coding_dataset.xlsx) — Nairaland coding (100 rows; not in pilot)
- [`data/processed/india/language_splits/`](processed/india/language_splits/) — language-split CSVs

## How to verify

```bash
python scripts/validate_data.py
```

Layer 3 reports md5 vs gold for all 16 mirror files. If the upstream gold
directory is moved or absent, Layer 3 reports `SKIP` rather than `FAIL` —
in-repo mirror files are still validated for shape and required columns.
