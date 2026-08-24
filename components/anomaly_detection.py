"""
anomaly_detection.py
--------------------
Page 2 — Anomaly Detection: Identifying Underperformers

The agent evaluates every segment against two thresholds:
  • CPA > $50   → acquisition cost too high
  • CTR < 0.5%  → creative is failing to capture attention

Underperforming segments surface in:
  1. A quadrant scatter plot (CTR vs CPA) with threshold lines marked
  2. Worst-offender highlight cards
  3. A full styled dataframe
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.styling import (
    page_header,
    workshop_callout,
    section_label,
    tier_badge,
    PLOTLY_LAYOUT,
    CHART_COLORS,
    performance_color,
)


def render_anomaly_detection(df: pd.DataFrame) -> None:
    """Render the Anomaly Detection page."""

    # ── Page header ────────────────────────────────────────────────────────
    page_header(
        eyebrow="Agent Module 01 · Anomaly Detection",
        title="Identifying Underperformers",
        subtitle="The agent scans all segments against performance benchmarks and surfaces those that need immediate action.",
    )

    workshop_callout(
        "This is the agent's <strong>diagnostic loop</strong>. Every 15 minutes it re-evaluates "
        "the full segment portfolio. Segments crossing either threshold — CPA above $50 "
        "or CTR below 0.5% — are flagged and queued for the Creative Optimization module. "
        "Think of this as the agent's early-warning system."
    )

    underperformers = df[df["is_underperformer"]].sort_values("cpa", ascending=False)
    good_performers = df[~df["is_underperformer"]]
    count_under = len(underperformers)

    # ── Alert banner ───────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="alert-banner">
          <span class="alert-icon">🚨</span>
          <span class="alert-text">
            Agent Alert — {count_under} Underperforming Segments Detected
            &nbsp;|&nbsp; ${underperformers["spend"].sum():,.0f} at risk of wasted spend
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Worst offender cards ────────────────────────────────────────────────
    section_label("Worst Offenders by CPA")

    top_bad = underperformers.head(4).reset_index(drop=True)
    cols = st.columns(len(top_bad))

    for i, (_, row) in enumerate(top_bad.iterrows()):
        is_critical = row["performance_tier"] == "Critical"
        css_extra   = "" if is_critical else " warn"
        with cols[i]:
            st.markdown(
                f"""
                <div class="offender-card{css_extra}">
                  <div class="offender-label">CPA</div>
                  <div class="offender-value">${row['cpa']:,.0f}</div>
                  <div class="offender-name">{row['segment']}</div>
                  <div class="offender-platform">▸ {row['platform']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Scatter: CTR vs CPA quadrant plot ──────────────────────────────────
    section_label("Performance Quadrant — CTR vs CPA")

    fig = go.Figure()

    # Shade the "danger zone" (CPA > 50 OR CTR < 0.5)
    fig.add_shape(type="rect", x0=0, x1=0.5, y0=50, y1=df["cpa"].max() * 1.15,
                  fillcolor="rgba(240,82,82,0.05)", line_width=0)
    fig.add_shape(type="rect", x0=0.5, x1=df["ctr"].max() * 1.1, y0=50,
                  y1=df["cpa"].max() * 1.15,
                  fillcolor="rgba(240,82,82,0.05)", line_width=0)
    fig.add_shape(type="rect", x0=0, x1=0.5, y0=0, y1=50,
                  fillcolor="rgba(240,82,82,0.05)", line_width=0)

    # Threshold lines
    fig.add_hline(y=50, line_dash="dash", line_color="rgba(244,172,50,0.5)",
                  annotation_text="CPA $50 limit", annotation_font=dict(size=9, color="#F4AC32"),
                  annotation_position="right")
    fig.add_vline(x=0.5, line_dash="dash", line_color="rgba(244,172,50,0.5)",
                  annotation_text="CTR 0.5% floor", annotation_font=dict(size=9, color="#F4AC32"),
                  annotation_position="top")

    # Plot good performers
    fig.add_trace(go.Scatter(
        name="Good / Excellent",
        x=good_performers["ctr"],
        y=good_performers["cpa"],
        mode="markers+text",
        marker=dict(
            size=good_performers["spend"] / 500,
            color=CHART_COLORS["teal"],
            opacity=0.75,
            line=dict(width=1, color="rgba(255,255,255,0.15)"),
        ),
        text=good_performers["segment"],
        textposition="top center",
        textfont=dict(size=8, color="#5A6482"),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "CTR: %{x:.2f}%<br>"
            "CPA: $%{y:.2f}<br>"
            "<extra></extra>"
        ),
    ))

    # Plot underperformers
    fig.add_trace(go.Scatter(
        name="Underperforming / Critical",
        x=underperformers["ctr"],
        y=underperformers["cpa"],
        mode="markers+text",
        marker=dict(
            size=underperformers["spend"] / 500,
            color=CHART_COLORS["critical"],
            opacity=0.8,
            symbol="circle",
            line=dict(width=1.5, color="rgba(240,82,82,0.6)"),
        ),
        text=underperformers["segment"],
        textposition="top center",
        textfont=dict(size=8, color="#F05252"),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "CTR: %{x:.2f}%<br>"
            "CPA: $%{y:.2f}<br>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text="CTR vs CPA — bubble size = spend   •   red zone = underperforming",
            font=dict(size=12, color="#5A6482"), x=0,
        ),
        xaxis=dict(title="Click-Through Rate (%)", title_font=dict(size=10, color="#5A6482"),
                   ticksuffix="%", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(title="Cost per Acquisition ($)", title_font=dict(size=10, color="#5A6482"),
                   tickprefix="$", **PLOTLY_LAYOUT["yaxis"]),
        legend=dict(orientation="h", y=1.06, x=0,
                    **{k: v for k, v in PLOTLY_LAYOUT["legend"].items() if k != "orientation"}),
        height=430,
        margin=dict(l=10, r=10, t=48, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Full segment table ─────────────────────────────────────────────────
    section_label("All Segments — Agent Diagnostic Report")

    # Build display table
    display_df = df[[
        "segment", "platform", "spend", "conversions",
        "ctr", "cpa", "roas", "performance_tier",
    ]].copy()
    display_df.columns = ["Segment", "Platform", "Spend", "Conversions", "CTR %", "CPA $", "ROAS", "Status"]

    def _row_style(row):
        """Apply row-level background tint to underperforming rows."""
        if row["Status"] == "Critical":
            return ["background-color: rgba(240,82,82,0.06)"] * len(row)
        if row["Status"] == "Underperforming":
            return ["background-color: rgba(244,172,50,0.05)"] * len(row)
        return [""] * len(row)

    def _status_style(val):
        return {
            "Critical":       "color: #F05252; font-weight: 600",
            "Underperforming":"color: #F4AC32; font-weight: 600",
            "Good":           "color: #2ECC8F",
            "Excellent":      "color: #1FCEAB; font-weight: 600",
        }.get(val, "")

    styled = (
        display_df
        .sort_values("CPA $", ascending=False)
        .style
        .apply(_row_style, axis=1)
        .applymap(_status_style, subset=["Status"])
        .format({
            "Spend":  "${:,.0f}",
            "CPA $":  "${:.2f}",
            "CTR %":  "{:.2f}%",
            "ROAS":   "{:.2f}×",
        })
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # ── Workshop expand — how thresholds work ─────────────────────────────
    with st.expander("📖  How the Agent Sets Thresholds"):
        st.markdown("""
**CPA Threshold — $50**

The agent calculates the industry-benchmark CPA for this vertical and flags any segment
spending more than 2× the median. In this campaign, the portfolio median CPA is **$38.40**;
the $50 ceiling allows a 30 % buffer before hard-flagging.

**CTR Threshold — 0.5%**

A CTR below 0.5% signals that the creative itself is failing to earn attention —
the audience is seeing the ad but choosing not to engage. This is a creative problem,
not a targeting problem, which is why low-CTR segments are routed directly to the
**Creative Optimization Agent** module.

**Why both thresholds?**

A segment can have a decent CTR but a catastrophically high CPA (poor landing-page
conversion), or a terrible CTR but acceptable CPA because the segment is small.
The agent evaluates both independently and routes the segment to the appropriate
remediation workflow.
        """)
