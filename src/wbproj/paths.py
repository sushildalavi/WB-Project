"""Single source of truth for every file path the project reads or writes.

All paths resolve relative to the repository root, so the package works
regardless of the current working directory.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"

# Pointer to the upstream published pilot dataset directory (NLC-Datasets).
# Existence is not required — the gold *files* are mirrored into this repo.
# This constant is informational, used by the validator's byte-identity layer.
GOLD_RELEASE = Path("/Users/sushildalavi/Desktop/NLC/NLC-Datasets-main")


class _Country:
    def __init__(self, name: str):
        self.name = name
        self.raw = DATA / "raw" / name
        self.interim = DATA / "interim" / name
        self.processed = DATA / "processed" / name
        self.human_coded = DATA / "human_coded" / name
        self.reach = DATA / "reach" / name


INDIA = _Country("india")
KENYA = _Country("kenya")
NIGERIA = _Country("nigeria")

# India ----------------------------------------------------------------------
INDIA.raw_full = INDIA.raw / "MIH_S2_full_data.xlsx"
INDIA.raw_videos = INDIA.raw / "MIH_S2_yt_videos_data.xlsx"
INDIA.cleaned = INDIA.interim / "MIH_S2_cleaned.xlsx"
INDIA.topic_relevant = INDIA.processed / "MIH_S2_final_topic_relevant.xlsx"
INDIA.for_llm_coding = INDIA.processed / "MIH_S2_for_llm_coding.xlsx"
INDIA.final_dataset = INDIA.processed / "MIH_S2_final_dataset.xlsx"
INDIA.virality = INDIA.reach / "MIH_S2_youtube_virality.csv"
INDIA.human_coding = INDIA.human_coded / "MIH_S2_human_coding_dataset.xlsx"        # 114 rows, codebook v2
INDIA.human_coding_extended = INDIA.human_coded / "MIH_S2_human_coding_extended.xlsx"  # 951 rows, codebook v1

# Kenya ----------------------------------------------------------------------
KENYA.raw_tweets = KENYA.raw / "RHONairobi_tweets.csv"
KENYA.raw_tiktok = KENYA.raw / "RHONairobi_tiktok.csv"
KENYA.raw_yt = KENYA.raw / "RHONairobi_yt_comments.xlsx"
KENYA.raw_apify = KENYA.raw / "RHONairobi_apify_scraped.xlsx"
KENYA.topic_relevant = KENYA.processed / "RHONairobi_final_topic_relevant.xlsx"
KENYA.for_llm_coding = KENYA.processed / "RHONairobi_for_llm_coding.xlsx"
KENYA.relevant_comments = KENYA.processed / "RHONairobi_relevant_comments.xlsx"
KENYA.scored = KENYA.processed / "RHONairobi_scored.xlsx"
KENYA.videos_virality = KENYA.reach / "RHONairobi_youtube_virality.csv"
KENYA.human_coding = KENYA.human_coded / "RHONairobi_human_coding_dataset.csv"

# Nigeria --------------------------------------------------------------------
NIGERIA.raw_nairaland = NIGERIA.raw / "BBNaija_nairaland.csv"
NIGERIA.sentiment_emotions = NIGERIA.processed / "BBNaija_sentiment_emotions.csv"
NIGERIA.topic_relevant = NIGERIA.processed / "BBNaija_final_topic_relevant.xlsx"
NIGERIA.for_llm_coding = NIGERIA.processed / "BBNaija_for_llm_coding.xlsx"
NIGERIA.human_coding = NIGERIA.human_coded / "BBNaija_human_coding_dataset.xlsx"
NIGERIA.tiktok = NIGERIA.raw / "BBNaija_tiktok.xlsx"  # optional; not in repo


# Files in this repo that are byte-identical to the upstream gold release.
# The validator (Layer 3) checks md5 against GOLD_RELEASE for each entry.
GOLD_MIRROR: dict[Path, Path] = {
    INDIA.raw_full:         GOLD_RELEASE / "India_MIH_S2/MIH_S2_FullData.xlsx",
    INDIA.raw_videos:       GOLD_RELEASE / "India_MIH_S2/MIH_S2_YTvidsdata.xlsx",
    INDIA.topic_relevant:   GOLD_RELEASE / "India_MIH_S2/MIH_S2_Final_Topic Relevant.xlsx",
    INDIA.for_llm_coding:   GOLD_RELEASE / "India_MIH_S2/MIH_S2 for LLM Coding.xlsx",
    INDIA.virality:         GOLD_RELEASE / "India_MIH_S2/MIH_S2_Virality Report.csv",  # now in data/reach/
    INDIA.human_coding:     GOLD_RELEASE / "India_MIH_S2/MIH_S2 YT Human Coding Dataset.xlsx",
    KENYA.raw_tweets:       GOLD_RELEASE / "Kenya_RHONairobi/RHONairobi.csv",
    KENYA.raw_tiktok:       GOLD_RELEASE / "Kenya_RHONairobi/RHO Nairobi Tiktok.csv",
    KENYA.topic_relevant:   GOLD_RELEASE / "Kenya_RHONairobi/RHONairobi_Final Topic Relevant.xlsx",
    KENYA.for_llm_coding:   GOLD_RELEASE / "Kenya_RHONairobi/RHONairobi for LLM Coding.xlsx",
    KENYA.videos_virality:  GOLD_RELEASE / "Kenya_RHONairobi/rhonairobi_videos virality.csv",
    KENYA.human_coding:     GOLD_RELEASE / "Kenya_RHONairobi/RHONairobi Human Coding Dataset.csv",
    NIGERIA.raw_nairaland:      GOLD_RELEASE / "Nigeria_BBNaija/BBNaija.csv",
    NIGERIA.sentiment_emotions: GOLD_RELEASE / "Nigeria_BBNaija/BBNaija Sentiment & Emotions.csv",
    NIGERIA.topic_relevant:     GOLD_RELEASE / "Nigeria_BBNaija/BBNaija_Final Topic Relevant.xlsx",
    NIGERIA.for_llm_coding:     GOLD_RELEASE / "Nigeria_BBNaija/BBNaija for LLM Coding.xlsx",
}
