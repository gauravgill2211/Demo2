# 🤖 Agentic Campaign Optimization Engine

> **Workshop demo** — AI Agents in Marketing  
> All campaign data is synthetic and generated at runtime.

---

## What This App Demonstrates

This Streamlit application shows how a multi-module AI agent system can autonomously manage a marketing campaign portfolio:

| Module | What the Agent Does |
|--------|---------------------|
| **Campaign Dashboard** | Monitors KPIs in real time across all audience segments |
| **Anomaly Detection** | Flags segments where CPA > $50 or CTR < 0.5% |
| **Creative Optimizer** | Diagnoses creative failures and generates 3 replacement ad copy variants |
| **Budget Reallocation** | Cuts 20% from underperformers and redistributes to top 3 performers |

---

## Project Structure

```
Demo1/
├── app.py                        # Main entry point — routing + sidebar
├── data/
│   └── campaign_data.py          # Synthetic campaign data + AI analysis text
├── components/
│   ├── dashboard.py              # Page 1: KPIs, Spend vs Conversions, 30-day trend
│   ├── anomaly_detection.py      # Page 2: Quadrant scatter, offender cards, table
│   ├── creative_optimizer.py     # Page 3: Agent animation, root-cause + 3 variants
│   └── budget_reallocation.py    # Page 4: Donut charts, delta table, projections
├── utils/
│   └── styling.py                # CSS injection, Plotly theme, HTML helpers
├── .streamlit/
│   └── config.toml               # Dark theme + Streamlit server config
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1 — Install dependencies

```bash
pip install -r requirements.txt
```

### 2 — Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Design System

| Token | Value | Role |
|-------|-------|------|
| Ground | `#070D1A` | Page background |
| Surface | `#0F1729` | Section background |
| Card | `#141E33` | Card / component background |
| Primary | `#5B6EF5` | Indigo — interactive + AI accent |
| Teal | `#1FCEAB` | Data highlights, top performers |
| Warning | `#F4AC32` | Underperforming segments |
| Critical | `#F05252` | Worst-offender alerts |
| Text | `#C8D0E7` | Body copy |
| Muted | `#5A6482` | Labels, supporting text |

**Typefaces**  
- Display headings: *Plus Jakarta Sans* (800 weight)  
- Body & UI: *Inter*  
- Numbers & code: *JetBrains Mono*

---

## Data

### Campaign Segments (12 total)

Eight segments perform at or above threshold. Four are intentionally underperforming:

| Segment | Platform | CPA | CTR | Status |
|---------|----------|-----|-----|--------|
| 55+ Retirees | Facebook | $362.50 | 0.60% | 🔴 Critical |
| 40-60 Healthcare | Google | $251.61 | 1.00% | 🟠 Underperforming |
| 18-24 Mobile Gaming | TikTok | $190.91 | 0.40% | 🔴 Critical |
| 18-24 Students | TikTok | $150.00 | 0.50% | 🟠 Underperforming |

### Budget Reallocation Logic

```
freed_budget = sum(underperformer_spend × 0.20)
top_3        = segments ranked by conversion volume (excluding underperformers)
allocation   = freed_budget × (segment_conversions / top_3_total_conversions)
```

---

## Workshop Notes

Each page includes an expandable **🎓 Workshop** callout explaining what the agent is doing at each step — making the application self-teaching for attendees who want to understand the mechanics behind the UI.

The **Creative Optimizer** simulates a multi-stage LLM reasoning loop with a progress animation, then surfaces:
1. A root-cause diagnosis (formatted as structured markdown)
2. Three targeted ad copy variants with strategic rationale

In a production system, these variants would be submitted directly to the ad platform API for automated A/B testing.

---

## Extending the App

| Extension idea | Where to change |
|----------------|-----------------|
| Connect real platform data | Replace `get_campaign_data()` in `data/campaign_data.py` |
| Use a real LLM for copy generation | Replace `get_ai_analysis()` with an Anthropic / OpenAI API call |
| Add email alerts for anomalies | Add a notification module triggered in `anomaly_detection.py` |
| Add a 5th page for A/B test results | Create `components/ab_testing.py` + add a route in `app.py` |

---

*Built for the AI Agents in Marketing workshop. All data is synthetic.*
