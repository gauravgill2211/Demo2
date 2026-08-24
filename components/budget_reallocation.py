"""
budget_reallocation.py
-----------------------
Page 4 — Budget Reallocation Engine

Agent logic:
  • Identify the 4 underperforming segments
  • Cut 20% of each underperformer's budget
  • Distribute freed budget to the top 3 performing segments
    (weighted by their current conversion volume)
  • Project the net conversion impact at each segment's current CPA

Displays:
  • Side-by-side donut charts (Current vs Recommended allocation)
  • Detailed reallocation table with delta markers
  • Projected impact strip (net conversion gain, ROAS lift, waste saved)
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from utils.styling import (
    page_header,
    workshop_callout,
    section_label,
    PLOTLY_LAYOUT,
    CHART_COLORS,
    SERIES_PALETTE,
)


# ---------------------------------------------------------------------------
# Reallocation logic
# ---------------------------------------------------------------------------

CUT_FRACTION     = 0.20   # 20 % cut from each underperformer
TOP_N_RECIPIENTS = 3      # distribute to the top 3 performers


def _compute_reallocation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of df with two extra columns:
        new_spend       — recommended budget after reallocation
        spend_delta     — difference (positive = gained, negative = cut)
    """
    df = df.copy()
    df["new_spend"] = df["spend"].copy().astype(float)

    under_mask = df["is_underperformer"]
    good_mask  = ~under_mask

    # Amount freed from underperformers
    freed = (df.loc[under_mask, "spend"] * CUT_FRACTION).sum()

    # Cut underperformers
    df.loc[under_mask, "new_spend"] *= (1 - CUT_FRACTION)

    # Choose top N recipients by conversion volume
    top_idx = (
        df.loc[good_mask]
        .nlargest(TOP_N_RECIPIENTS, "conversions")
        .index
    )

    # Distribute freed budget weighted by their conversion count
    total_convs = df.loc[top_idx, "conversions"].sum()
    for idx in top_idx:
        share = df.at[idx, "conversions"] / total_convs
        df.at[idx, "new_spend"] += freed * share

    df["spend_delta"] = df["new_spend"] - df["spend"]
    return df


def _project_conversions(df_realloc: pd.DataFrame) -> dict:
    """
    Project the net conversion change resulting from the reallocation,
    assuming each segment maintains its current CPA rate.
    """
    # Conversions gained by top performers
    gain_rows = df_realloc[df_realloc["spend_delta"] > 0]
    gained    = (gain_rows["spend_delta"] / gain_rows["cpa"]).sum()

    # Conversions lost from underperformers (minimal because CPA is awful)
    lost_rows = df_realloc[df_realloc["spend_delta"] < 0]
    lost      = (lost_rows["spend_delta"].abs() / lost_rows["cpa"]).sum()

    net_gain      = gained - lost
    total_current = df_realloc["conversions"].sum()
    waste_saved   = df_realloc.loc[df_realloc["is_underperformer"], "spend_delta"].abs().sum() * CUT_FRACTION * 5  # rough waste proxy

    current_roas  = (total_current * 52) / df_realloc["spend"].sum()
    new_roas      = ((total_current + net_gain) * 52) / df_realloc["new_spend"].sum()

    return {
        "net_gain":      net_gain,
        "pct_lift":      (net_gain / total_current) * 100,
        "current_roas":  current_roas,
        "new_roas":      new_roas,
        "roas_lift":     new_roas - current_roas,
        "freed_budget":  df_realloc.loc[df_realloc["is_underperformer"], "spend"].sum() * CUT_FRACTION,
    }


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------

def _donut_chart(labels: list, values: list, title: str, highlight_color: str) -> go.Figure:
    """Create a consistent donut chart."""
    colors = [highlight_color if i < 3 else CHART_COLORS["muted"] for i in range(len(labels))]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.60,
        marker=dict(colors=SERIES_PALETTE[:len(labels)], line=dict(color="#070D1A", width=2)),
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
        sort=False,
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=title, font=dict(size=13, color="#8A96B8"), x=0.5, xanchor="center"),
        showlegend=True,
        legend=dict(
            orientation="v", x=1.02, y=0.5,
            font=dict(size=9, color="#8A96B8"),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=320,
        margin=dict(l=0, r=120, t=42, b=0),
    )
    return fig


# ---------------------------------------------------------------------------
# Page renderer
# ---------------------------------------------------------------------------

def render_budget_reallocation(df: pd.DataFrame) -> None:
    """Render the Budget Reallocation Engine page."""

    page_header(
        eyebrow="Agent Module 03 · Budget Reallocation",
        title="Budget Reallocation Engine",
        subtitle="The agent reallocates 20% of underperformer budgets to the top 3 performing segments and projects the net impact.",
    )

    workshop_callout(
        "The reallocation agent runs a <strong>constrained optimisation</strong>: "
        "given a fixed total budget, it solves for the allocation that maximises "
        "total conversions. In this simplified model it uses each segment's current "
        "CPA as a proxy for marginal return — but in production it fits a "
        "diminishing-returns curve per segment to avoid over-saturating top performers."
    )

    df_r = _compute_reallocation(df)
    proj = _project_conversions(df_r)

    # ── Projected impact strip ──────────────────────────────────────────────
    section_label("Projected 30-Day Impact")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            f"""
            <div class="impact-strip">
              <div class="impact-number">+{proj['net_gain']:.0f}</div>
              <div class="impact-label">Net Additional Conversions</div>
            </div>
            """, unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"""
            <div class="impact-strip">
              <div class="impact-number">+{proj['pct_lift']:.1f}%</div>
              <div class="impact-label">Conversion Volume Lift</div>
            </div>
            """, unsafe_allow_html=True,
        )
    with col_c:
        st.markdown(
            f"""
            <div class="impact-strip">
              <div class="impact-number">${proj['freed_budget']:,.0f}</div>
              <div class="impact-label">Freed from Inefficient Spend</div>
            </div>
            """, unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Side-by-side donuts ─────────────────────────────────────────────────
    section_label("Budget Allocation — Current vs Recommended")

    d_left, d_right = st.columns(2)

    segs   = df_r["segment"].tolist()
    cur_spend  = df_r["spend"].tolist()
    new_spend  = df_r["new_spend"].round(0).tolist()

    with d_left:
        fig_cur = _donut_chart(segs, cur_spend, "Current Allocation", CHART_COLORS["muted"])
        # Add centre annotation
        fig_cur.add_annotation(
            text=f"<b>${sum(cur_spend):,.0f}</b><br><span style='font-size:10px;color:#5A6482'>total spend</span>",
            x=0.38, y=0.5, xref="paper", yref="paper",
            showarrow=False, font=dict(size=12, color="#C8D0E7"),
            align="center",
        )
        st.plotly_chart(fig_cur, use_container_width=True)

    with d_right:
        fig_new = _donut_chart(segs, new_spend, "Recommended Allocation", CHART_COLORS["teal"])
        fig_new.add_annotation(
            text=f"<b>${sum(new_spend):,.0f}</b><br><span style='font-size:10px;color:#5A6482'>total spend</span>",
            x=0.38, y=0.5, xref="paper", yref="paper",
            showarrow=False, font=dict(size=12, color="#C8D0E7"),
            align="center",
        )
        st.plotly_chart(fig_new, use_container_width=True)

    # ── Bar chart: spend delta by segment ───────────────────────────────────
    section_label("Spend Change by Segment")

    df_plot = df_r.sort_values("spend_delta")
    bar_colors = [
        CHART_COLORS["teal"] if v > 0 else CHART_COLORS["critical"]
        for v in df_plot["spend_delta"]
    ]

    fig_delta = go.Figure(go.Bar(
        orientation="h",
        x=df_plot["spend_delta"].round(0),
        y=df_plot["segment"],
        marker_color=bar_colors,
        marker_opacity=0.85,
        hovertemplate="<b>%{y}</b><br>Budget change: $%{x:+,.0f}<extra></extra>",
    ))
    fig_delta.add_vline(x=0, line_color="rgba(255,255,255,0.1)", line_width=1)
    fig_delta.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text="Budget Δ per Segment (green = gained, red = reduced)",
                   font=dict(size=12, color="#5A6482"), x=0),
        xaxis=dict(title="Spend Change ($)", title_font=dict(size=10),
                   tickprefix="$", **PLOTLY_LAYOUT["xaxis"]),
        yaxis=dict(tickfont=dict(size=9), **{k: v for k, v in PLOTLY_LAYOUT["yaxis"].items()}),
        showlegend=False,
        height=380,
    )
    st.plotly_chart(fig_delta, use_container_width=True)

    # ── Detailed reallocation table ─────────────────────────────────────────
    section_label("Segment-Level Reallocation Detail")

    # Header
    st.markdown(
        """
        <div class="realloc-row" style="border-bottom:2px solid #1E2D4A; margin-bottom:0.25rem;">
          <div class="realloc-segment" style="color:#5A6482; font-size:0.72rem;
               letter-spacing:0.08em; text-transform:uppercase; font-family:'JetBrains Mono',monospace;">
            Segment
          </div>
          <div class="realloc-num" style="color:#5A6482; font-size:0.72rem;
               letter-spacing:0.08em; text-transform:uppercase; font-family:'JetBrains Mono',monospace;">
            Current
          </div>
          <div class="realloc-num" style="color:#5A6482; font-size:0.72rem;
               letter-spacing:0.08em; text-transform:uppercase; font-family:'JetBrains Mono',monospace;">
            Recommended
          </div>
          <div class="realloc-delta" style="color:#5A6482; font-size:0.72rem;
               letter-spacing:0.08em; text-transform:uppercase; font-family:'JetBrains Mono',monospace;">
            Delta
          </div>
          <div class="realloc-delta" style="color:#5A6482; font-size:0.72rem;
               letter-spacing:0.08em; text-transform:uppercase; font-family:'JetBrains Mono',monospace;">
            Est. Conv Δ
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Rows — underperformers first (cuts), then gainers
    df_table = pd.concat([
        df_r[df_r["spend_delta"] < 0].sort_values("spend_delta"),
        df_r[df_r["spend_delta"] >= 0].sort_values("spend_delta", ascending=False),
    ])

    for _, row in df_table.iterrows():
        delta  = row["spend_delta"]
        est_cv = delta / row["cpa"]  # estimated conversion change
        d_class = "delta-pos" if delta > 0 else "delta-neg"
        d_sign  = "+" if delta > 0 else ""
        cv_sign = "+" if est_cv > 0 else ""

        st.markdown(
            f"""
            <div class="realloc-row">
              <div class="realloc-segment">
                {row['segment']}
                <div class="realloc-platform">▸ {row['platform']}</div>
              </div>
              <div class="realloc-num" style="color:#8A96B8;">${row['spend']:,.0f}</div>
              <div class="realloc-num" style="color:#C8D0E7;">${row['new_spend']:,.0f}</div>
              <div class="realloc-delta {d_class}">{d_sign}${abs(delta):,.0f}</div>
              <div class="realloc-delta {d_class}">{cv_sign}{est_cv:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── ROAS comparison ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Current Portfolio ROAS", f"{proj['current_roas']:.2f}×")
    with m2:
        st.metric("Projected ROAS",
                  f"{proj['new_roas']:.2f}×",
                  delta=f"+{proj['roas_lift']:.2f}× ROAS lift")
    with m3:
        st.metric("Wasted Spend Recovered",
                  f"${proj['freed_budget']:,.0f}",
                  delta="Reallocated to winners", delta_color="off")

    with st.expander("🎓  Workshop: The Optimisation Model Explained"):
        st.markdown(f"""
**What the agent optimises for:** Total portfolio conversions, subject to a fixed budget.

**The 20% cut rule:**
Rather than zeroing out underperformers immediately (which could damage retargeting
audiences built over months), the agent applies a conservative **{CUT_FRACTION:.0%} reduction**.
This reduces waste while giving the creative team time to deploy the new variants from
Module 02. If the segment still underperforms after 14 days with new creative, the agent
escalates to a 50% cut.

**Recipient weighting:**
Freed budget is distributed to the top {TOP_N_RECIPIENTS} performers weighted by their current
conversion volume — so the segment with the most proven demand gets the largest share.
This is a *greedy* heuristic. A full Mixed-Integer Programming model would account for
diminishing returns as saturation increases.

**Conversion projection:**
Projected conversions assume constant CPA for the period. In reality:
- Gainers may see slight CPA *increases* as spend scales (saturation)
- Losers see larger proportional drops in conversions than the math suggests
  (brand damage from reduced frequency)

Both effects mean the real net gain may be lower than shown — but consistently in
the same direction (better).
        """)
