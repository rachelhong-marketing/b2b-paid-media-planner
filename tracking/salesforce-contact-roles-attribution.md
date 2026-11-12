# Salesforce Contact Roles & Multi-Touch Attribution

This is the most commonly skipped step in B2B marketing attribution — and the reason most marketing teams can't prove their impact on pipeline.

---

## The Problem

B2B deals involve multiple people. The procurement manager, the technical lead, the VP who signs off. Each of them may have engaged with your marketing at different times — downloaded a whitepaper, attended a webinar, clicked a Google ad. All of that activity is recorded in Salesforce as Campaign Members.

But none of it connects to the Opportunity unless you add Contact Roles.

Without Contact Roles, you can see that May attended a webinar and Joe downloaded a report. What you can't see is that May and Joe are both stakeholders on the same deal — and that your marketing touched two out of three decision-makers before it closed.

---

## What Contact Roles Are

A Contact Role is a record that links a Contact to an Opportunity, with a defined role (Decision Maker, Influencer, Technical Buyer, Economic Buyer, Champion, etc.).

This is the bridge between:

```
Campaign Member (person ↔ campaign)
        +
  Contact Role (person ↔ opportunity)
        ↓
Campaign Influence (campaign ↔ opportunity)
```

No Contact Roles = no Campaign Influence = no multi-touch attribution.

---

## How to Add Contact Roles

1. Open an Opportunity in Salesforce
2. Navigate to the **Contact Roles** related list
3. Add each stakeholder involved in the deal
4. Assign a role to each: Decision Maker, Influencer, Technical Buyer, etc.

Once a Contact is linked to an Opportunity via a Contact Role, Salesforce can connect that person's Campaign Member history to the Opportunity — enabling Campaign Influence reporting.

---

## Why Sales Doesn't Do This

In practice, most salespeople don't fill in Contact Roles. The reasons are real:

1. **It's extra work** with no immediate benefit for them.
2. **They don't want to create Opportunities early.** Once an Opportunity is in the system with a pipeline amount, it affects win rate if it doesn't close. Sales reps often delay creating Opportunities until the deal is nearly done — which means all the early-stage marketing touches are never recorded.

This isn't a Salesforce problem. It's a process and incentives problem.

---

## Practical Fixes

### Short-term: Backfill with Automation
If sales hasn't been filling in Contact Roles historically, Sales Ops can configure an automation that assigns a default Contact Role to all Contacts under an Account when an Opportunity is created. This isn't perfect (everyone gets the same role), but it at least creates the connection so Campaign Influence has data to work with.

This is a "clean up the past" fix. It won't reflect actual deal dynamics, but it's better than a complete data gap.

### Long-term: Process + Systems Enforcement
The most effective approaches I've seen:

**1. Gate Opportunity stage progression on data completeness.**
Sales Ops can configure Salesforce validation rules so that an Opportunity can't advance past a certain stage (e.g., Proposal/Price Quote) without a pipeline amount and at least one Contact Role filled in. Sales can't ignore it because the system won't let them proceed.

**2. Report on data quality in pipeline reviews.**
If leadership reviews a weekly pipeline report and missing Contact Roles are highlighted, it creates accountability. What gets measured gets managed.

**3. Sales Ops reporting to Finance, not Sales.**
The most reliable data quality I've seen was at a company where Sales Ops reported into Finance rather than Sales. Finance controlled budget authority, which meant Sales Ops had organizational leverage to enforce data standards. Sales still had to comply with weekly pipeline updates, and system validations were enforced. The data was clean enough to run real attribution reporting.

---

## Campaign Influence: What It Shows Once This Is Set Up

With Contact Roles in place and Campaign Influence enabled, you can run reports that show:

- Every campaign that touched a stakeholder on a given deal
- The total pipeline influenced by a campaign (across all Opportunities where a Campaign Member had a Contact Role)
- Revenue attributed to specific campaign types (webinars, paid social, content syndication)
- Marketing's contribution to pipeline by quarter

**Sample Campaign Influence Report output:**

| Campaign | Influenced Opportunities | Influenced Pipeline | Closed Won Revenue |
|---|---|---|---|
| 2026-Q3 ABM Tech — LinkedIn | 12 | $1.4M | $280K |
| 2026-Q3 Webinar — Oct 15 | 8 | $920K | $150K |
| 2026-Q3 Content Syndication | 5 | $550K | $60K |

This is what you bring to a CMO review or a sales leadership meeting. It answers the question: *what did marketing actually contribute to revenue?*

---

## Attribution Models Available in Salesforce

| Model | Credit distribution | When to use |
|---|---|---|
| First Touch | 100% to the first campaign | Measuring awareness/top-of-funnel impact |
| Last Touch | 100% to the last campaign before Opportunity creation | Default; easiest to implement |
| Even Distribution | Equal credit to all campaigns | Long sales cycles with many touchpoints |
| Custom | You define the weights | When you have strong opinions about which stages matter most |

For most B2B teams, **Even Distribution** or a **custom model** is more accurate than Last Touch for long sales cycles.

---

## Related

- [Salesforce Campaign Hierarchy](salesforce-campaign-hierarchy.md) — structuring campaigns so this data rolls up correctly
- [UTM Naming Convention](utm-naming-convention.md) — connecting ad spend to these Salesforce records
