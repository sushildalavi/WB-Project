"""Streamlit dashboard for the WB gender-norms project.

Run from the repo root:
    streamlit run src/app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Make `wbproj` importable when Streamlit launches this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from wbproj.clean import expand_themes_column  # noqa: E402
from wbproj.loaders import (  # noqa: E402
    load_bbnaija_human_coding,
    load_bbnaija_tiktok,
    load_mih_human_coding_extended,
    load_mih_virality,
)

TIKTOK_HASHTAG_COLS = ["Hashtag1", "Hashtag2", "Hashtag3"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _prepare_hashtags(data: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in TIKTOK_HASHTAG_COLS if c in data.columns]
    if not cols or "video_url" not in data.columns:
        return pd.DataFrame(columns=["video_url", "Hashtag"])
    return (
        data.melt(id_vars=["video_url"], value_vars=cols, value_name="Hashtag")
        .dropna(subset=["Hashtag"])
        .assign(Hashtag=lambda d: d["Hashtag"].astype(str).str.strip().str.lower())
    )


# ---------------------------------------------------------------------------
# Made in Heaven (India) dashboard
# ---------------------------------------------------------------------------
def render_mih_dashboard() -> None:
    df = load_mih_human_coding_extended()
    df_viral = load_mih_virality()

    st.title("🎬 Made in Heaven S2 — YouTube Insights")

    st.markdown("### 📈 Comment & Theme Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Unique Comments (labeled)", f"{df['comment_text'].nunique():,}")
    c2.metric("Total Theme Assignments", f"{len(df):,}")
    c3.metric("Unique Themes", f"{df['themes'].nunique():,}")
    c4.metric("Sentiment Categories", f"{df['sentiment'].nunique():,}")

    st.sidebar.header("⚙️ MIH Filters")
    sentiments = sorted(df["sentiment"].dropna().unique().tolist())
    themes = sorted(df["themes"].dropna().unique().tolist())
    sel_sent = st.sidebar.multiselect("Sentiment", sentiments, default=sentiments)
    sel_theme = st.sidebar.multiselect("Theme", themes, default=themes)
    f = df[df["sentiment"].isin(sel_sent) & df["themes"].isin(sel_theme)]

    tabs = st.tabs(
        [
            "📌 Theme Distribution",
            "😊 Sentiment Split",
            "🔥 Theme vs Sentiment",
            "📈 Trends",
            "🚀 Virality",
            "📂 Raw",
        ]
    )

    with tabs[0]:
        counts = f["themes"].value_counts().reset_index()
        counts.columns = ["Theme", "Count"]
        fig = px.bar(
            counts.sort_values("Count"),
            x="Count",
            y="Theme",
            orientation="h",
            color="Count",
            color_continuous_scale="Viridis",
        )
        fig.update_layout(template="simple_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(counts, use_container_width=True)

    with tabs[1]:
        counts = f["sentiment"].value_counts().reset_index()
        counts.columns = ["Sentiment", "Count"]
        fig = px.pie(counts, values="Count", names="Sentiment", hole=0.4)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(counts, use_container_width=True)

    with tabs[2]:
        pivot = f.pivot_table(index="themes", columns="sentiment", aggfunc="size", fill_value=0).reset_index()
        long = pivot.melt(id_vars="themes", var_name="Sentiment", value_name="Count")
        fig = px.density_heatmap(
            long, x="Sentiment", y="themes", z="Count", color_continuous_scale="YlGnBu"
        )
        fig.update_traces(texttemplate="%{z}", textfont={"size": 11})
        fig.update_layout(template="simple_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(pivot.set_index("themes"), use_container_width=True)

    with tabs[3]:
        if "date" in df_viral.columns and df_viral["date"].notna().any():
            daily = (
                df_viral.groupby(pd.Grouper(key="date", freq="D"))[
                    ["viewCount", "likes", "ViralityScore"]
                ]
                .agg({"viewCount": "sum", "likes": "sum", "ViralityScore": "mean"})
                .reset_index()
            )
            fig = px.line(
                daily,
                x="date",
                y=["viewCount", "likes", "ViralityScore"],
                markers=True,
            )
            fig.update_layout(template="simple_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No date information in the virality file.")

    with tabs[4]:
        needed = {"viewCount", "likes", "ViralityScore"}
        if not needed.issubset(df_viral.columns):
            st.warning("Virality report missing expected metrics.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric(
                "Avg ReachFactor",
                f"{df_viral['ReachFactor'].mean():.2f}" if "ReachFactor" in df_viral else "N/A",
            )
            c2.metric(
                "Avg Engagement Efficiency",
                f"{df_viral['EngagementEfficiency'].mean():.2f}"
                if "EngagementEfficiency" in df_viral
                else "N/A",
            )
            c3.metric("Top Virality Score", f"{df_viral['ViralityScore'].max():.2f}")
            fig = px.scatter(
                df_viral,
                x="viewCount",
                y="ViralityScore",
                size="likes",
                hover_data=[c for c in ["title"] if c in df_viral.columns],
                color="ViralityScore",
                color_continuous_scale="Turbo",
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            cols = [c for c in ["title", "viewCount", "likes", "ViralityScore"] if c in df_viral.columns]
            st.dataframe(
                df_viral.sort_values("ViralityScore", ascending=False)[cols].head(10),
                use_container_width=True,
            )

    with tabs[5]:
        cols = [c for c in ["comment_text", "themes", "sentiment"] if c in f.columns]
        st.dataframe(f[cols].head(200) if cols else f.head(200), use_container_width=True)
        st.download_button(
            "📥 Download filtered",
            data=f.drop_duplicates().to_csv(index=False).encode("utf-8"),
            file_name="MIH_S2_filtered.csv",
            mime="text/csv",
        )


# ---------------------------------------------------------------------------
# BBNaija (Nigeria) dashboard — Nairaland human coding + optional TikTok
# ---------------------------------------------------------------------------
def render_bbnaija_dashboard() -> None:
    df_metrics = load_bbnaija_tiktok()
    df_human = load_bbnaija_human_coding()
    df_human_exp = expand_themes_column(df_human, col="themes")

    st.title("📱 BBNaija — Nairaland Coding & TikTok Engagement")

    st.markdown("### 🧩 Human Coding Overview (Nairaland)")
    if df_human.empty:
        st.info("No human-coded data available.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Labeled Comments", f"{df_human['comment_text'].nunique():,}")
        c2.metric("Total Theme Assignments", f"{len(df_human_exp):,}")
        c3.metric("Unique Themes", f"{df_human_exp['themes'].nunique():,}")
        c4.metric("Sentiment Categories", f"{df_human['sentiment'].nunique():,}")

    if df_metrics.empty:
        st.info(
            "TikTok metrics file not found at "
            "`data/raw/nigeria/BBNaija_tiktok.xlsx`. Drop a file there to enable "
            "the TikTok tabs. Showing Nairaland coding only."
        )
        st.subheader("🔥 Theme vs Sentiment Heatmap (Nairaland)")
        pivot = df_human_exp.pivot_table(
            index="themes", columns="sentiment", aggfunc="size", fill_value=0
        ).reset_index()
        long = pivot.melt(id_vars="themes", var_name="Sentiment", value_name="Count")
        fig = px.density_heatmap(
            long, x="Sentiment", y="themes", z="Count", color_continuous_scale="YlGnBu"
        )
        fig.update_traces(texttemplate="%{z}", textfont={"size": 11})
        fig.update_layout(template="simple_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(pivot.set_index("themes"), use_container_width=True)
        return

    # --- TikTok branch (only reached if metrics file is present) ---
    st.sidebar.header("🔎 TikTok Filters")
    f = df_metrics.copy()
    if "created_at" in f.columns:
        valid = f["created_at"].dropna()
        if not valid.empty:
            r = st.sidebar.date_input("Date range", [valid.min(), valid.max()])
            if len(r) == 2:
                lo, hi = pd.to_datetime(r[0]), pd.to_datetime(r[1])
                f = f[(f["created_at"] >= lo) & (f["created_at"] <= hi)]
    if "Author Username" in f.columns:
        creators = f["Author Username"].dropna().unique().tolist()
        if creators:
            sel = st.sidebar.multiselect("Creator", creators, default=creators)
            f = f[f["Author Username"].isin(sel)]

    st.markdown("### 📈 TikTok Engagement Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Views", f"{f.get('views', pd.Series(dtype=float)).sum():,.0f}")
    c2.metric("Total Likes", f"{f.get('likes', pd.Series(dtype=float)).sum():,.0f}")
    c3.metric("Total Comments", f"{f.get('comments', pd.Series(dtype=float)).sum():,.0f}")
    c4.metric("Total Shares", f"{f.get('shares', pd.Series(dtype=float)).sum():,.0f}")

    tab_h, tab_trend, tab_top, tab_hash, tab_mix, tab_vir, tab_vel, tab_raw = st.tabs(
        [
            "🧩 Themes (Nairaland)",
            "📅 Trends",
            "🔥 Top Videos",
            "💬 Hashtags",
            "🎨 Engagement Mix",
            "🚀 Virality",
            "⚡ Velocity",
            "📂 Raw",
        ]
    )

    with tab_h:
        pivot = df_human_exp.pivot_table(
            index="themes", columns="sentiment", aggfunc="size", fill_value=0
        ).reset_index()
        long = pivot.melt(id_vars="themes", var_name="Sentiment", value_name="Count")
        fig = px.density_heatmap(
            long, x="Sentiment", y="themes", z="Count", color_continuous_scale="YlGnBu"
        )
        fig.update_traces(texttemplate="%{z}", textfont={"size": 11})
        fig.update_layout(template="simple_white")
        st.plotly_chart(fig, use_container_width=True)

    with tab_trend:
        if "created_at" in f.columns:
            trend = (
                f.groupby(pd.Grouper(key="created_at", freq="D"))[
                    ["views", "likes", "comments", "shares"]
                ]
                .sum()
                .reset_index()
            )
            fig = px.line(
                trend,
                x="created_at",
                y=["views", "likes", "comments", "shares"],
                markers=True,
            )
            fig.update_layout(template="simple_white")
            st.plotly_chart(fig, use_container_width=True)

    with tab_top:
        if "engagement_rate" in f.columns:
            top = f.sort_values("engagement_rate", ascending=False).head(10)
            y = "video_url" if "video_url" in top.columns else top.index.astype(str)
            fig = px.bar(
                top,
                x="engagement_rate",
                y=y,
                orientation="h",
                color="engagement_rate",
                color_continuous_scale="Viridis",
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    with tab_hash:
        h = _prepare_hashtags(f)
        if h.empty:
            st.warning("No hashtag data.")
        else:
            top = h["Hashtag"].value_counts().reset_index().head(10)
            top.columns = ["Hashtag", "Count"]
            fig = px.bar(top, x="Count", y="Hashtag", orientation="h", color="Count")
            st.plotly_chart(fig, use_container_width=True)

    with tab_mix:
        totals = pd.DataFrame(
            {
                "Type": ["Likes", "Comments", "Shares"],
                "Count": [
                    f.get("likes", pd.Series(dtype=float)).sum(),
                    f.get("comments", pd.Series(dtype=float)).sum(),
                    f.get("shares", pd.Series(dtype=float)).sum(),
                ],
            }
        )
        fig = px.bar(totals, x="Type", y="Count", color="Type")
        fig.update_layout(template="simple_white")
        st.plotly_chart(fig, use_container_width=True)

    with tab_vir:
        if {"views", "engagement_rate"}.issubset(f.columns):
            fig = px.scatter(
                f,
                x="views",
                y="engagement_rate",
                size="shares" if "shares" in f.columns else None,
                color="likes" if "likes" in f.columns else None,
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    with tab_vel:
        if "velocity" in f.columns:
            fig = px.histogram(f, x="velocity", nbins=30)
            fig.update_layout(template="simple_white")
            st.plotly_chart(fig, use_container_width=True)

    with tab_raw:
        st.dataframe(f.head(200), use_container_width=True)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
def main() -> None:
    st.set_page_config(page_title="WB Gender-Norms Dashboard", layout="wide", page_icon="🎬")
    with st.sidebar:
        choice = st.radio(
            "Dashboard",
            ["MIH S2 (India)", "BBNaija (Nigeria)"],
            index=0,
        )
    if choice.startswith("MIH"):
        render_mih_dashboard()
    else:
        render_bbnaija_dashboard()


if __name__ == "__main__":
    main()
