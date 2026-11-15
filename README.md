# B2B Paid Media Planner

> **B2B Campaign Lifecycle Toolkit**, step 2 of 5
>
> [1. Plan](https://github.com/rachelhong-marketing/b2b-campaign-assistant) → **2. Set up** → [3. Test](https://github.com/rachelhong-marketing/b2b-campaign-test-planner) → [4. Report](https://github.com/rachelhong-marketing/b2b-campaign-reporting-agent) → [5. Prove](https://github.com/rachelhong-marketing/b2b-pipeline-attribution-tool)

A practical reference for B2B marketers on how to plan paid media campaigns, build retargeting audiences, and track marketing's contribution to pipeline in Salesforce. It includes a **launch checker** that builds tracking links and catches tracking mistakes before the ads go live.

Built from years of experience running demand gen programs at B2B SaaS and professional services companies.

---

## Launch checker: catch tracking mistakes before launch

Most attribution problems start on launch day: a capital letter in `utm_source`, two test versions with the same `utm_content`, a link copied from the wrong row, or a Salesforce campaign nobody created. Once the ads run, those leads can't be traced back. The launch checker catches these before launch, using the rules in [UTM Naming Convention](tracking/utm-naming-convention.md) and [Salesforce Campaign Hierarchy](tracking/salesforce-campaign-hierarchy.md).

### With Claude Code (no commands to type)

The repo includes a Claude Code skill, `.claude/skills/paid-media-launch-checker/SKILL.md`. Download the repo, open the folder in Claude Code, and ask:

- "Build links for our Q3 LinkedIn campaign: 3 video ads for CFOs, landing page yoursite.com/guide."
- "Check sample-data/utm-tracker-sample.csv against the Salesforce campaigns before we launch."
- "Which sources and mediums are we allowed to use?"

It builds or checks the links, explains every problem in plain English with the fix, and can save a cleaned-up copy of the tracker. The rules come from the Python code, not the AI.

### From the command line

Python 3 only, nothing to install.

```bash
python3 -m launch_checker build --url https://yoursite.com/guide --source linkedin --medium paid-social \
  --campaign 2026-q3-abm-tech-sector --content video-cfo
python3 -m launch_checker check sample-data/utm-tracker-sample.csv --salesforce sample-data/salesforce-campaigns-sample.csv
python3 -m launch_checker check my-tracker.csv --fixed my-tracker-fixed.csv
python3 -m launch_checker rules
python3 -m unittest discover -s tests
```

### What it checks

| Check | Example it catches | Level |
|---|---|---|
| Format | `LinkedIn` or `Carousel CMO` instead of `linkedin`, `carousel-cmo` | Fix before launch |
| Shared source list | `linkdin` (suggests `linkedin`) | Fix before launch |
| Source and medium pair | `linkedin` with `paid-search` | Fix before launch |
| Link matches its columns | The tagged link says `banner-728x90`, the tracker says `banner-300x250` | Fix before launch |
| One `utm_content` per ad | Test versions A and B both tagged `video-cfo-a` | Fix before launch |
| Landing page | `http://`, a stray space, or UTMs already in the page URL | Fix before launch |
| Salesforce campaign exists | No campaign for the Bing Search row, so its leads won't be credited | Fix before launch |
| Campaign name format | `q4-retargeting` instead of `2026-q4-retargeting` | Warning |
| Campaign period vs. launch date | Named `2026-q3` but launches in October | Warning |
| `utm_content` on social and display | A display ad with no `utm_content` | Warning |
| `utm_term` only on search | A keyword on a Meta ad | Warning |
| Salesforce parent and type | No parent campaign, or type "Paid Social" on a display campaign | Warning |
| GCLID reminder | Google Search links: turn on auto-tagging and capture the GCLID | Note |

On the made-up sample tracker, 7 of 14 links are ready to launch. The other 7 each have a planted mistake. `--fixed` cleans up format and rebuilds every link from its columns. It leaves wrong sources, mediums and duplicate content for a person to decide.

Allowed sources and mediums live in [`rules/sources.csv`](rules/sources.csv). Add your own partners there.

All sample data in [`sample-data/`](sample-data/) is made up.

---

## What's Inside

Campaign planning (the theme, the campaign plan and the master brief) happens before this step, in [step 1, the B2B Campaign Assistant](https://github.com/rachelhong-marketing/b2b-campaign-assistant). Its [Campaign Planning Framework](https://github.com/rachelhong-marketing/b2b-campaign-assistant/blob/main/framework/campaign-planning-framework.md) covers input gathering, what makes a good B2B campaign theme, ABM considerations and the shared brainstorm.

### Paid Media Channels & Retargeting
| Doc | What it covers |
|---|---|
| [Channel & Content Guide](retargeting/channel-and-content-guide.md) | Channel selection by funnel stage, content format matching, targeting logic per platform |
| [Retargeting Strategy](retargeting/retargeting-strategy.md) | How to build audience pools across LinkedIn, Google, ZoomInfo Display, and Meta Ads — platform minimums, common mistakes |
| [Brand + Demand Channel Waterfall](retargeting/brand-demand-channel-waterfall.md) | How brand awareness and demand gen channels should hand off audiences across the full buyer journey |

### Tracking & Attribution
| Doc | What it covers |
|---|---|
| [UTM Naming Convention](tracking/utm-naming-convention.md) | Standard naming structure for paid campaigns, with full URL examples and Salesforce flow |
| [Google Ads → Salesforce](tracking/google-ads-to-salesforce.md) | GCLID capture, Offline Conversion Import, Smart Bidding setup — closing the loop from click to MQL |
| [Salesforce Campaign Hierarchy](tracking/salesforce-campaign-hierarchy.md) | Parent/child campaign structure, campaign fields, connecting campaigns to opportunities |
| [Salesforce Contact Roles & Attribution](tracking/salesforce-contact-roles-attribution.md) | Why Contact Roles are the missing link in B2B attribution, and how to get sales to fill them in |

### Testing
| Doc | What it covers |
|---|---|
| [Paid Media Test & Learn](testing/paid-media-test-and-learn.md) | A/B testing framework for B2B volumes — feasibility checks, hypothesis writing, calling winners, Learning Library |

### Templates
| File | What it covers |
|---|---|
| [UTM Tracker Template](templates/utm-tracker-template.csv) | Copy-paste template for tracking all paid links in one place (the launch checker reads this format) |
| [Allowed sources and mediums](rules/sources.csv) | The shared source list the launch checker enforces; add your own partners |

---

## Who This Is For

B2B demand gen managers, marketing ops practitioners, and anyone who needs to show marketing's impact on pipeline — not just impressions and clicks.

---

## Context

B2B paid media has fundamentally different logic from B2C. You can't just apply the same playbook. The channels are different (LinkedIn, ZoomInfo, content syndication), the targeting is different (account-level, job title, intent), and the measurement is different (Salesforce pipeline, not last-click ROAS).

This repo captures the frameworks and processes I've used across B2B organizations to:
- Match the right paid channels to each stage of the funnel
- Build retargeting audiences that actually carry intent signals
- Set up UTM tracking that maps back to Salesforce campaigns
- Use Contact Roles and Campaign Influence to attribute pipeline to marketing

---

## Quick Reference: Channel × Funnel Stage

| Channel | Best for | Targeting strength |
|---|---|---|
| LinkedIn Ads | TOFU + MOFU | Job title, company, industry, company size — best for ABM |
| Google Ads | MOFU + BOFU | Search intent, In-Market Audience, Custom Intent |
| ZoomInfo Programmatic Display | MOFU | Account-level — target your exact account list |
| Meta Ads | MOFU retargeting | Large audience pool, low CPC — good LinkedIn complement |
| Content Syndication | TOFU | Rented audience via vendors (Selling Simplified, Intensify) |
| Industry Association / Webinar | TOFU → MOFU | Third-party trust — reaches audiences you can't target directly |

---

## The B2B Campaign Lifecycle Toolkit

Five tools, one per step of a B2B campaign, from the brief to proving pipeline. Each works on its own; together they cover the whole cycle. All sample data is made up.

| Step | Tool | What it does |
|---|---|---|
| 1. Plan | [B2B Campaign Assistant](https://github.com/rachelhong-marketing/b2b-campaign-assistant) | Brainstorm the campaign theme, write the campaign plan and master brief, then draft channel briefs, keywords, landing page and ad copy, all checked before launch. |
| 2. Set up | **B2B Paid Media Planner** (this repo) | Plan channels and retargeting, then build and check tracking links before launch. |
| 3. Test | [B2B Campaign Test Planner](https://github.com/rachelhong-marketing/b2b-campaign-test-planner) | Size tests on leads and MQLs, not clicks, and read the results. |
| 4. Report | [B2B Campaign Reporting Agent](https://github.com/rachelhong-marketing/b2b-campaign-reporting-agent) | Consolidate ad platform and CRM data into one file, check every channel and funnel stage for gaps, and draft insights. |
| 5. Prove | [B2B Pipeline Attribution Tool](https://github.com/rachelhong-marketing/b2b-pipeline-attribution-tool) | Check the CRM data can be trusted, then show sourced and influenced pipeline. |

---

## Connect

[LinkedIn](https://www.linkedin.com/in/rachelhongatbaruch/) · [Accelerator Consulting](https://acceleratorsconsulting.com)
