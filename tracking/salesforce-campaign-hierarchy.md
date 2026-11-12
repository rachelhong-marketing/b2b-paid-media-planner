# Salesforce Campaign Hierarchy for B2B Paid Media

A well-structured campaign hierarchy in Salesforce is what lets you roll up performance data cleanly — from individual ad sets up to program-level and quarter-level reporting.

---

## Why Campaign Hierarchy Matters

Without hierarchy, every campaign in Salesforce is a flat list. You can see individual campaign performance, but you can't easily answer questions like:

- How much pipeline did our Q3 ABM program generate total?
- Across all channels, how much did our awareness campaigns contribute vs. our decision-stage campaigns?
- How does webinar performance compare to paid social across a whole year?

Hierarchy lets you nest campaigns so parent campaigns aggregate child campaign data automatically.

---

## Recommended Structure

```
Parent Campaign (Program level)
└── Child Campaign (Tactic / Channel level)
    └── Individual Campaign Member records
```

**Example:**

```
2026-Q3 ABM Tech Sector [Parent]
├── 2026-Q3 ABM Tech Sector — LinkedIn Sponsored Content
├── 2026-Q3 ABM Tech Sector — ZoomInfo Programmatic Display
├── 2026-Q3 ABM Tech Sector — Content Syndication (Selling Simplified)
└── 2026-Q3 ABM Tech Sector — Webinar (Oct 15)
```

```
2026-H1 Demand Gen [Parent]
├── 2026-H1 Demand Gen — Google Search
├── 2026-H1 Demand Gen — LinkedIn Lead Gen Forms
└── 2026-H1 Demand Gen — Email Nurture
```

---

## Campaign Fields to Populate

| Field | What to put here |
|---|---|
| Campaign Name | Follow your UTM campaign naming convention for alignment |
| Type | Email / Event / Webinar / Paid Social / Paid Search / Display / Content Syndication |
| Status | Planned / Active / Completed |
| Start Date / End Date | Actual flight dates |
| Budgeted Cost | What you planned to spend |
| Actual Cost | What you actually spent |
| Expected Revenue | Optional — useful for board-level reporting |
| Parent Campaign | Link to the program-level parent |
| Description | Brief note on the goal (e.g., "TOFU awareness for tech sector accounts") |

---

## Lead Source vs. Campaign

A common point of confusion:

| | Lead Source | Campaign |
|---|---|---|
| **What it is** | A field on the Lead/Contact record | A separate object in Salesforce |
| **What it captures** | Where the lead originally came from | Every marketing touchpoint over time |
| **Attribution model** | First touch only | Multi-touch (with Campaign Influence) |
| **Who fills it** | Auto-populated or by sales | You add Campaign Members when a lead engages |

Lead Source is a snapshot. Campaigns are the full story.

---

## Adding Campaign Members

A Campaign Member is what connects a person (Lead or Contact) to a Campaign. This is the step most teams skip — and it's the reason attribution data falls apart.

**When to add a Campaign Member:**
- Someone responds to an email (MAP sync handles this automatically if configured)
- Someone downloads a piece of content via a form
- Someone registers for or attends a webinar
- Someone clicks a paid ad and fills out a form with UTM parameters tracked back to this campaign

**Member Status options (configure per campaign type):**

| Campaign Type | Member Statuses |
|---|---|
| Email | Sent / Opened / Clicked / Responded |
| Webinar | Invited / Registered / Attended / No Show |
| Paid Social | Sent / Responded |
| Event / Trade Show | Invited / Registered / Attended |

The "Responded" status is what Campaign Influence counts as an engaged touchpoint.

---

## Connecting Campaigns to Opportunities

Campaigns connect to Opportunities through two mechanisms:

1. **Primary Campaign Source** (default) — The last campaign a lead engaged with before converting to an Opportunity. Last-touch attribution, automatic.

2. **Campaign Influence** (customizable) — Links an Opportunity to multiple campaigns. Requires enabling Customizable Campaign Influence in Salesforce settings. This is what enables true multi-touch attribution.

For this to work, **Contact Roles must be filled in on the Opportunity.** See [Salesforce Contact Roles & Attribution](salesforce-contact-roles-attribution.md).

---

## Reporting

Once campaigns are structured correctly, the core reports to run:

**Campaign ROI Report**
- Report Type: Campaigns with Campaign Members
- Key fields: Budgeted Cost, Actual Cost, Expected Revenue, Opportunities (from Campaign Influence)
- Summary formula: `(Amount Won - Actual Cost) / Actual Cost`

**Campaign Influence Report**
- Report Type: Campaign Influence
- Shows every campaign associated with Opportunities, the influenced pipeline amount, and revenue
- Filter by: Campaign Type, Date Range, Opportunity Stage

**Pipeline by Program (Parent Campaign)**
- Group by: Parent Campaign
- Shows total influenced pipeline per program, rolling up all child campaigns

---

## Related

- [UTM Naming Convention](utm-naming-convention.md) — align campaign names with UTM parameters
- [Salesforce Contact Roles & Attribution](salesforce-contact-roles-attribution.md) — the missing link between campaigns and opportunities
