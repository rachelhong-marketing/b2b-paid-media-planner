# Brand + Demand: Channel Waterfall for B2B

Brand and demand gen teams typically run separate programs targeting the same people. The problem: a person who watched a brand video looks like a stranger to the demand gen campaign. Nothing passes between them.

This document outlines how to connect brand and demand gen channels into a single journey — using audience signals as the handoff mechanism.

---

## The Core Idea

Three principles underpin the whole model:

1. **A person's behavior decides who talks to them.** Brand leads awareness. Demand gen takes over when someone shows product interest. Sales takes over after they engage with a lead capture moment.

2. **The click is the bridge.** A tracked landing page behind every ad is what lets one channel feed another. Without it, every ad impression stays siloed in platform data.

3. **Every retarget moves people one step forward.** Don't show the same ad again. Show the next thing — deeper content, a more specific proof point, a lower-friction conversion ask.

---

## The Five-Stage Journey

| Stage | Goal | Who leads | Signal you can see |
|---|---|---|---|
| **Awareness** | Make target accounts know the brand | Brand | Intent data (ZoomInfo/6sense), video views, reach |
| **Interest** | First product-level engagement | Demand Gen (Brand supports) | Site visit, ad click, video completion |
| **Consideration** | Comparing vendors | Demand Gen | Repeat site visits to product/pricing pages, content downloads |
| **Evaluation** | Ready to talk | Demand Gen → SDR | Form fill, demo request, MQL |
| **Opportunity** | In a sales conversation | Sales | SAL, SQL, open opportunity |

Brand ads can run in the background across all stages — the key is **frequency capping** so someone already in an active sales conversation isn't flooded with top-of-funnel brand ads.

---

## The Two TAM Lists

Brand and demand gen should be working from two different — but related — audience lists:

**Brand TAM (Total Addressable Market)**
The full set of companies that fit your ideal customer profile by firmographics alone: industry, revenue, company size, geography. Brand awareness runs against this broader list.

**Demand Gen TAM**
A subset of the Brand TAM filtered by **behavioral intent signals** — companies that are actively researching relevant topics (via ZoomInfo, Bombora, 6sense, or similar). Demand gen campaigns run against this narrower, hotter list.

The logic: Brand's job is broad reach. Demand gen's job is pipeline for specific products. Spending demand gen budget on companies with no current intent is inefficient. Spending brand budget only on intent-matched accounts leaves future buyers unprimed.

---

## Channel Roles by Stage

### Awareness
| Channel | Role |
|---|---|
| Brand CTV / streaming video | Reach decision-makers at target accounts at home |
| LinkedIn Brand Video | Reach by job title + company at work |
| YouTube / Google Demand Gen | Reach via topic/category interest signals |
| ZoomInfo Display (Brand TAM list) | IP-based display across the full TAM |

> At Awareness, the signal you get back is mostly platform-side (reach, video views). You can't retarget on it yet — you need a click to your own site to get a signal you own.

### Interest
| Channel | Role |
|---|---|
| LinkedIn Sponsored Content | Demand Gen TAM list; product-level content (not brand) |
| ZoomInfo Display (Demand Gen TAM list) | Product-level display to intent-matched accounts |
| Google Demand Gen | Video/image ads on YouTube + Gmail + Discover to warm audience |

> This is where the Brand → Demand Gen handoff happens. Someone who visited your site (via a brand ad click) can now be retargeted by demand gen with product messages.

### Consideration
| Channel | Role |
|---|---|
| LinkedIn retargeting | Video viewers + ad engagers from TOFU, served deeper content |
| Google Display retargeting | Site visitors served case studies, comparison content |
| Meta Ads retargeting | Cost-efficient reach extension for MOFU (lower CPCs than LinkedIn) |
| ZoomInfo Programmatic Display | Account-list display for known target accounts |

### Evaluation
| Channel | Role |
|---|---|
| Google Search (Always On) | Capture active searches: category and problem-based queries |
| LinkedIn Customer Match | CRM list upload — retarget known leads with demo/talk-to-expert CTA |
| Google Customer Match | Same list, served on Search, YouTube, Display |
| Dynamic Remarketing | Show ads based on the specific pages someone visited |

### Opportunity (suppress or shift)
Once a contact becomes an open opportunity, remove them from prospecting audiences. Options:
- Upload the account to exclusion lists in LinkedIn, Google, ZoomInfo
- Or shift to lighter-touch brand-only exposure (frequency capped) to stay visible during the sales process

---

## The Handoff Rules

What triggers a person moving from Brand → Demand Gen handling:

| Trigger | Action |
|---|---|
| Clicks a brand ad to your site | Enters site visitor retargeting pool (demand gen takes over) |
| Watches 25%+ of a brand video | Enters video viewer audience (demand gen can retarget) |
| Downloads content via form | Becomes a known lead; enters MAP nurture + LinkedIn Customer Match |
| Scores to MQL | Routes to SDR queue; exits prospecting audiences |
| Becomes open opportunity | Removed from prospecting; account added to exclusion lists |

---

## What Makes This Work Technically

1. **Tracking pixels on every landing page.** LinkedIn Insight Tag, Google Tag, and any DSP pixel must be live before campaigns launch.

2. **UTM parameters on every ad URL.** Without UTMs, you can't tell which channel drove a site visit. See [UTM Naming Convention](../tracking/utm-naming-convention.md).

3. **Shared account/contact lists between MAP and ad platforms.** Your MAP (Marketo, HubSpot) should sync lead and contact lists to LinkedIn Matched Audiences and Google Customer Match on a regular cadence.

4. **Exclusion lists maintained in real time.** Current customers and open opportunities should be excluded from prospecting campaigns. This requires a live sync from Salesforce to ad platforms, either directly or via MAP.

---

## Common Failure Modes

**Running brand and demand gen as fully separate programs.**
They target the same people. If there's no handoff logic, you're paying twice for the same impressions and getting no cumulative effect.

**No tracked landing pages behind brand ads.**
Brand awareness without click-through tracking means zero retargeting data. Every brand impression that doesn't generate a site visit is a signal lost.

**Retargeting with the same creative.**
Someone who already clicked your ad and read your product page doesn't need to see the same banner again. Segment your retargeting audiences by engagement depth and match the content to where they are.

**Not excluding current customers and open opportunities.**
Spending money showing top-of-funnel ads to someone who's already in a demo stage is a waste and a bad experience.

---

## Related

- [Retargeting Strategy](retargeting-strategy.md) — audience pools and platform-specific setup
- [Channel & Content Guide](channel-and-content-guide.md) — content format matching by funnel stage
- [Campaign Planning Framework](https://github.com/rachelhong-marketing/b2b-campaign-assistant/blob/main/framework/campaign-planning-framework.md) (step 1, B2B Campaign Assistant): how to build the campaign strategy upstream of channel execution
