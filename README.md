# B2B Paid Media Planner

A practical reference for B2B marketers on how to plan paid media campaigns, build retargeting audiences, and track marketing's contribution to pipeline in Salesforce.

Built from years of experience running demand gen programs at B2B SaaS and professional services companies.

---

## What's Inside

### Campaign Planning
| Doc | What it covers |
|---|---|
| [Campaign Planning Framework](campaign-planning/campaign-planning-framework.md) | Input-gathering process, what makes a good B2B campaign theme, ABM considerations, shared brainstorm structure |

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
| [UTM Tracker Template](templates/utm-tracker-template.csv) | Copy-paste template for tracking all paid links in one place |

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

## Connect

[LinkedIn](https://www.linkedin.com/in/rachelhongatbaruch/) · [Accelerator Consulting](https://acceleratorsconsulting.com)
