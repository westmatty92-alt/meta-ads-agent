---
name: ad-strategy
description: Baseleap Meta Ads strategy frameworks — business maturity decision tree, close rate mapping, social proof hierarchy, budget allocation, objection handling, Canadian market specifics, service vs product logic, and campaign type selection.
license: proprietary
metadata:
  author: Baseleap (derived from Baseleap discovery questionnaire + live client data)
---

# Baseleap Ad Strategy Skill

## When to Use This Skill

Invoke before writing any ad, campaign brief, or budget recommendation.
These frameworks answer the strategic questions BEFORE the creative work begins.
If you skip strategy, you write great copy for the wrong objective.

Load this skill when:
- Selecting campaign type or objective
- Writing budget recommendations
- Choosing social proof to feature
- Handling objections in ad copy
- Assessing whether a client is ready to run ads
- Adapting messaging for a Canadian suburban market
- Deciding between lead gen and direct conversion

---

## 1. Business Maturity Decision Tree

Determines the right ad strategy based on where the business is in its lifecycle.
Assess before recommending any campaign structure.

```
START: How long has the business been operating?

├── STAGE 1 — NEW (0–12 months)
│   Symptoms: < 20 reviews, no ad history, unproven offer
│   ├── Priority: Proof generation, not volume
│   ├── Campaign type: Lead Gen (Instant Form — More Volume)
│   ├── Budget floor: $15/day minimum, $30/day recommended
│   ├── Creative strategy: Founder story + first-mover offer
│   ├── Offer type: Introductory discount or free consultation
│   ├── Audience: Broad + interest stack (no lookalikes yet)
│   └── Success metric: First 10 paying clients → case studies
│
├── STAGE 2 — GROWING (1–3 years)
│   Symptoms: 20-100 reviews, some ad history, consistent close rate
│   ├── Priority: Lead volume + cost per lead reduction
│   ├── Campaign type: Lead Gen (Instant Form — Higher Intent)
│   ├── Budget floor: $30/day, scaling to $60-100/day
│   ├── Creative strategy: Results + social proof + limited availability
│   ├── Offer type: Seasonal promotion or package bundle
│   ├── Audience: Interest stack + 1% lookalike from customer list
│   └── Success metric: Cost per booking under $100 CAD
│
└── STAGE 3 — ESTABLISHED (3+ years)
    Symptoms: 100+ reviews, strong close rate, existing ad account data
    ├── Priority: Scale + retention + referral acquisition
    ├── Campaign type: Leads + Retargeting + Lookalike
    ├── Budget floor: $100/day with layered campaign structure
    ├── Creative strategy: Authority + transformation + community
    ├── Offer type: VIP program, referral incentive, loyalty
    ├── Audience: Lookalike 1-3%, retargeting, customer email list
    └── Success metric: Cost per booking under $60 CAD, ROAS > 3x
```

**Key signals to detect business stage from S state:**
- `S.brandSnapshot.years_in_business` or infer from review count
- `S.competitorAds.length` → if 0, first-mover → lean into Stage 1/2 language
- Review count in `S.serpIntelligence.reviewSnippets` → proxy for market maturity

---

## 2. Close Rate Strategy Mapping

Close rate = % of qualified leads that convert to paying clients.
**Ask the client: "If 10 leads come in, how many become clients?"**
This single number determines where the bottleneck is.

```
CLOSE RATE → DIAGNOSIS → AD STRATEGY

< 20%  │ OFFER OR POSITIONING PROBLEM
       │ Ads are attracting the wrong people OR offer is unclear
       │ → Tighten ICP in targeting (age, interests, exclusions)
       │ → Use Higher Intent Instant Form to pre-qualify
       │ → Add qualification question to form (e.g. "What's your budget?")
       │ → Reduce ad spend until offer is fixed
       │ → Focus ad copy on WHO this is NOT for (qualify by exclusion)

20–40% │ NORMAL — OPTIMIZE FOR VOLUME
       │ Pipeline is healthy, scale cautiously
       │ → A/B test hooks to increase lead quality
       │ → Add retargeting sequence for non-closers
       │ → Test More Volume vs Higher Intent form types
       │ → Target: $50-80 CAD cost per lead
       │ → Scale when CPL stable for 7 consecutive days

40–60% │ STRONG — SCALE AGGRESSIVELY
       │ Product-market fit confirmed
       │ → Increase daily budget by 20% every 3 days
       │ → Expand to lookalike audiences (2-5%)
       │ → Test video creatives for lower CPM
       │ → Build retargeting campaign for abandoned leads
       │ → Target: $30-50 CAD cost per lead

> 60%  │ VOLUME PROBLEM — MAXIMIZE REACH
       │ Sales process works perfectly; need more leads
       │ → Maximize budget within CAC tolerance
       │ → Broad targeting + Meta's Advantage+ audience
       │ → Multiple creative angles simultaneously
       │ → Run awareness + lead gen in parallel
       │ → Target: < $30 CAD cost per lead
```

**Close rate questions to surface in ad copy:**
- Low close rate: Copy should filter (address objections upfront, state the price, show the process)
- High close rate: Copy should attract volume (broad appeal, low friction, easy CTA)

---

## 3. Social Proof Hierarchy

Use the highest available tier. Never skip social proof — it is the #1 CTR driver in Canadian service business ads.
Match proof type to business stage.

```
TIER 1 — TRANSFORMATION STORY (highest converting)
  Format: "[Client name], [location], [specific result in X days/sessions]"
  Example: "Sarah from St. Catharines got her smile back in one session"
  Use when: You have a named client willing to be featured
  Placement: Primary text line 1 OR headline
  Note: Specific numbers (4 sessions, 6 weeks, $X saved) outperform vague claims by 3-5x

TIER 2 — QUANTIFIED REVIEW SNIPPET
  Format: "★★★★★ '[exact quote from real review]' — [first name, city]"
  Example: "★★★★★ 'My teeth are 8 shades whiter and it took 45 minutes' — Jessica, Niagara"
  Use when: You have 10+ Google reviews with specific language
  Placement: Primary text (after hook), or overlay text on image
  Note: Pull from S.serpIntelligence.reviewSnippets for real client language

TIER 3 — AGGREGATE CREDIBILITY
  Format: "[Number] [city] [clients/patients/sessions] since [year]"
  Example: "500+ St. Catharines clients trust us with their smile"
  Use when: Client has clear volume but no standout testimonials
  Placement: Primary text bridge OR subtext
  Note: Hyper-local numbers outperform national claims for local service businesses

TIER 4 — COMPETITOR POSITIONING (no proof required)
  Format: "The only [service] in [city] that [specific differentiator]"
  Example: "The only mobile whitening service in Niagara — we come to you"
  Use when: No strong reviews yet OR first-mover in market
  Placement: Hook or headline
  Note: Use when S.competitorAds.length === 0 — own the first-mover position

TIER 5 — CREDENTIAL / CERTIFICATION
  Format: "[Credential] approved | [N] years certified | [Association] member"
  Use when: Regulated industry (dental, medical, financial)
  Placement: Visual overlay or CTA description
  Note: Canadian audiences trust professional credentials — especially in Ontario

TIER 6 — RECENCY SIGNAL (minimum viable proof)
  Format: "[N] [clients/sessions] this month" or "Booking [month] now"
  Use when: No other proof is available
  Placement: CTA or urgency line
  Note: Scarcity + recency > generic social proof when inventory is truly limited
```

**Proof extraction logic from S state:**
1. Check `S.serpIntelligence.reviewSnippets` for real customer language
2. Check `S.brandSnapshot.social_proof` or `S.brandSnapshot.testimonials`
3. Check `S.brandSnapshot.client_count` or `S.brandSnapshot.years_in_business`
4. Fall back to Tier 4 (competitor positioning) if nothing is available

---

## 4. Budget Allocation by Stage

All figures in CAD. All phases assume Meta Ads (Facebook + Instagram).
The $15/day floor is non-negotiable — below this Meta cannot exit the learning phase.

### Phase Structure (apply to every campaign)

```
MONTHLY BUDGET → DAILY BUDGET → PHASE SPLIT

< $450/month  │ ⚠️ WARNING — below learning phase minimum
              │ → Advise client to wait or increase budget
              │ → If must run: single ad set, single creative, 30-day test

$450–900/mo   │ $15–30/day
($15–30/day)  │ PHASE 1 — Test (100% of budget)
              │   • 1 campaign, 1 ad set, 2 creatives (short vs medium copy)
              │   • No retargeting yet (audience too small)
              │   • Stop hook A if CTR < 0.8% after 2,000 impressions
              │   • Scale trigger: CPL under $80 for 5 consecutive days

$900–2,100/mo │ $30–70/day
($30–70/day)  │ PHASE 1 — Test (60%): $18–42/day
              │   • 2 ad sets (2 interest audiences or 1 interest + broad)
              │   • 3 creatives per ad set
              │ PHASE 2 — Scale (30%): $9–21/day
              │   • Winner from Phase 1 only
              │   • Increase budget 20% every 3 days if CPL stable
              │ PHASE 3 — Retarget (10%): $3–7/day
              │   • Website visitors + lead form openers (last 30 days)
              │   • Same creative as winner, add urgency CTA

$2,100–4,500/mo│ $70–150/day
($70–150/day) │ PHASE 1 — Test (40%): $28–60/day
              │   • 3 ad sets: 2 interest + 1 broad
              │   • 3-4 creatives per ad set, video preferred
              │ PHASE 2 — Scale (40%): $28–60/day
              │   • Top 1-2 performers from Phase 1
              │   • Expand to 1% lookalike from lead list
              │ PHASE 3 — Retarget (20%): $14–30/day
              │   • 2 retargeting ad sets (30-day + 90-day window)
              │   • Softer CTA (e.g. "Learn More" vs "Book Now")

> $4,500/mo   │ $150+/day
              │ Full funnel: Awareness (20%) + Lead Gen (50%) + Retarget (30%)
              │ → Introduce video for awareness
              │ → Lookalike 1%, 2%, 3% as separate ad sets
              │ → Dedicated retargeting creative (not repurposed lead gen)
```

### Canadian Meta Benchmarks (2026 — Beauty/Wellness)

| Metric               | Low        | Average    | Strong     |
|----------------------|------------|------------|------------|
| CPM                  | $8 CAD     | $11 CAD    | $15 CAD    |
| CPC (link)           | $0.80 CAD  | $1.15 CAD  | $1.50 CAD  |
| CTR (all)            | 0.8%       | 1.5%       | 2.5%+      |
| Lead form CVR        | 3%         | 5%         | 8%+        |
| Cost per lead        | $25 CAD    | $50 CAD    | $80 CAD    |
| Cost per booking     | $60 CAD    | $120 CAD   | $200 CAD   |

**Kill rules (apply every 48-72 hours during testing):**
- CTR < 0.8% after 500 impressions → pause creative
- CPA > 3x target for 3 consecutive days → pause ad set
- Frequency > 3.0 → warning; > 3.5 → rotate creative immediately
- CPM > $20 CAD → audience is too narrow, broaden or switch

**Scale triggers:**
- CPL stable (< 10% variance) for 5 consecutive days → +20% budget
- CTR > 2.5% for 3 days → duplicate ad set at 2x budget
- Cost per booking < $80 CAD → scale aggressively

---

## 5. Objection Mapping Framework

Every objection that kills a sale must be pre-handled IN the ad or Instant Form, not left for the sales call.
Map the objection to the ad element that kills it.

```
OBJECTION              │ ROOT CAUSE          │ AD ELEMENT TO FIX
───────────────────────┼─────────────────────┼────────────────────────────────
"Too expensive"        │ Value unclear        │ Anchor with transformation cost
                       │                     │ "Less than a set of veneers"
                       │                     │ Show ROI: confidence = opportunity
                       │                     │ Payment plan mention in subtext

"Does it actually      │ Trust deficit        │ Tier 1-2 social proof in hook
work for me?"          │                     │ Before/after with specific result
                       │                     │ "X shade whiter in X minutes"
                       │                     │ Avoid vague: "amazing results"

"I'm not ready yet"    │ Urgency absent       │ Real scarcity (spots, dates)
                       │                     │ "June slots filling — 3 left"
                       │                     │ Seasonal hook (summer, wedding)
                       │                     │ Never fake urgency — it kills trust

"I need to think       │ Decision friction    │ Retargeting sequence (3-touch)
about it"              │                     │ Touch 1: Social proof ad
                       │                     │ Touch 2: FAQ / process explainer
                       │                     │ Touch 3: Limited offer + deadline

"Can I trust them?"    │ Credibility gap      │ Local city name in ad copy
                       │                     │ Google review count + stars
                       │                     │ Credentials / certification
                       │                     │ Founder photo (not stock)

"I'll just do it       │ Convenience gap      │ Lead with the convenience angle
myself"                │                     │ "Why [DIY method] gives uneven..."
                       │                     │ Time saved + professional result

"I found cheaper"      │ Commodity risk       │ Own the quality positioning
                       │                     │ Differentiate on experience/result
                       │                     │ Never compete on price in the ad
                       │                     │ "Not all [services] are equal"
```

**Objection detection from S state:**
- `S.objection` → primary objection client identified
- `S.serpIntelligence.peopleAlsoAsk` → real questions = real objections
- `S.serpIntelligence.reviewSnippets` → negative sentiment = unresolved objections
- `S.competitorAds` → what competitors promise = what customers expect

**Objection hierarchy for ad copy:**
1. Handle the #1 objection in the primary text (not the hook)
2. Handle the #2 objection in the Instant Form intro screen
3. Handle the #3 objection in the form thank-you screen

---

## 6. Canadian Market Specifics

### Voice and Tone
Canadian audiences respond to warmth, honesty, and local specificity.
They are skeptical of American-style aggressive sales language.

```
CANADIAN WORKS                    │ AVOID IN CANADA
──────────────────────────────────┼────────────────────────────────
"Trusted by 200 St. Catharines…" │ "BEST IN THE WORLD!!!"
"Honest pricing, no surprises"   │ "LIMITED TIME ONLY — ACT NOW"
"Come see us in [neighbourhood]" │ Generic national claims
Warm founder photo (real person) │ Stock photo models
Conversational, not corporate    │ Pushy, aggressive urgency
Community feel, local roots      │ Corporate / enterprise tone
"Book a free chat" vs "Buy now"  │ Hard sell on first touch
```

### Seasonal Patterns (Ontario)

| Season          | Peak Events                        | Ad Angle
|-----------------|------------------------------------|-----------------------------------------
| Jan–Feb         | New Year, Valentine's Day          | Fresh start, gift for partner
| Mar–Apr         | Spring refresh, Easter             | New look, seasonal reset
| May–Jun         | Wedding season, prom, graduations  | Special occasion, confidence
| Jul–Aug         | Summer, vacation, social events    | Summer-ready, visible confidence
| Sep–Oct         | Back to routine, fall events       | Self-care reset, routine
| Nov–Dec         | Holiday season, gift cards         | Gift an experience, year-end treat

### Regional Calibration (Ontario Suburbs — e.g. Niagara, Halton, Durham)

- Radius: 15–30km is the sweet spot for local service businesses
- Population: Mid-market, value-conscious, community-oriented
- Price sensitivity: Higher than Toronto core, lower than rural
- Ad creative: Real local environments beat polished studio shoots
- Copy tone: Friendly neighbour, not luxury brand
- CTA preference: "Book a chat" or "Claim your spot" over "Buy Now"

### Canadian Compliance

- **CASL**: Collecting emails via Instant Form requires express consent language
  → Add to form intro: "By submitting, you agree to receive follow-up from [Business]"
- **Pricing**: Show CAD explicitly — "$179 CAD" not just "$179"
- **HST**: Never build tax surprises into the sales process; address in ad if price-sensitive
- **Privacy**: Do not promise data security in ad copy (PIPEDA risk if breached)
- **Regulated services**: Dental/medical claims require evidence — no "whitens 10 shades" without proof

---

## 7. Service Business vs Product Business Logic

The entire campaign structure changes based on whether you are selling a service or a product.
Detect from `S.brandSnapshot.industry` or `S.goal`.

### Service Business (e.g. Stay Radiant, salons, coaching, clinics)

```
PRIMARY OBJECTIVE:   Leads → Bookings (not purchases)
META OBJECTIVE:      Leads (Instant Form) or Traffic (to booking page)
CREATIVE STRATEGY:   Sell the transformation, not the transaction
HOOK STRUCTURE:      Lead with the OUTCOME, not the service
CTA:                 "Book your [service]" / "Claim your spot" / "Get started"
FORM TYPE:           Higher Intent (pre-qualifies, reduces no-shows)
CLOSE RATE FOCUS:    Track lead-to-booking AND booking-to-show rate
RETARGETING:         3-5 day window (decision made quickly for services)
PRICE IN AD:         Yes — filters out non-buyers, improves lead quality
AUDIENCE SIZE:       Smaller (local radius 15-30km), needs refresh at 3.0 frequency
PROOF TYPE:          Tier 1-2 (transformation stories, named local clients)
SEASONAL RISK:       High — service businesses have strong seasonal patterns
UPSELL:              Cross-service packages, maintenance programs, gift cards
LIFETIME VALUE:      High — optimize for repeat clients, not single transactions
```

### Product Business (e-commerce, retail, supplements)

```
PRIMARY OBJECTIVE:   Purchases (direct conversion)
META OBJECTIVE:      Conversions (Add to Cart or Purchase event)
CREATIVE STRATEGY:   Sell the product + the identity it creates
HOOK STRUCTURE:      Lead with the PROBLEM the product solves
CTA:                 "Shop now" / "Get yours" / "Try it free"
FORM TYPE:           Not applicable — send to landing page or product page
CLOSE RATE FOCUS:    Add-to-cart rate, checkout completion rate, ROAS
RETARGETING:         7-14 day window (longer consideration for products)
PRICE IN AD:         Optional — test with/without; lower ASP products benefit from hiding price
AUDIENCE SIZE:       Larger (province/national), more scale available
PROOF TYPE:          Tier 2-3 (review count, rating, aggregate numbers)
SEASONAL RISK:       Medium — tied to e-commerce seasons (BFCM, Christmas)
UPSELL:              Bundles, subscriptions, complementary products
LIFETIME VALUE:      Depends on repeat purchase rate — optimize for LTV not ROAS
```

### Mixed Model (service + retail product)

When a business sells both (e.g. teeth whitening service + take-home kit):
- Run separate campaigns per revenue stream
- Never mix service and product in the same ad — confuses the algorithm
- Product campaign: Conversions objective, broad audience
- Service campaign: Leads objective, local radius

---

## 8. Campaign Type Selection Framework

Match the client's goal this month to the correct Meta campaign type.
The campaign type drives the entire creative brief and copy angle.

```
CLIENT SITUATION               │ CAMPAIGN TYPE          │ META OBJECTIVE
───────────────────────────────┼────────────────────────┼──────────────────────
Wants new clients (no offer)   │ New Client Acquisition │ Leads (Instant Form)
Running a sale or discount     │ Promotion / Special    │ Leads or Traffic
Seasonal event (wedding, etc.) │ Seasonal               │ Leads or Traffic
Has existing leads to re-engage│ Retargeting            │ Engagement or Traffic
Wants to grow brand awareness  │ Awareness              │ Reach or Video Views
Has product to sell directly   │ E-commerce             │ Conversions (Purchase)
Wants phone calls              │ Call Generation        │ Calls (click-to-call)
Launching a new service        │ Launch                 │ Leads + Reach split
```

### New Client Acquisition (most common for Baseleap clients)

```
Objective: Generate qualified leads via Instant Form
Form type: Higher Intent (reduces no-shows by ~40%)
Form questions (max 3, never more):
  Q1: "Which service are you most interested in?" (multiple choice)
  Q2: "When are you looking to book?" (multiple choice: this week / this month / just browsing)
  Q3: "What's your main goal?" (open text — captures language for future copy)
Thank you screen: Confirms next step + sets expectation ("We'll text within 24h")
Ad copy angle: Focus on the transformation, address #1 objection, create urgency via social proof
```

### Promotion / Special Offer

```
Objective: High volume leads at lower CPL (offer does the selling)
Form type: More Volume (lower friction = more leads = more to work)
Promotion rules:
  → Must have real end date (fake urgency kills trust)
  → Discount should be meaningful: 20%+ or $X off (not 5-10%)
  → Name the offer in the hook: "20% off your first session — June only"
  → Retarget non-converters at Day 3 and Day 6 with countdown
Budget allocation: Run heavier in first 10 days, taper in final week
Expected CPL: 30-50% lower than standard acquisition campaign
Expected lead quality: Lower — build Higher Intent retargeting sequence to upgrade them
```

### Seasonal Campaign

```
Run 3-4 weeks before the seasonal event (not during — decision is made before)
Seasonal hooks that work in Ontario:
  Wedding season: "Your smile is part of the photos — make it ready"
  Summer: "Summer is 6 weeks away. Your confidence doesn't have to wait."
  Valentine's: "Give [her/him] something they'll remember"
  New Year: "This year, stop hiding your smile"
Urgency mechanism: Calendar date as natural deadline (no fake scarcity needed)
Audience: Layer seasonal interests (wedding planning, event photography) over base
```

### Retargeting

```
Audience: Website visitors (30-day), Lead form openers (non-submitters), Past leads
Frequency cap: 2-3 impressions per person per week
Creative rule: MUST be different from acquisition creative (they've seen it)
Angles to rotate:
  Touch 1 (Day 1-3): Social proof — "Others from [city] who hesitated…"
  Touch 2 (Day 4-7): Objection killer — address the #1 reason they didn't book
  Touch 3 (Day 8-14): Urgency or offer — real deadline or bonus
Budget: 10-20% of total campaign budget
Expected performance: CPL 40-60% lower than cold acquisition
```

---

## Quick Decision Checklist (Run Before Every Ad)

Before writing a single word of copy, answer these 7 questions:

```
1. STAGE:    What stage is this business? (New / Growing / Established)
2. CLOSE:    What is their close rate? (Adjust ICP targeting accordingly)
3. PROOF:    What is the highest available social proof tier? (Use it in the hook)
4. BUDGET:   Is the budget above $15/day? If not, advise to wait.
7. OBJECTION:What is the #1 reason people don't buy? (Address in primary text)
5. TYPE:     Service or product? (Sets objective, form type, copy structure)
6. CAMPAIGN: What type of campaign? (Acquisition / Promotion / Seasonal / Retarget)
7. CANADIAN: Is the tone warm, local, and specific to a city or region?
```

If you cannot answer all 7, go back to the client intake / S state before writing.
An ad built without answering these questions will score below 70/100 on the audit.
