# Connecting Google Ads to Salesforce: From Click to MQL

By default, Google Ads only sees the form fill. It has no idea which clicks became MQLs, SALs, or opportunities. This means Google's algorithm optimizes for form fills — not lead quality. The result: lower-intent leads, higher cost per MQL, and no visibility into which keywords and ads actually drive pipeline.

This document covers the two-part fix: sharper targeting to reach the right people, and closing the data loop so quality signals flow back to Google.

---

## The Two Levers

### Lever 1: Targeting — who sees your ads

| Feature | What it does | Dependency |
|---|---|---|
| **Customer Match** | Upload a contact email list; Google matches them to signed-in users so you can show ads specifically to people at target accounts | Legal approval (personal emails match better than work emails; raises data handling questions) |
| **Remarketing** | Build an audience of people who visited your site — retarget them on Search, YouTube, and Display | Google Tag installed on your site |
| **Exclusion Lists** | Upload current customers and accounts already in a sales conversation; stop paying for clicks from them | CRM export or MAP sync |
| **In-Market Audiences** | Google's own signal for people actively researching a category | None — available out of the box |
| **Custom Intent** | Build audiences based on specific search queries or URLs people have visited | None — configure in Google Ads |

### Lever 2: Data loop — quality signals back to Google

| Feature | What it does | Dependency |
|---|---|---|
| **GCLID capture** | Save Google's click ID on the form submission, carried into Salesforce | Hidden field on forms + GCLID field on Lead/Contact/Campaign Member in Salesforce |
| **Offline Conversion Import** | Send MQL, SAL, SQL status back to Google Ads matched on the GCLID | GCLID in Salesforce + regular upload (manual CSV or automated API) |
| **Smart Bidding** | Google's automated bidding optimizes for the conversion events you define — once MQL/SAL data flows back, it bids more on clicks that look like qualified leads | Offline conversion import must be live first |

---

## Why GCLID Matters

Google assigns a unique click ID (GCLID) to every ad click. If you capture and store this ID when someone fills out a form, you can later send their MQL or SQL status back to Google — matched on that ID.

Without GCLID:
- Google sees: `click → form fill`
- You see: `lead source = google / paid-search`

With GCLID + Offline Conversion Import:
- Google sees: `click → form fill → MQL (3 weeks later) → SAL (5 weeks later)`
- You see: keyword, ad, and match type tied to actual pipeline outcomes in Salesforce

This is what enables Smart Bidding to optimize for lead quality instead of click volume.

---

## Technical Setup: GCLID in Salesforce

### Step 1: Capture GCLID on the form

Add a hidden field called `GCLID` to your MAP forms (HubSpot, Marketo, Pardot, Eloqua). Configure it to auto-populate from the `gclid` URL parameter on the landing page.

In your Google Ads account: enable **Auto-tagging** (Account Settings → Auto-tagging → Yes). This appends `?gclid=xxxxx` to every ad click URL automatically.

### Step 2: Add GCLID fields in Salesforce

Create custom fields on:
- **Lead** object: `GCLID__c` (Text, 255)
- **Contact** object: `GCLID__c` (Text, 255)
- **Campaign Member** object: `GCLID__c` (Text, 255) — this is the most important one; it ties the click to the specific campaign response

### Step 3: Map the field from your MAP to Salesforce

In HubSpot/Marketo/Pardot: map the GCLID form field to the corresponding Salesforce field. When a lead syncs, the GCLID travels with it.

### Step 4: Offline Conversion Import

Once MQL/SAL data exists in Salesforce with GCLIDs attached, you can upload a conversion file to Google Ads:

```
Google Click ID | Conversion Name | Conversion Time | Conversion Value
Cl1Xy2Z3...     | MQL             | 2026-10-15 09:30:00 | 1
Cl1Xy2Z3...     | SAL             | 2026-11-01 14:00:00 | 1
```

**Note:** Compliance/Legal review is typically required before activating the upload. Recommended approach: add the fields now and start collecting GCLIDs, then activate the upload once approved. You'll have historical data to send when it goes live.

---

## UTM Fields in Salesforce (Related)

GCLID is for the Google data loop. UTM fields are for Salesforce attribution reporting. Both should exist and be populated.

The UTM fields most useful on Campaign Member:
- `utm_source` — platform (google, linkedin, zoominfo)
- `utm_medium` — channel type (paid-search, paid-social, display)
- `utm_campaign` — campaign name
- `utm_content` — ad variant (useful for A/B test tracking)
- `utm_term` — keyword (Google Search: set once as `{keyword}` at account level)

If UTM fields exist in Salesforce but are blank, the most common cause is the MAP not syncing them. Check the form hidden fields, the MAP-Salesforce field mapping, and whether the campaign member sync is running.

See [UTM Naming Convention](utm-naming-convention.md) for the full setup.

---

## What This Unlocks

Once GCLID capture and Offline Conversion Import are live:

**In Google Ads:**
- See MQLs and SALs by keyword, ad group, and campaign
- Enable Smart Bidding targeting MQL conversions instead of form fills
- Identify which keywords bring qualified leads vs. high-volume low-quality leads

**In Salesforce (via Campaign Influence):**
- Join keyword data to Campaign Influence reports
- See which search queries appear across Opportunities
- Over time: build a view of which keywords appear in closed-won deals

**For the broader team:**
- Stop manually matching UTMs to leads from platform exports — the data flows automatically
- Give copywriters and media planners feedback on which ad messages drove MQLs (not just clicks)

---

## Related

- [UTM Naming Convention](utm-naming-convention.md) — the parallel tracking setup for Salesforce attribution
- [Salesforce Campaign Hierarchy](salesforce-campaign-hierarchy.md) — structuring campaigns so this data rolls up correctly
- [Paid Media Test & Learn](../testing/paid-media-test-and-learn.md) — once keyword/ad data reaches Salesforce, how to run structured tests
