"""
dashboard.py
------------
Page 1 — Campaign Dashboard

Shows the aggregate state of all active campaigns:
  • Four KPI metric cards (Spend, Conversions, Avg CPA, Avg CTR)
  • Spend vs Conversions grouped bar chart
  • CPA by Segment horizontal bar chart  (colour-coded by performance)
  • 30-day trend line chart
  • Workshop callout explaining what the agent is monitoring
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from utils.styling import (
    page_header,
    workshop_callout,
    section_label,
    PLOTLY_LAYOUT,
    CHART_COLORS,
    SERIES_PALETTE,
    performance_color,
    tier_badge,
)
from data.campaign_data import get_daily_trend_data


def render_dashboard(df: pd.DataFrame) -> None:
    """Render the full Campaign Dashboard page."""

    # ── Page header ────────────────────────────────────────────────────────
    page_header(
        eyebrow="Live Intelligence · All Campaigns",
        title="Campaign Dashboard",
        subtitle="Real-time performance monitoring across all active audience segments and platforms.",
    )

    workshop_callout(
        "The AI agent continuously polls your ad platform APIs and evaluates each segment "
        "against performance thresholds. This dashboard is the agent's live view of the "
        "entire campaign portfolio — the data it uses to decide <em>where</em> to intervene "
        "and <em>how urgently</em>."
    )

    # ── KPI metrics ────────────────────────────────────────────────────────
    section_label("Portfolio Overview")

    total_spend       = df["spend"].sum()
    total_conversions = df["conversions"].sum()
    avg_cpa           = total_spend / total_conversions
    avg_ctr           = df["ctr"].mean()
    underperformer_ct = int(df["is_underperformer"].sum())

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Total Spend",     f"${total_spend:,.0f}",      delta="+3.2% MoM")
    with c2:
        st.metric("Total Conversions", f"{total_conversions:,}",  delta="+8.7% MoM")
    with c3:
        st.metric("Avg CPA",         f"${avg_cpa:.2f}",           delta="-$4.12",  delta_color="inverse")
    with c4:
        st.metric("Avg CTR",         f"{avg_ctr:.2f}%",           delta="+0.18pp")
    with c5:
        st.metric("Underperformers", f"{underperformer_ct} / {len(df)}",
                  delta=f"{underperformer_ct} need attention", delta_color="off")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart row 1: Spend vs Conversions + CPA by Segment ─────────────────
    section_label("Spend & Conversion Performance by Segment")
    chart_l, chart_r = st.columns(2)

    with chart_l:
        # Grouped bar: spend (left Y) + conversions line (right Y)
        df_sorted = df.sort_values("spend", ascending=False)
        bar_colors = [performance_color(t) for t in df_sorted["performance_tier"]]

        fig_sv = go.Figure()
        fig_sv.add_trace(go.Bar(
            name="Spend ($)",
            x=df_sorted["segment"],
            y=df_sorted["spend"],
            marker_color=bar_colors,
            marker_opacity=0.85,
            yaxis="y",
            hovertemplate="<b>%{x}</b><br>Spend: $%{y:,.0f}<extra></extra>",
        ))
        fig_sv.add_trace(go.Scatter(
            name="Conversions",
            x=df_sorted["segment"],
            y=df_sorted["conversions"],
            mode="lines+markers",
            line=dict(color=CHART_COLORS["teal"], width=2),
            marker=dict(size=6, color=CHART_COLORS["teal"]),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Conversions: %{y}<extra></extra>",
        ))
        fig_sv.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Spend vs Conversions", font=dict(size=13, color="#8A96B8"), x=0),
            xaxis=dict(tickangle=-40, tickfont=dict(size=9)),
            yaxis=dict(title="Spend ($)", title_font=dict(size=10, color="#5A6482"),
                       tickprefix="$", **PLOTLY_LAYOUT["yaxis"]),
            yaxis2=dict(title="Conversions", title_font=dict(size=10, color=CHART_COLORS["teal"]),
                        overlaying="y", side="right",
                        gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10, color=CHART_COLORS["teal"])),
            legend=dict(orientation="h", y=1.08, x=0, **{k: v for k, v in PLOTLY_LAYOUT["legend"].items() if k != "orientation"}),
            height=370,
            barmode="group",
        )
        st.plotly_chart(fig_sv, use_container_width=True)

    with chart_r:
        # Horizontal bar chart of CPA by segment, coloured by tier
        df_cpa = df.sort_values("cpa", ascending=True)
        cpa_colors = [performance_color(t) for t in df_cpa["performance_tier"]]

        fig_cpa = go.Figure()
        fig_cpa.add_trace(go.Bar(
            orientation="h",
            x=df_cpa["cpa"],
            y=df_cpa["segment"],
            marker_color=cpa_colors,
            marker_opacity=0.85,
            hovertemplate="<b>%{y}</b><br>CPA: $%{x:.2f}<extra></extra>",
        ))
        # Threshold reference line at $50
        fig_cpa.add_vline(
            x=50,
            line_dash="dash",
            line_color="rgba(244,172,50,0.5)",
            annotation_text="$50 threshold",
            annotation_font=dict(size=9, color="#F4AC32"),
            annotation_position="top right",
        )
        fig_cpa.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Cost-per-Acquisition by Segment", font=dict(size=13, color="#8A96B8"), x=0),
            xaxis=dict(tickprefix="$", title="CPA ($)", title_font=dict(size=10, color="#5A6482"),
                       **PLOTLY_LAYOUT["xaxis"]),
            yaxis=dict(tickfont=dict(size=9), **{k: v for k, v in PLOTLY_LAYOUT["yaxis"].items()}),
            showlegend=False,
            height=370,
        )
        st.plotly_chart(fig_cpa, use_container_width=True)

    # ── Chart row 2: 30-day trend ───────────────────────────────────────────
    section_label("30-Day Performance Trend")
    trend_df = get_daily_trend_data()

    fig_trend = go.Figure()
    # Spend area
    fig_trend.add_trace(go.Scatter(
        name="Daily Spend ($)",
        x=trend_df["date"], y=trend_df["spend"],
        mode="lines",
        line=dict(color=CHART_COLORS["primary"], width=2),
        fill="tozeroy",
        fillcolor="rgba(91,110,245,0.08)",
        hovertemplate="<b>%{x}</b><br>Spend: $%{y:,.0f}<extra></extra>",
    ))
    # Conversions line
    fig_trend.add_trace(go.Scatter(
        name="Conversions",
        x=trend_df["date"], y=trend_df["conversions"],
        mode="lines+markers",
        line=dict(color=CHART_COLORS["teal"], width=2, dash="dot"),
        marker=dict(size=4, color=CHART_COLORS["teal"]),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Conversions: %{y}<extra></extra>",
    ))
    fig_trend.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Daily Spend & Conversions — Last 30 Days",
                   font=dict(size=13, color="#8A96B8"), x=0),
        yaxis=dict(title="Spend ($)", title_font=dict(size=10, color="#5A6482"),
                   tickprefix="$", **PLOTLY_LAYOUT["yaxis"]),
        yaxis2=dict(title="Conversions", title_font=dict(size=10, color=CHART_COLORS["teal"]),
                    overlaying="y", side="right",
                    gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10, color=CHART_COLORS["teal"])),
        legend=dict(orientation="h", y=1.06, x=0,
                    **{k: v for k, v in PLOTLY_LAYOUT["legend"].items() if k != "orientation"}),
        height=300,
        margin=dict(l=10, r=10, t=42, b=10),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── Segment table ────────────────────────────────────────────────────────
    with st.expander("📋  Full Segment Data Table", expanded=False):
        display_df = df[[
            "segment", "platform", "spend", "impressions", "clicks",
            "conversions", "ctr", "cpa", "roas", "performance_tier"
        ]].copy()
        display_df.columns = [
            "Segment", "Platform", "Spend ($)", "Impressions", "Clicks",
            "Conversions", "CTR (%)", "CPA ($)", "ROAS", "Tier"
        ]
        st.dataframe(
            display_df.style
                .format({
                    "Spend ($)": "${:,.0f}",
                    "Impressions": "{:,.0f}",
                    "Clicks": "{:,.0f}",
                    "CPA ($)": "${:.2f}",
                    "CTR (%)": "{:.2f}%",
                    "ROAS": "{:.2f}x",
                })
                .applymap(
                    lambda v: "color: #F05252" if v == "Critical"
                    else ("color: #F4AC32" if v == "Underperforming"
                    else ("color: #1FCEAB" if v == "Excellent" else "color: #2ECC8F")),
                    subset=["Tier"],
                ),
            use_container_width=True,
            hide_index=True,
        )
