# Meta Ads Setup Skill
## Campaign Structure
- Campaign → Ad Set → Ad (always 3 levels)
- Never mix objectives within a campaign
- Naming convention: [Client]-[Campaign Type]-[Date]-[Objective]

## Objective Selection
- Service business booking: Leads (Instant Form)
- Website with pixel + 50 events: Conversions
- New account or awareness: Reach or Traffic
- Retargeting warm audience: Traffic or Engagement

## Pixel Setup Checklist
- [ ] Pixel installed on all pages
- [ ] Standard events firing: PageView, Lead, Purchase
- [ ] Test Events tool confirms pixel is receiving data
- [ ] Conversions API (CAPI) set up for iOS14+ tracking
- [ ] Custom conversion created for booking confirmation page

## Instant Form Best Practices
- Higher Intent: adds review screen before submit (better quality)
- More Volume: removes review screen (more leads, lower quality)
- Context card headline: match the ad hook exactly
- Questions: maximum 3, never ask for info Meta already has
- Thank you screen: tell them exactly what happens next
- CASL compliance: add consent language for Canadian campaigns

## Ad Set Configuration
- Budget: set at ad set level (not campaign) for easier control
- Schedule: run all times unless data shows clear off-peak hours
- Bid strategy: Lowest cost (default) until you have conversion data
- Placements: Advantage+ placements (let Meta optimize)
- Audience: start broad, let Meta find converters

## Learning Phase Rules
- Minimum $15 CAD/day to enter learning phase
- Need 50 optimization events in 7 days to exit learning
- DO NOT edit during learning phase (resets the algorithm)
- Limited Learning = not enough data — increase budget or broaden audience
- Learning phase complete = green light to scale

## Common Mistakes That Waste Budget
- Wrong objective (Traffic when you want Leads)
- No pixel installed before spending
- Too many ad sets splitting budget (consolidate)
- Editing campaigns during learning phase
- Targeting too narrow (audience under 100K)
- Using post engagement as proxy for leads
- Not installing CAPI alongside pixel

## A/B Testing Order
1. Test hooks first (same audience, same offer, different hook)
2. Then test audiences (same hook, different targeting)
3. Then test creative format (image vs video vs carousel)
4. Never test more than one variable at a time

## Campaign Naming Convention (Baseleap standard)
[Business]-[CampaignType]-[YYYY-MM]-[Objective]
Example: StayRadiant-SummerPromo-2026-06-Leads
