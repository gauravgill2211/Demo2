"""
app.py
------
Agentic Campaign Optimization Engine — Main Entry Point

Workshop: AI Agents in Marketing
---------------------------------
This Streamlit application demonstrates how AI agents can autonomously:
  1. Monitor campaign data in real time (Dashboard)
  2. Detect underperforming segments using threshold rules (Anomaly Detection)
  3. Diagnose creative failures and generate replacement copy (Creative Optimizer)
  4. Reallocate budget from losers to winners (Budget Reallocation Engine)

Run with:
    streamlit run app.py
"""

import streamlit as st

from utils.styling import apply_custom_css
from data.campaign_data import get_campaign_data
from components.dashboard import render_dashboard
from components.anomaly_detection import render_anomaly_detection
from components.creative_optimizer import render_creative_optimizer
from components.budget_reallocation import render_budget_reallocation


# ---------------------------------------------------------------------------
# Page config — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Agentic Campaign Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Apply global CSS
# ---------------------------------------------------------------------------
apply_custom_css()

# ---------------------------------------------------------------------------
# Load data (cached so it doesn't regenerate on every interaction)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Cache the campaign DataFrame for the session."""
    return get_campaign_data()


df = load_data()

# Derived summary stats for the sidebar
total_spend   = df["spend"].sum()
total_convs   = df["conversions"].sum()
n_under       = int(df["is_underperformer"].sum())

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:

    # Brand / logo block
    st.markdown(
        """
        <div class="sidebar-logo">
          <div class="logo-icon">🤖</div>
          <div>
            <div class="logo-title">MarketingAI</div>
            <div class="logo-sub">Campaign Optimization Engine</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<hr style="margin:0.5rem 0 1rem 0;">', unsafe_allow_html=True)

    # Navigation
    page = st.radio(
        "nav",
        options=[
            "📊  Campaign Dashboard",
            "🔍  Anomaly Detection",
            "✨  Creative Optimizer",
            "💰  Budget Reallocation",
        ],
        label_visibility="collapsed",
    )

    st.markdown('<hr style="margin:1rem 0;">', unsafe_allow_html=True)

    # Live sidebar stats
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.62rem;'
        'letter-spacing:0.12em;text-transform:uppercase;color:#3D4E6B;'
        'margin-bottom:0.75rem;">Portfolio Snapshot</div>',
        unsafe_allow_html=True,
    )

    s1, s2 = st.columns(2)
    with s1:
        st.markdown(
            f'<div class="sidebar-stat">'
            f'<div class="sidebar-stat-val">${total_spend / 1000:.1f}K</div>'
            f'<div class="sidebar-stat-label">Total Spend</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f'<div class="sidebar-stat">'
            f'<div class="sidebar-stat-val">{total_convs:,}</div>'
            f'<div class="sidebar-stat-label">Conversions</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    s3, s4 = st.columns(2)
    with s3:
        st.markdown(
            f'<div class="sidebar-stat">'
            f'<div class="sidebar-stat-val">{len(df)}</div>'
            f'<div class="sidebar-stat-label">Segments</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with s4:
        color = "#F05252" if n_under > 0 else "#1FCEAB"
        st.markdown(
            f'<div class="sidebar-stat">'
            f'<div class="sidebar-stat-val" style="color:{color};">{n_under}</div>'
            f'<div class="sidebar-stat-label">Flagged</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr style="margin:1rem 0 0.75rem 0;">', unsafe_allow_html=True)

    # Workshop badge
    st.markdown(
        '<div style="font-family:\'Inter\',sans-serif;font-size:0.72rem;'
        'color:#3D4E6B;line-height:1.5;">'
        '🎓 <strong style="color:#5A6482;">AI Agents in Marketing</strong><br>'
        'Workshop Demo · All data is synthetic'
        '</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Route to the selected page
# ---------------------------------------------------------------------------
if "Dashboard" in page:
    render_dashboard(df)

elif "Anomaly" in page:
    render_anomaly_detection(df)

elif "Creative" in page:
    render_creative_optimizer(df)

elif "Budget" in page:
    render_budget_reallocation(df)
