"""
creative_optimizer.py
---------------------
Page 3 — Agentic Creative Optimization

The user selects an underperforming segment and clicks "Run AI Agent".
A multi-stage progress animation simulates the LLM reasoning loop, then
the agent's output is displayed:
  1. Root-cause analysis (why the current creative is failing)
  2. Three fully-written, audience-targeted ad copy variants
"""

import time
import streamlit as st
import pandas as pd

from utils.styling import (
    page_header,
    workshop_callout,
    section_label,
    CHART_COLORS,
)
from data.campaign_data import get_current_ad_copy, get_ai_analysis


# Agent reasoning stages with (progress_fraction, status_message)
AGENT_STAGES = [
    (0.15, "🔍  Fetching audience intelligence & segment history…"),
    (0.32, "📊  Evaluating creative performance signals…"),
    (0.55, "🧠  Running diagnostic pattern-matching against ad library…"),
    (0.78, "✨  Generating audience-targeted copy variants…"),
    (0.92, "🔬  Scoring variants against brand safety guidelines…"),
    (1.00, "✅  Optimization complete."),
]


def render_creative_optimizer(df: pd.DataFrame) -> None:
    """Render the Agentic Creative Optimization page."""

    # ── Page header ────────────────────────────────────────────────────────
    page_header(
        eyebrow="Agent Module 02 · Creative Optimization",
        title="Agentic Creative Optimizer",
        subtitle="Select a flagged segment and run the AI agent to receive a root-cause diagnosis and three replacement ad variants.",
    )

    workshop_callout(
        "This module shows the <strong>generative loop</strong> of the agent. "
        "It takes the underperforming segment's audience data, its historical CTR/CPA, "
        "and the current creative brief, then prompts an LLM to: (1) diagnose the exact "
        "creative failure, (2) produce three high-specificity replacement variants. "
        "In production, these variants would be A/B tested automatically."
    )

    # ── Session state init ──────────────────────────────────────────────────
    if "creative_results" not in st.session_state:
        st.session_state.creative_results = {}
    if "active_segment" not in st.session_state:
        st.session_state.active_segment = None

    # ── Segment selector ────────────────────────────────────────────────────
    underperformers = (
        df[df["is_underperformer"]]
        .sort_values("cpa", ascending=False)["segment"]
        .tolist()
    )

    section_label("Select Underperforming Segment")
    selected = st.selectbox(
        "Choose a segment flagged by the anomaly agent:",
        options=underperformers,
        label_visibility="collapsed",
    )

    # Clear cached results when the user picks a different segment
    if selected != st.session_state.active_segment:
        st.session_state.active_segment = selected
        st.session_state.creative_results.pop(selected, None)

    # ── Current performance strip ───────────────────────────────────────────
    row = df[df["segment"] == selected].iloc[0]

    st.markdown("<br>", unsafe_allow_html=True)
    section_label("Current Segment Performance")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Platform",    row["platform"])
    with m2:
        st.metric("CPA",         f"${row['cpa']:.2f}",
                  delta=f"${row['cpa'] - 50:.0f} over limit", delta_color="inverse")
    with m3:
        st.metric("CTR",         f"{row['ctr']:.2f}%",
                  delta=f"{row['ctr'] - 0.5:.2f}pp vs 0.5% floor", delta_color="inverse")
    with m4:
        st.metric("Monthly Spend", f"${row['spend']:,.0f}")

    # ── Current ad copy ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    section_label("Current Running Creative (Failing)")
    ad_copy = get_current_ad_copy()

    if selected in ad_copy:
        c = ad_copy[selected]
        st.markdown(
            f"""
            <div class="ad-copy-box">
              <div class="ad-copy-label">Headline</div>
              <div class="ad-copy-headline">{c['headline']}</div>
              <div class="ad-copy-label">Primary Text</div>
              <div class="ad-copy-body">{c['primary_text']}</div>
              <span class="ad-copy-cta">CTA: {c['cta']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No current creative brief on file for this segment.")

    # ── Run agent button ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🤖  Run AI Agent — Analyse & Rewrite", use_container_width=False)

    if run_btn:
        # Animated reasoning stages
        progress_bar  = st.progress(0.0)
        status_holder = st.empty()

        for fraction, message in AGENT_STAGES:
            status_holder.markdown(
                f'<div class="agent-status">{message}</div>',
                unsafe_allow_html=True,
            )
            progress_bar.progress(fraction)
            time.sleep(0.75)

        time.sleep(0.3)
        progress_bar.empty()
        status_holder.empty()

        # Cache results in session state
        all_analysis = get_ai_analysis()
        if selected in all_analysis:
            st.session_state.creative_results[selected] = all_analysis[selected]
        else:
            st.session_state.creative_results[selected] = {
                "analysis": "No pre-computed analysis available for this segment.",
                "variants": [],
            }

    # ── Display cached results ──────────────────────────────────────────────
    if selected in st.session_state.creative_results:
        result = st.session_state.creative_results[selected]

        st.markdown("<br>", unsafe_allow_html=True)
        section_label("Agent Diagnosis — Root Cause Analysis")

        # Analysis block (markdown)
        with st.container():
            st.markdown(result["analysis"])

        # Variants
        if result["variants"]:
            st.markdown("<br>", unsafe_allow_html=True)
            section_label("Agent Output — 3 Optimised Ad Variants")
            _render_variants(result["variants"])

        # Workshop note
        with st.expander("🎓  Workshop: How the Agent Writes Copy", expanded=False):
            st.markdown("""
**Step 1 — Audience Intelligence Pull**

The agent retrieves first-party audience data: demographic breakdowns, past
engagement patterns with similar creatives, psychographic signals (interests,
purchase intent), and platform-specific behavioural benchmarks.

**Step 2 — Creative Failure Classification**

It runs the current creative through a failure taxonomy:
- *Tone mismatch* — does the language match the audience's self-identity?
- *Platform mismatch* — does the format match how this platform serves content?
- *Pain-point mismatch* — does the copy address what this audience actually cares about?
- *Trust deficit* — are there credibility signals the audience needs before converting?

**Step 3 — Constrained Generation**

The LLM generates copy variants under hard constraints:
- Each variant targets a different angle (trust, benefit, identity/community)
- Every claim must be supportable with a real data point
- Character counts match platform specifications
- Brand voice and tone guidelines are enforced via system prompt

**Step 4 — Scoring & Selection**

Variants are scored against a predicted CTR model trained on historical ad
performance, then ranked. In production, the top 2 are submitted directly to
the platform API for automated A/B testing.
            """)


def _render_variants(variants: list) -> None:
    """Render the three ad copy variant cards."""
    letter_map = ["A", "B", "C", "D"]

    for idx, v in enumerate(variants):
        letter = letter_map[idx] if idx < len(letter_map) else str(idx + 1)
        st.markdown(
            f"""
            <div class="variant-card">
              <div class="variant-tag-row">
                <span class="variant-letter">Variant {letter}</span>
                <span class="variant-name">{v['name'].split('—')[-1].strip() if '—' in v['name'] else v['name']}</span>
              </div>
              <div class="variant-headline">{v['headline']}</div>
              <div class="variant-body">{v['primary_text']}</div>
              <div class="variant-rationale">
                <strong>Why this works:</strong>&nbsp; {v['rationale']}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
