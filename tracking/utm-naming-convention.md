# UTM Naming Convention for B2B Paid Campaigns

UTM parameters are how you connect paid ad spend to Salesforce pipeline. Without consistent naming, traffic shows up as direct or organic in your analytics and you can't tell which campaigns drove form fills.

---

## The Five Parameters

| Parameter | What it tracks | B2B examples |
|---|---|---|
| `utm_source` | The platform the ad ran on | `linkedin`, `google`, `zoominfo`, `selling-simplified`, `meta` |
| `utm_medium` | The channel type | `paid-social`, `paid-search`, `display`, `content-syndication`, `sponsored-email` |
| `utm_campaign` | The campaign name | `2026-q3-abm-launch`, `2026-h1-brand-awareness` |
| `utm_content` | The specific ad or creative | `video-ad-cfo`, `whitepaper-cta-banner` |
| `utm_term` | Keyword (Google Search only) | `marketing-attribution-software` |

---

## Naming Format

Use lowercase, hyphens only (no spaces, no underscores, no special characters).

**Campaign naming convention:**

```
{year}-{quarter or half}-{program}-{asset}
```

**Examples:**
```
utm_campaign=2026-q3-abm-tech-sector
utm_campaign=2026-h1-demand-gen-whitepaper
utm_campaign=2026-q4-retargeting-demo
```

---

## Full URL Examples

**LinkedIn sponsored content:**
```
https://yoursite.com/whitepaper
  ?utm_source=linkedin
  &utm_medium=paid-social
  &utm_campaign=2026-q3-abm-tech-sector
  &utm_content=whitepaper-banner-cto
```

**Google Search:**
```
https://yoursite.com/product
  ?utm_source=google
  &utm_medium=paid-search
  &utm_campaign=2026-q3-brand
  &utm_term=b2b-marketing-attribution
```

**ZoomInfo Programmatic Display:**
```
https://yoursite.com/product
  ?utm_source=zoominfo
  &utm_medium=display
  &utm_campaign=2026-q3-abm-tech-sector
  &utm_content=product-banner-300x250
```

**Content Syndication (Selling Simplified):**
```
https://yoursite.com/whitepaper-landing
  ?utm_source=selling-simplified
  &utm_medium=content-syndication
  &utm_campaign=2026-q3-whitepaper-tech
```

---

## Rules for the Whole Team

1. **Every paid link gets UTM parameters.** No exceptions. An untagged link means that session shows as direct traffic.
2. **Use the shared naming list.** Don't invent new `utm_source` values on the fly. Maintain a master list (see [utm-tracker-template.csv](../templates/utm-tracker-template.csv)) so reports can aggregate by channel correctly.
3. **Case sensitive.** `LinkedIn` and `linkedin` are treated as two different sources in analytics. Stick to lowercase.
4. **Store parameters in a shared sheet.** Every campaign URL should be logged before it goes live. This makes campaign audits and Salesforce reporting significantly easier.

---

## How UTMs Flow Into Salesforce

When a lead fills out a form on your site:

```
Ad click (with UTM)
  → Landing page (HubSpot / Marketo form with hidden fields)
  → UTM values captured in hidden fields
  → Synced to Salesforce as custom fields on the Lead/Contact
  → Visible in Salesforce as: UTM Source, UTM Medium, UTM Campaign
```

This requires:
- Hidden fields set up in your MAP (HubSpot, Marketo, Pardot)
- Custom UTM fields created in Salesforce on the Lead and/or Contact object
- Field mapping configured between MAP and Salesforce

For more on setting up Salesforce to capture this data, see [Salesforce Campaign Hierarchy](salesforce-campaign-hierarchy.md).

---

## Related

- [Salesforce Campaign Hierarchy](salesforce-campaign-hierarchy.md)
- [Salesforce Contact Roles & Attribution](salesforce-contact-roles-attribution.md)
- [UTM Tracker Template](../templates/utm-tracker-template.csv)
