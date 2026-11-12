# B2B Retargeting Strategy

Retargeting is what turns a disconnected set of paid channels into a coordinated system. Without it, every channel runs independently and you lose the audience signals you've already paid to build.

---

## Audience Pool Sources

Before you can retarget, you need audiences. These are the four main pool types in B2B paid media:

### 1. Video Ad Viewers
People who watched 25%+ of a video ad. Strong intent signal — they chose to engage.  
**Can activate on:** LinkedIn, YouTube/Google

### 2. Ad Clickers / Post Engagers
People who clicked an ad or engaged with a sponsored post.  
**Can activate on:** LinkedIn, Google Display

### 3. Website Visitors (Pixel-based)
People who visited specific pages — product pages, pricing, resources. Requires a tracking pixel installed in advance.  
**Can activate on:** LinkedIn, Google, ZoomInfo Programmatic Display  
> **Note:** Set up pixels before you need them. A pixel installed after a campaign launches captures no historical data.

### 4. CRM Contact List Upload
Export a lead or contact list from your MAP (Marketo, HubSpot, Pardot) and upload it as a custom audience.  
**Can activate on:** LinkedIn (Matched Audiences), Google (Customer Match), Email Retargeting

---

## Cross-Channel Retargeting Flow

```
TOFU — LinkedIn / ZoomInfo
  └─ Build awareness with video ads, thought leadership posts
  └─ Accumulates: video viewers + ad engagers

      ↓

MOFU — Google Ads + ZoomInfo Display + Meta Ads
  └─ Retarget the TOFU audience with deeper content
     (case studies, buyer's guides, demo invites)
  └─ Also retarget website visitors from pixel
  └─ Accumulates: website visitors, content downloaders

      ↓

BOFU — Google Search + Retargeting
  └─ Capture active searchers at decision stage
  └─ Reinforce brand with retargeting ads to known prospects
```

---

## Platform-Specific Notes

### LinkedIn
- **Matched Audiences:** Upload a contact/account list from your CRM or MAP
- **Video retargeting:** Build a custom audience from people who watched 25%+ of a video ad
- **Lead Gen Form retargeting:** Retarget people who opened but didn't submit a Lead Gen Form
- Minimum audience size: 300 matched members to activate

### Google Ads
- **Customer Match:** Upload a contact email list (requires account in good standing, $50k+ spend history)
- **In-Market Audience:** Google's own signal for buyers researching a category
- **Custom Intent:** Build audiences based on specific search queries or URLs
- **Website Remarketing:** Anyone who visited a specific page, powered by Google Tag
- Minimum audience size: 1,000 for Display, 1,000 for Search

### ZoomInfo Programmatic Display
- Account-level targeting — upload your target account list directly
- Serves display ads to contacts at those companies across the web via DSP
- No minimum list size for account lists (unlike cookie-based retargeting)

### Meta Ads
- Lower CPCs than LinkedIn — good for extending reach at MOFU without blowing budget
- Can integrate with ZoomInfo to upload account lists for account-level targeting
- Custom Audiences from website pixel or CRM list upload
- Minimum audience: 100 people (but 1,000+ recommended for delivery)
- Best used as a complement to LinkedIn, not a replacement for B2B targeting

---

## Common Mistakes

**Not installing pixels early enough.**  
Pixels only capture data going forward. If you launch a campaign and then set up the pixel, you've lost all that audience data. Install LinkedIn Insight Tag and Google Tag on your site before any campaign goes live.

**Using the same creative across all retargeting audiences.**  
A person who watched your video ad is at a different stage than someone who visited your pricing page. Segment your audiences and match the content to their intent level.

**Retargeting too broadly.**  
Not all website visitors are worth retargeting. Someone who bounced from the homepage in 5 seconds is not the same as someone who spent 3 minutes on your product page. Use page-level audience segmentation.

**Forgetting minimum audience sizes.**  
LinkedIn requires 300 matched members before an audience activates. If your list is small, your ads won't run. Combine audiences (video viewers + ad engagers) to hit the threshold.

---

## Related

- [Channel & Content Guide](channel-and-content-guide.md) — which channels to use at each funnel stage
- [UTM Naming Convention](../tracking/utm-naming-convention.md) — how to track retargeting traffic back to Salesforce
