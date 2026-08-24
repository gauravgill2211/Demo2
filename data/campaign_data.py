"""
campaign_data.py
-----------------
All dummy data for the Agentic Campaign Optimization Engine.

Contains:
- 12 audience segments across 5 platforms (4 intentionally underperforming)
- 30-day daily performance trend
- Current "bad" ad copy for each underperformer
- Pre-written AI analysis + 3 copy variants per underperformer
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Primary campaign data
# ---------------------------------------------------------------------------

def get_campaign_data() -> pd.DataFrame:
    """
    Generate the main campaign segments DataFrame.
    Metrics: spend, impressions, clicks, conversions, CTR, CPA, ROAS.
    Underperformer thresholds: CPA > $50 OR CTR < 0.5%
    """
    raw = {
        "segment": [
            "18-35 Fashion & Beauty",      # top performer
            "25-34 Fitness & Wellness",     # top performer
            "35-44 Parents",               # top performer
            "25-34 Tech Enthusiasts",      # good
            "25-44 Gamers",               # good
            "30-50 Business Owners",       # good
            "35-44 Homeowners",           # good
            "45-54 Professionals",         # good
            # — Underperformers below —
            "55+ Retirees",               # critical
            "40-60 Healthcare",           # underperforming
            "18-24 Students",             # underperforming
            "18-24 Mobile Gaming",        # underperforming (low CTR + high CPA)
        ],
        "platform": [
            "Instagram", "Instagram", "Google", "Google",
            "YouTube",   "LinkedIn",  "Facebook", "LinkedIn",
            "Facebook",  "Google",    "TikTok",   "TikTok",
        ],
        "spend": [
            3_600, 3_200, 7_200, 8_500,
            4_500, 9_200, 6_300, 5_800,
            2_900, 7_800, 1_800, 4_200,
        ],
        "impressions": [
            480_000, 210_000, 380_000, 450_000,
            620_000, 120_000, 190_000,  95_000,
             85_000, 210_000, 320_000, 280_000,
        ],
        "clicks": [
            14_400, 6_300, 7_220, 9_000,
             5_580, 3_000, 3_990, 2_375,
               510, 2_100, 1_600, 1_120,
        ],
        "conversions": [
            312, 156, 198, 185,
             93, 196, 148, 118,
              8,  31,  12,  22,
        ],
    }

    df = pd.DataFrame(raw)

    # Derived metrics
    df["ctr"]               = (df["clicks"] / df["impressions"] * 100).round(2)
    df["cpa"]               = (df["spend"] / df["conversions"]).round(2)
    df["roas"]              = ((df["conversions"] * 52) / df["spend"]).round(2)
    df["conversion_rate"]   = (df["conversions"] / df["clicks"] * 100).round(2)

    # Performance classification
    df["is_underperformer"] = (df["cpa"] > 50) | (df["ctr"] < 0.5)

    def _tier(row):
        if row["cpa"] > 150:
            return "Critical"
        if row["cpa"] > 50 or row["ctr"] < 0.5:
            return "Underperforming"
        if row["cpa"] <= 25:
            return "Excellent"
        return "Good"

    df["performance_tier"] = df.apply(_tier, axis=1)

    return df


# ---------------------------------------------------------------------------
# 30-day daily trend
# ---------------------------------------------------------------------------

def get_daily_trend_data() -> pd.DataFrame:
    """
    Simulate 30 days of aggregated daily performance with a gentle upward trend.
    """
    np.random.seed(42)
    today = datetime.now().date()
    dates = [today - timedelta(days=x) for x in range(29, -1, -1)]

    records = []
    for i, d in enumerate(dates):
        trend = 1 + (i / 30) * 0.18
        noise = np.random.uniform(0.87, 1.13)
        spend       = round(1_840 * trend * noise, 2)
        impressions = int(np.random.randint(19_000, 26_000) * noise)
        clicks      = int(impressions * np.random.uniform(0.016, 0.026))
        conversions = int(max(np.random.randint(34, 52) * trend * noise, 1))
        records.append({
            "date":        d.strftime("%Y-%m-%d"),
            "spend":       spend,
            "impressions": impressions,
            "clicks":      clicks,
            "conversions": conversions,
            "cpa":         round(spend / conversions, 2),
        })

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Current (bad) ad copy — used in the Creative Optimizer page
# ---------------------------------------------------------------------------

def get_current_ad_copy() -> dict:
    """
    Simulates the live, poorly-performing creative currently running for
    each underperforming segment. These are deliberately generic/misaligned
    to make the agent's improvements obvious.
    """
    return {
        "55+ Retirees": {
            "headline":     "Shop the Latest Trends Today!",
            "primary_text": "Upgrade your lifestyle with our revolutionary products. "
                            "Limited time offer — act fast! 🔥 Don't miss out on the "
                            "best deals of the season.",
            "cta":          "Shop Now",
        },
        "40-60 Healthcare": {
            "headline":     "Best Healthcare Solutions | Get Started",
            "primary_text": "We offer comprehensive healthcare services for all your "
                            "needs. Contact us today and see why thousands choose us "
                            "for their health journey.",
            "cta":          "Contact Us Today",
        },
        "18-24 Students": {
            "headline":     "Save Money on Your Education",
            "primary_text": "We help students achieve their goals with our premium "
                            "platform. Start your free trial and transform your future "
                            "with the power of learning.",
            "cta":          "Start Free Trial",
        },
        "18-24 Mobile Gaming": {
            "headline":     "Level Up Your Game Today",
            "primary_text": "Our gaming products will take your experience to the next "
                            "level. Shop now for the best deals and dominate the "
                            "competition.",
            "cta":          "Shop Now",
        },
    }


# ---------------------------------------------------------------------------
# Pre-written AI analysis + copy variants
# ---------------------------------------------------------------------------

def get_ai_analysis() -> dict:
    """
    Simulates the structured output of an LLM agent that has diagnosed
    the root cause of each underperformer and produced 3 targeted ad
    copy variants.

    Each entry contains:
        analysis  (str) – markdown-formatted root cause breakdown
        variants  (list[dict]) – 3 copy variants, each with:
            name, headline, primary_text, rationale
    """
    return {
        # ──────────────────────────────────────────────────
        "55+ Retirees": {
            "analysis": """\
**Root Cause Analysis — 55+ Retirees / Facebook**

Agent has identified **3 critical creative misalignments** driving a **$362.50 CPA** \
(7.3× above the $50 target):

1. **Generational tone mismatch.** High-energy language ("Latest Trends!", "act fast!", 🔥) \
creates an authenticity gap. This demographic has a 65 % longer consideration cycle than 18–34 \
audiences and responds to reliability — not manufactured FOMO.

2. **Missing trust architecture.** Zero social proof, zero guarantee language, zero credibility \
markers. For 55+ audiences, trust outranks price *and* features as the #1 purchase driver.

3. **Wrong value frame.** "Upgrade your lifestyle" implies dissatisfaction. This segment is \
identity-secure and responds better to *enhancement* framing ("for people who know what they want") \
than disruption messaging.

**Agent recommendation:** Shift from urgency-driven to trust-driven creative. Lead with social \
proof, use measured language, anchor on guarantees and return ease.""",
            "variants": [
                {
                    "name":         "Variant A — Social Proof & Trust",
                    "headline":     "Trusted by 50,000+ Customers Since 2018",
                    "primary_text": "When quality matters most, discerning shoppers choose us. "
                                    "No pressure, no gimmicks — just the products your lifestyle "
                                    "deserves, backed by our 60-day satisfaction guarantee. "
                                    "See why customers like Margaret, 63, say: "
                                    "\"I wish I'd found this sooner.\"",
                    "rationale":    "Leads with a specific social-proof number, removes all urgency "
                                    "language, adds a relatable first-name testimonial, anchors "
                                    "on a strong guarantee.",
                },
                {
                    "name":         "Variant B — Quality & Longevity",
                    "headline":     "Premium Craftsmanship, Built to Last a Lifetime",
                    "primary_text": "You've spent decades learning what truly matters. "
                                    "Our products are designed for people who demand lasting "
                                    "quality — not disposable trends. Free shipping, easy returns, "
                                    "and a dedicated care team ready whenever you need them.",
                    "rationale":    "Respects accumulated life experience, emphasises durability "
                                    "over novelty, eliminates every urgency cue, and highlights "
                                    "frictionless service.",
                },
                {
                    "name":         "Variant C — Exclusive Appreciation Offer",
                    "headline":     "A Special Thank-You for Our Most Valued Customers",
                    "primary_text": "We've reserved a 20 % member discount exclusively for "
                                    "customers 55 and over this month. No countdown clocks, "
                                    "no pressure — browse at your own pace, read every detail, "
                                    "and purchase when you're ready. Your complete satisfaction "
                                    "is our only priority.",
                    "rationale":    "Age-specific exclusivity creates positive identity signal, "
                                    "explicitly removes urgency, emphasises buyer autonomy and "
                                    "a satisfaction-first commitment.",
                },
            ],
        },

        # ──────────────────────────────────────────────────
        "40-60 Healthcare": {
            "analysis": """\
**Root Cause Analysis — 40-60 Healthcare / Google**

Agent diagnostic complete. **$251.61 CPA** traced to a 3-layer problem:

1. **Keyword relevance collapse.** Copy is so generic ("comprehensive healthcare services \
for all your needs") it earns near-zero Quality Score. Estimated 60–70 % of clicks are \
broad-match informational queries — burning budget on non-converting traffic.

2. **Zero credibility specifics.** "Thousands choose us" with no number, no star rating, \
and no certification badge is immediately dismissed by a research-intensive, high-anxiety \
audience. They need *proof*, not claims.

3. **Commitment barrier too high.** "Contact Us Today" as a cold first-touch CTA in a \
high-stakes category (personal health) is a conversion wall. The first ask should be \
low-friction: a free assessment, a guide, a second opinion.

**Agent recommendation:** Hyper-specific copy with verifiable credentials, number-driven \
proof points, and a low-commitment discovery CTA.""",
            "variants": [
                {
                    "name":         "Variant A — Credentials + Accessibility",
                    "headline":     "Board-Certified Specialists | Same-Week Appointments",
                    "primary_text": "Stop waiting months for answers. Our network of 300+ "
                                    "board-certified physicians specialises in adults 40–65, "
                                    "with same-week availability and telehealth options. "
                                    "Insurance accepted. Rated 4.8 ★ across 12,000+ verified "
                                    "patient reviews.",
                    "rationale":    "Solves the waiting-time pain point immediately, backs every "
                                    "claim with specifics (300 physicians, 4.8★, 12K reviews), "
                                    "and removes two common friction points (insurance, distance).",
                },
                {
                    "name":         "Variant B — Preventive Value Proposition",
                    "headline":     "Comprehensive Wellness Plans from $89 / Month",
                    "primary_text": "At 40+, proactive health management is the highest-return "
                                    "decision you'll make. Our all-inclusive plans cover annual "
                                    "panels, specialist consultations, and personalised health "
                                    "coaching. Join 85,000+ members who took control — before "
                                    "something forced them to.",
                    "rationale":    "Specific price anchor removes uncertainty, reframes health "
                                    "spend as investment, community proof (85K), and adds "
                                    "gentle urgency without pressure.",
                },
                {
                    "name":         "Variant C — Free Assessment Entry",
                    "headline":     "Your Free 3-Minute Health Assessment Starts Here",
                    "primary_text": "Not sure where to begin? Our free assessment identifies "
                                    "your top risk factors and matches you with specialists "
                                    "focused on your specific concerns. Used by 140,000+ patients "
                                    "aged 40–65. No commitment required — just clarity.",
                    "rationale":    "Eliminates the commitment barrier entirely, leads with zero-"
                                    "risk free value, emphasises age-bracket specificity, and "
                                    "removes every sales signal.",
                },
            ],
        },

        # ──────────────────────────────────────────────────
        "18-24 Students": {
            "analysis": """\
**Root Cause Analysis — 18-24 Students / TikTok**

Agent has flagged a **Platform Culture Mismatch** as the primary driver of a **$150 CPA**:

1. **Corporate language in a native-content feed.** TikTok's algorithm penalises ad-signalling \
copy. "Premium platform", "transform your future", and "achieve their goals" are the exact phrases \
Gen Z scrolls past in 0.3 seconds. Authenticity is the algorithm's currency.

2. **Wrong pain point.** "Save Money on Your Education" is LinkedIn-level messaging in a TikTok \
context. This cohort responds to peer FOMO, social validation, fast-setup, and humour — not tuition \
economics.

3. **Missing native format signals.** The copy structure reads like a transposed Facebook ad. \
TikTok-native copy is conversational, punchy, uses direct address, and often breaks the fourth wall.

**Agent recommendation:** Peer-to-peer tone, FOMO-and-social-proof hook, structure copy for a \
1.5-second attention window.""",
            "variants": [
                {
                    "name":         "Variant A — FOMO + Peer Social Proof",
                    "headline":     "Broke But Make It Smart 💸",
                    "primary_text": "Real talk — 2.4M students already figured this out. "
                                    "[Brand] gives you [specific benefit] without the $200/month "
                                    "price tag. Students get 60 % off automatically. No contracts. "
                                    "No corporate BS. Your roommate's not telling you for a reason.",
                    "rationale":    "Authentic Gen Z language, peer positioning, specific number "
                                    "(2.4M), targets real cost pain, in-group framing creates "
                                    "identity-driven appeal.",
                },
                {
                    "name":         "Variant B — Humour + Reverse FOMO",
                    "headline":     "Your Roommate Already Has This. Don't Ask Why. 👀",
                    "primary_text": "While you're reading this, 500K students already [got result] "
                                    "with [Brand]. Takes 3 minutes to set up. Works on your phone. "
                                    "Student discount auto-applied. Why are you still reading? Go.",
                    "rationale":    "Opens with humour, creates FOMO via roommate scenario, speed "
                                    "signal (3 min), direct CTA urgency without sounding corporate.",
                },
                {
                    "name":         "Variant C — Anti-Ad Authenticity",
                    "headline":     "47,000 Students on TikTok Are Talking About This",
                    "primary_text": "Not sponsored. Not an influencer deal. Just students sharing "
                                    "why [Brand] changed their [study/money/social] life. First "
                                    "30 days free — no card required. See what textbooks don't teach.",
                    "rationale":    "Directly addresses Gen Z sponsored-content scepticism, UGC "
                                    "signal copy, zero-friction entry (no card), mystery hook "
                                    "that drives curiosity clicks.",
                },
            ],
        },

        # ──────────────────────────────────────────────────
        "18-24 Mobile Gaming": {
            "analysis": """\
**Root Cause Analysis — 18-24 Mobile Gaming / TikTok**

**Lowest CTR in portfolio: 0.40%.** Agent traced this to a systemic authenticity failure:

1. **Cliché overload.** "Level Up Your Game" and "dominate the competition" are so overused they \
register as invisible noise to actual gamers. This audience has a calibrated BS-detector for brands \
trying to "sound gamer" without delivering gamer substance.

2. **Zero specificity.** The ad could be selling chairs, energy drinks, or cloud servers. Without \
naming real games (CODM, PUBG Mobile, Genshin Impact) or real problems (lag, ping, aim drift), \
you're competing with everyone and converting no one.

3. **No competitive or community hook.** Mobile gaming at this age is social, ranked, and tribal. \
The current copy ignores ladder culture, streamer ecosystems, and the FOMO of being outplayed. It \
sells product features to an audience that buys *player identity*.

**Agent recommendation:** Hyper-specific game/problem reference, insider language, competitive \
identity angle, in-group/out-group framing.""",
            "variants": [
                {
                    "name":         "Variant A — Insider Advantage",
                    "headline":     "The Setup Pro Streamers Don't Want You to Know 🎮",
                    "primary_text": "847K competitive mobile gamers found the [Brand] edge — "
                                    "and they're not sharing it. Compatible with CODM, PUBG Mobile, "
                                    "Genshin, and 200+ titles. Tournament-legal. Limited stock "
                                    "(obviously). GGs only.",
                    "rationale":    "Exclusivity + in-group identity, names specific titles for "
                                    "instant relevance, scarcity signal, validates via elite-player "
                                    "reference, uses authentic gaming language.",
                },
                {
                    "name":         "Variant B — Technical Pain Point",
                    "headline":     "Your Ping Is Costing You Ranked Matches. We Fixed It.",
                    "primary_text": "50ms of lag is the difference between Rank 1 and uninstalling. "
                                    "[Brand] users average 73 % fewer lag spikes — verified across "
                                    "2M gaming sessions. Setup: 4 minutes. Free 14-day trial. "
                                    "Stop blaming your connection.",
                    "rationale":    "Leads with the #1 pain point for competitive mobile gamers, "
                                    "uses specific verifiable stats (73 %, 2M sessions), technical "
                                    "credibility, minimal commitment ask.",
                },
                {
                    "name":         "Variant C — Competitive Identity",
                    "headline":     "Ranked #1 by Competitive Players for 3 Seasons 🏆",
                    "primary_text": "Not for casual players. [Brand] was built for people who "
                                    "actually care about winning. 1.2M ranked players. 47 pro team "
                                    "endorsements. Zero pay-to-win. If you're still looking for "
                                    "excuses to lose, this isn't for you. Everyone else: welcome.",
                    "rationale":    "Exclusive identity for serious players, uses competitive "
                                    "hierarchy, negative selling (excludes casuals) creates desire, "
                                    "pro team social proof, sharp closing line.",
                },
            ],
        },
    }
