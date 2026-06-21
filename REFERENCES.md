# Runbase CRM — Master Reference Guide
# FILE NAME TO REMEMBER: REFERENCES.md
# HOW TO USE: Start every build conversation by saying "read REFERENCES.md first"

---

## 🏗️ BUSINESS MODEL

### The Core Principle
Clients never log into GHL. Runbase is the interface. GHL is the engine.

### Two-Track Model
**Track A — Services (Now)**
Done-for-you services at $1,500-3,000/mo per client. Tools validate in real work. Every client is a case study. Cash flow funds the build.

**Track B — Software (Building Toward)**
Sell Runbase CRM subscriptions to agencies. White-label option for resellers.
- Starter: $97/mo
- Pro: $197/mo
- Agency: $397/mo
- Enterprise/White Label: $697/mo

### GHL Integration Strategy
- Phase 1: Agency API Key (master key, all sub-accounts)
- Phase 2: OAuth per Sub-Account (white-label)
- Phase 3: Webhook Real-Time (pipeline events push to Runbase)

### Critical Architecture Rule
Every module must be iFrame-embeddable for GHL from day one.
Each tool needs its own standalone URL that works inside GHL sub-accounts.
Auth via GHL SSO or login token per client.

---

## 🛠️ ALL 17 TOOL MODULES

### Phase 1 — MVP (Build First)
1. **Client Dashboard + Health Score** (access_key: dashboard) — All tiers
   Live 0-100 Business Health Score. Measures automation, brand, ads, pipeline.
   
2. **AI Audit Assistant** (access_key: audit_assistant) — All tiers
   Listens to live consultation calls. Identifies gaps. Generates Gap Report + Build Plan.
   
3. **Meta Ads Agent** (access_key: meta_ads) — All tiers ← CURRENTLY BUILDING
   5-stage pipeline: Data → Audit → Research → Ad Builder → Visual + Image Gen
   
4. **Brand Builder** (access_key: brand_builder) — All tiers
   6-phase brand build: Discovery → DNA → Naming → Visual Identity → Assets → Brand Book
   
5. **Gap Report Builder** (access_key: gap_report) — All tiers
   Pre-populates from audit. Exports PDF. Logs to GHL.
   
6. **Proposal Generator** (access_key: proposal_gen) — Pro+
   Audit to proposal. Package selection. Pushes to GHL as opportunity.

### Phase 2 — Growth
7. **Runbase Automate — n8n Embedded** (access_key: n8n_automate) — Pro+
   UNIQUE DIFFERENTIATOR. n8n self-hosted, branded as Runbase Automate. 400+ integrations. No per-task fees.
   
8. **Brief-to-Everything Engine** (access_key: brief_engine) — Pro+
   UNIQUE DIFFERENTIATOR. One intake form pre-populates every tool automatically.
   
9. **Competitor Intelligence Feed** (access_key: competitor_intel) — Starter (1), Pro (3), Agency (unlimited)
   UNIQUE DIFFERENTIATOR. Weekly automated competitor monitoring via Apify. Meta ads, Instagram, Google reviews.
   
10. **Onboarding Assistant** (access_key: onboarding) — Pro+
    Post-sale onboarding. Collects accesses. Builds kickoff plan. Triggered by GHL Closed Won.

### Phase 3 — Scale
11. **Design Studio** (access_key: design_studio) — Pro+
    Flux/DALL-E 3 for images. Bannerbear/Templated.io for branded templates. Creatomate for video. NOTE: Canva Autofill = Enterprise only. Use Bannerbear instead.
    
12. **Industry Pre-Configuration** (access_key: industry_config) — Pro+
    UNIQUE DIFFERENTIATOR. 20+ industry configs. If client has existing brand — ingest it, skip brand builder.
    
13. **Client Success Assistant** (access_key: client_success) — Agency+
    Monitors health score. Flags churn risk. Triggers upsell conversations.
    
14. **Lead Qualification Assistant** (access_key: lead_qual) — Agency+
    Qualifies leads before audit call. Scores opportunity. Prepares pre-audit brief.
    
15. **Snapshot and System Library** (access_key: snapshot_lib) — Agency+
    GHL snapshots and automation templates by industry. One-click deploy.
    
16. **Scope Control Assistant** (access_key: scope_control) — Agency+
    Prevents scope creep. Flags out-of-scope requests. Generates response scripts and change orders.
    
17. **QA Testing Assistant** (access_key: qa_testing) — Agency+
    Creates testing instructions for automation builds. Verifies before client handover.

---

## 🆚 6 UNIQUE DIFFERENTIATORS (The Moat)
1. AI Business Health Score — live 0-100, nobody else has this
2. Brief-to-Everything Engine — one form pre-populates all tools
3. Competitor Intelligence Feed — automated weekly competitor monitoring
4. Industry Pre-Configuration — 20+ industry configs, respects existing brands
5. Client Build Progress View — clients see their business being built in real time
6. Runbase Automate (n8n) — unlimited automation, no per-task fees

---

## 💻 TECH STACK
- Frontend: Single-page app (HTML → React rebuild planned)
- Auth + Database: Supabase (pgcrypto for key encryption)
- AI Engine: Anthropic API — Claude Sonnet 4.6
- Automation: n8n self-hosted (branded as Runbase Automate)
- GHL Integration: GHL Agency API v2
- Image Generation: Flux via Replicate + DALL-E 3
- Branded Templates: Bannerbear or Templated.io (NOT Canva API — Enterprise only)
- Video: Creatomate API
- Social Research: Apify
- Payments: Stripe
- Hosting: Vercel (live: https://meta-ads-agent-cyan.vercel.app/ — auto-deploys on git push)

---

## 📚 REFERENCE REPOSITORIES

### UI Components (use when rebuilding in React)
- **shadcn/ui** — https://github.com/shadcn/ui
  Copy-paste React components. Dark mode ready. Use for tables, cards, forms.

### Architecture Template (use when starting React rebuild)
- **bulletproof-react** — https://github.com/alan2207/bulletproof-react
  Industry-standard folder structure, TypeScript, API state handling.

### Dashboard Design Inspiration
- **posthog/posthog** — https://github.com/posthog/posthog
  Best open-source analytics dashboard. Study for health scores, campaign tables.

### Design Assets
- **bradtraversy/design-resources-for-developers** — https://github.com/bradtraversy/design-resources-for-developers
  Free fonts, color palettes, icons, UI kits.

### Dark UI Patterns
- **VoltAgent/awesome-design-md** — https://github.com/VoltAgent/awesome-design-md
  Dark interfaces, command layouts, micro-interactions.

### GHL + External API Connectors (use for Phase 2 GHL integration)
- **Composio Awesome Claude Skills** — https://github.com/ComposioHQ/awesome-claude-skills
  Pre-built Claude Code skills for connecting to external SaaS tools.
  Most relevant for Runbase: GHL connector, Stripe connector, Google Sheets connector.
  Use when building GHL OAuth per-sub-account integration in Phase 2.
  Install when ready: npx composio-core add gohighlevel

### Codebase Context Tool (use at start of every Claude Code session)
- **Repomix** — https://github.com/yamadashy/repomix
  Packs entire codebase into one AI-friendly file for perfect Claude context.
  Safety verified: Uses npm Trusted Publishing with OIDC provenance attestation.
  Install: npm install -g repomix
  Run before sessions: repomix /home/admin/meta-ads-agent
  Auto-runs via: .claude/hooks/pre-session.sh

---

## 🔧 INSTALLED SKILLS (Claude Code)
Location: ~/.claude/skills/ — 66 skills from jeffallan/claude-skills

Key skills for this project:
- debugging-wizard — hard-to-trace bugs
- secure-code-guardian — before any auth or key storage work
- postgres-pro — Supabase RLS, pgcrypto, schema
- architecture-designer — before building any new module
- javascript-pro — vanilla JS optimization
- react-expert — when rebuilding in React
- api-designer — when building backend API layer

---

## 🗓️ WHEN TO USE EACH REFERENCE

| Situation | What to use |
|-----------|-------------|
| Bug is hard to find | debugging-wizard skill |
| Building auth or key storage | secure-code-guardian skill |
| Writing Supabase SQL or RLS | postgres-pro + sql-pro skills |
| Starting a new feature | architecture-designer skill first |
| Building React components | react-expert skill + shadcn/ui |
| Designing dashboard UI | posthog repo for inspiration |
| Need icons/fonts/colors | bradtraversy repo |
| Starting React CRM rebuild | bulletproof-react repo |

---

## 📌 RULES TO NEVER BREAK
1. Always read this file at the start of every build conversation
2. Use architecture-designer skill to plan BEFORE writing code
3. Every module must be iFrame-embeddable for GHL
4. Canva Autofill API = Enterprise only. Use Bannerbear/Templated.io instead
5. pgcrypto passphrase must move to env var before production
6. shadcn/ui replaces building UI from scratch — check there first
7. GHL is the engine. Runbase is the interface. Never reverse this.
