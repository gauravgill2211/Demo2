"""
styling.py
----------
Global CSS injection and Plotly chart theme for the application.

Design system:
  Ground:   #070D1A  (deep navy)
  Surface:  #0F1729
  Card:     #141E33
  Border:   #1E2D4A
  Primary:  #5B6EF5  (indigo)
  Teal:     #1FCEAB  (data highlight)
  Warning:  #F4AC32
  Critical: #F05252
  Text:     #C8D0E7
  Muted:    #5A6482
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Plotly shared chart configuration
# ---------------------------------------------------------------------------

CHART_COLORS = {
    "primary":   "#5B6EF5",
    "teal":      "#1FCEAB",
    "warning":   "#F4AC32",
    "critical":  "#F05252",
    "good":      "#2ECC8F",
    "muted":     "#5A6482",
    "purple":    "#A78BFA",
    "pink":      "#F472B6",
    "cyan":      "#22D3EE",
}

# Ordered palette for multi-series charts
SERIES_PALETTE = [
    "#5B6EF5", "#1FCEAB", "#F4AC32", "#F05252",
    "#A78BFA", "#F472B6", "#22D3EE", "#2ECC8F",
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(20,30,51,0.45)",
    font=dict(family="Inter, sans-serif", color="#8A96B8", size=12),
    xaxis=dict(
        gridcolor="rgba(94,107,150,0.12)",
        linecolor="rgba(94,107,150,0.2)",
        tickfont=dict(size=11, color="#8A96B8"),
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor="rgba(94,107,150,0.12)",
        linecolor="rgba(94,107,150,0.2)",
        tickfont=dict(size=11, color="#8A96B8"),
        zeroline=False,
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color="#8A96B8"),
        bordercolor="rgba(0,0,0,0)",
    ),
    margin=dict(l=10, r=10, t=36, b=10),
    hoverlabel=dict(
        bgcolor="#0F1729",
        bordercolor="#1E2D4A",
        font=dict(family="Inter, sans-serif", color="#C8D0E7", size=12),
    ),
)


def performance_color(tier: str) -> str:
    """Map a performance tier string to its hex color."""
    return {
        "Excellent":       CHART_COLORS["teal"],
        "Good":            CHART_COLORS["good"],
        "Underperforming": CHART_COLORS["warning"],
        "Critical":        CHART_COLORS["critical"],
    }.get(tier, CHART_COLORS["muted"])


# ---------------------------------------------------------------------------
# CSS injection
# ---------------------------------------------------------------------------

def apply_custom_css() -> None:
    """Inject the application-wide CSS into the Streamlit page."""
    st.markdown(
        """
        <style>
        /* ── Google Fonts ─────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Ground ───────────────────────────────────────────────── */
        html, body, [data-testid="stAppViewContainer"] {
            background: #070D1A !important;
        }
        .main .block-container {
            padding: 2rem 2.5rem 4rem !important;
            max-width: 1280px;
        }

        /* ── Sidebar ──────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background: #0A1020 !important;
            border-right: 1px solid #1E2D4A !important;
        }
        section[data-testid="stSidebar"] > div { padding: 1.25rem 1rem; }

        /* ── Typography base ──────────────────────────────────────── */
        body, p, li, label, .stMarkdown {
            font-family: 'Inter', sans-serif !important;
            color: #C8D0E7;
        }
        h1, h2, h3, h4 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            text-wrap: balance;
        }

        /* ── Streamlit radio as nav ───────────────────────────────── */
        div[data-testid="stRadio"] > label { display: none; }
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        div[data-testid="stRadio"] > div > label {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: #8A96B8 !important;
            padding: 10px 14px !important;
            border-radius: 8px !important;
            cursor: pointer;
            transition: all 0.15s ease;
            border: none !important;
        }
        div[data-testid="stRadio"] > div > label:hover {
            background: rgba(91,110,245,0.12) !important;
            color: #C8D0E7 !important;
        }
        div[data-testid="stRadio"] > div > label[data-selected="true"] {
            background: rgba(91,110,245,0.18) !important;
            color: #7F8FFF !important;
            border-left: 3px solid #5B6EF5 !important;
        }

        /* ── Streamlit native metric cards ────────────────────────── */
        [data-testid="stMetric"] {
            background: #141E33;
            border: 1px solid #1E2D4A;
            border-radius: 12px;
            padding: 16px 20px !important;
        }
        [data-testid="stMetricLabel"] {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.08em !important;
            color: #5A6482 !important;
            text-transform: uppercase;
        }
        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.65rem !important;
            font-weight: 500 !important;
            color: #E8EDF8 !important;
        }
        [data-testid="stMetricDelta"] {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.78rem !important;
        }

        /* ── Primary button ───────────────────────────────────────── */
        .stButton > button {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            background: linear-gradient(135deg, #5B6EF5 0%, #7F5CF5 100%) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.75rem !important;
            letter-spacing: 0.02em;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 20px rgba(91,110,245,0.35) !important;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 28px rgba(91,110,245,0.5) !important;
        }
        .stButton > button:active { transform: translateY(0); }

        /* ── Select / dropdown ────────────────────────────────────── */
        .stSelectbox > div > div {
            background: #141E33 !important;
            border: 1px solid #1E2D4A !important;
            border-radius: 8px !important;
            color: #C8D0E7 !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* ── Dataframe ────────────────────────────────────────────── */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #1E2D4A;
        }

        /* ── Progress bar ─────────────────────────────────────────── */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #5B6EF5, #1FCEAB) !important;
        }

        /* ── Expander ─────────────────────────────────────────────── */
        [data-testid="stExpander"] {
            background: #0F1729;
            border: 1px solid #1E2D4A !important;
            border-radius: 10px !important;
        }
        [data-testid="stExpander"] summary {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.875rem !important;
            color: #8A96B8 !important;
        }

        /* ── Divider ─────────────────────────────────────────────── */
        hr { border-color: #1E2D4A !important; margin: 1rem 0 !important; }

        /* ── Spinner ─────────────────────────────────────────────── */
        .stSpinner > div { border-top-color: #5B6EF5 !important; }

        /* ══════════════════════════════════════════════════════════
           Custom HTML component classes
           ══════════════════════════════════════════════════════════ */

        /* ── Page header ─────────────────────────────────────────── */
        .page-header {
            margin-bottom: 2rem;
        }
        .page-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 500;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #5B6EF5;
            margin-bottom: 0.4rem;
        }
        .page-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.9rem;
            font-weight: 800;
            color: #E8EDF8;
            margin: 0 0 0.35rem 0;
            line-height: 1.15;
            text-wrap: balance;
        }
        .page-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #5A6482;
            margin: 0;
        }

        /* ── Workshop callout ────────────────────────────────────── */
        .workshop-callout {
            border-left: 3px solid #5B6EF5;
            background: rgba(91,110,245,0.07);
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.25rem;
            margin: 1.25rem 0;
        }
        .workshop-callout-header {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #5B6EF5;
            margin-bottom: 0.5rem;
        }
        .workshop-callout p {
            font-family: 'Inter', sans-serif;
            font-size: 0.875rem;
            color: #8A96B8;
            margin: 0;
            line-height: 1.65;
        }

        /* ── Alert banner ────────────────────────────────────────── */
        .alert-banner {
            background: rgba(240,82,82,0.1);
            border: 1px solid rgba(240,82,82,0.3);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin: 1rem 0;
        }
        .alert-icon { font-size: 1.25rem; }
        .alert-text {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.9rem;
            font-weight: 700;
            color: #F9A8A8;
        }

        /* ── Performance badge ───────────────────────────────────── */
        .badge {
            display: inline-block;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding: 3px 9px;
            border-radius: 4px;
        }
        .badge-excellent   { background: rgba(31,206,171,0.15); color: #1FCEAB; }
        .badge-good        { background: rgba(46,204,143,0.15); color: #2ECC8F; }
        .badge-under       { background: rgba(244,172,50,0.15);  color: #F4AC32; }
        .badge-critical    { background: rgba(240,82,82,0.15);   color: #F05252; }

        /* ── Underperformer highlight card ───────────────────────── */
        .offender-card {
            background: #141E33;
            border: 1px solid rgba(240,82,82,0.25);
            border-top: 3px solid #F05252;
            border-radius: 10px;
            padding: 1rem 1.1rem;
        }
        .offender-card.warn {
            border-color: rgba(244,172,50,0.3);
            border-top-color: #F4AC32;
        }
        .offender-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #5A6482;
            margin-bottom: 0.3rem;
        }
        .offender-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.4rem;
            font-weight: 500;
            color: #F05252;
        }
        .offender-card.warn .offender-value { color: #F4AC32; }
        .offender-name {
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: #8A96B8;
            margin-top: 0.25rem;
        }
        .offender-platform {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: #3D4E6B;
            margin-top: 0.1rem;
        }

        /* ── Current ad copy box ─────────────────────────────────── */
        .ad-copy-box {
            background: #0A1020;
            border: 1px solid #1E2D4A;
            border-radius: 10px;
            padding: 1.25rem;
        }
        .ad-copy-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #3D4E6B;
            margin-bottom: 0.35rem;
        }
        .ad-copy-headline {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: #C8D0E7;
            margin-bottom: 0.5rem;
        }
        .ad-copy-body {
            font-family: 'Inter', sans-serif;
            font-size: 0.845rem;
            color: #5A6482;
            line-height: 1.6;
        }
        .ad-copy-cta {
            display: inline-block;
            margin-top: 0.75rem;
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            font-weight: 600;
            color: #3D4E6B;
            border: 1px solid #1E2D4A;
            border-radius: 5px;
            padding: 3px 10px;
        }

        /* ── Agent thinking status ───────────────────────────────── */
        .agent-status {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: #5B6EF5;
            padding: 0.6rem 0;
        }

        /* ── Variant card ────────────────────────────────────────── */
        .variant-card {
            background: #141E33;
            border: 1px solid #1E2D4A;
            border-radius: 12px;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1rem;
            transition: border-color 0.2s ease;
        }
        .variant-card:hover { border-color: rgba(91,110,245,0.5); }
        .variant-tag-row {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }
        .variant-letter {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            font-weight: 500;
            background: rgba(91,110,245,0.2);
            color: #7F8FFF;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .variant-name {
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: #5A6482;
        }
        .variant-headline {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: #E8EDF8;
            margin-bottom: 0.6rem;
            line-height: 1.3;
        }
        .variant-body {
            font-family: 'Inter', sans-serif;
            font-size: 0.845rem;
            color: #8A96B8;
            line-height: 1.65;
            margin-bottom: 0.85rem;
        }
        .variant-rationale {
            border-top: 1px solid #1E2D4A;
            padding-top: 0.75rem;
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            color: #3D4E6B;
            line-height: 1.55;
        }
        .variant-rationale strong { color: #5A6482; }

        /* ── Sidebar logo block ──────────────────────────────────── */
        .sidebar-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.25rem 0 1rem 0;
        }
        .logo-icon {
            font-size: 1.75rem;
            background: rgba(91,110,245,0.15);
            width: 44px;
            height: 44px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .logo-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.95rem;
            font-weight: 800;
            color: #E8EDF8;
        }
        .logo-sub {
            font-family: 'Inter', sans-serif;
            font-size: 0.68rem;
            color: #3D4E6B;
            margin-top: 1px;
        }

        /* ── Sidebar stat row ────────────────────────────────────── */
        .sidebar-stat {
            text-align: center;
        }
        .sidebar-stat-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.1rem;
            font-weight: 500;
            color: #C8D0E7;
        }
        .sidebar-stat-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.65rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #3D4E6B;
            margin-top: 2px;
        }

        /* ── Budget reallocation table ───────────────────────────── */
        .realloc-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #1E2D4A;
            font-family: 'Inter', sans-serif;
            font-size: 0.845rem;
        }
        .realloc-row:last-child { border-bottom: none; }
        .realloc-segment { flex: 1; color: #C8D0E7; }
        .realloc-platform {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #3D4E6B;
        }
        .realloc-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            font-variant-numeric: tabular-nums;
            min-width: 80px;
            text-align: right;
        }
        .realloc-delta {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            font-variant-numeric: tabular-nums;
            min-width: 80px;
            text-align: right;
        }
        .delta-pos { color: #1FCEAB; }
        .delta-neg { color: #F05252; }

        /* ── Projected impact strip ──────────────────────────────── */
        .impact-strip {
            background: linear-gradient(135deg, rgba(31,206,171,0.07) 0%, rgba(91,110,245,0.07) 100%);
            border: 1px solid rgba(31,206,171,0.2);
            border-radius: 12px;
            padding: 1.5rem 2rem;
            text-align: center;
        }
        .impact-number {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.8rem;
            font-weight: 500;
            color: #1FCEAB;
            line-height: 1;
        }
        .impact-label {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: #5A6482;
            margin-top: 0.35rem;
            letter-spacing: 0.03em;
        }

        /* ── Section divider label ───────────────────────────────── */
        .section-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            font-weight: 500;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #3D4E6B;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #1E2D4A;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# HTML helper factories
# ---------------------------------------------------------------------------

def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    """Render the standard page header block."""
    st.markdown(
        f"""
        <div class="page-header">
          <div class="page-eyebrow">{eyebrow}</div>
          <h1 class="page-title">{title}</h1>
          <p class="page-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def workshop_callout(body: str) -> None:
    """Render a left-ruled workshop explanatory callout."""
    st.markdown(
        f"""
        <div class="workshop-callout">
          <div class="workshop-callout-header">🎓 Workshop — What is the Agent Doing?</div>
          <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tier_badge(tier: str) -> str:
    """Return the HTML badge for a performance tier."""
    class_map = {
        "Excellent":       "badge-excellent",
        "Good":            "badge-good",
        "Underperforming": "badge-under",
        "Critical":        "badge-critical",
    }
    css = class_map.get(tier, "badge-good")
    return f'<span class="badge {css}">{tier}</span>'


def section_label(text: str) -> None:
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)
