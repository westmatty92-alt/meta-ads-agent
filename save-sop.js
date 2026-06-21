// save-sop.js — Creates the sop_documents table and inserts the project SOP.
// Run: node save-sop.js
//
// NOTE: CREATE TABLE requires elevated DB access. Run the DDL below manually
// in the Supabase dashboard → SQL Editor if this script reports a table-not-found error.

const SUPA_URL = 'https://ytumpmtkxkhhehmvljoy.supabase.co';
const SUPA_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0dW1wbXRreGtoaGVobXZsam95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE0MjgxMDEsImV4cCI6MjA5NzAwNDEwMX0.0CHSJ1iXW8e8q49cdgte80VrmDgX_COejMRVIRMxi9I';

const SOP_TITLE = 'Agency CRM — Meta Ads Agent: Full Project SOP v1.0';

const SOP_CONTENT = `
# Agency CRM — Meta Ads Agent
## Standard Operating Procedure (SOP) v1.0
Generated: 2026-06-17

---

## 1. PROJECT OVERVIEW

**App Name:** Agency CRM — Meta Ads Agent
**Purpose:** A single-page AI-powered CRM for marketing agencies managing Meta (Facebook/Instagram) ad campaigns. The agent guides users through a 5-stage pipeline: data input → account audit → market research → ad build → visual generation, producing agency-grade ad creative and strategy.

**Live Deployment:** Served via Replit on port 5000.
**Repository:** https://github.com/westmatty92-alt/meta-ads-agent
**Primary File:** index.html (entire frontend — ~3000 lines of HTML/CSS/JS)
**Server:** server.py (Python SimpleHTTPServer with no-cache headers, port 5000, SO_REUSEADDR)

---

## 2. TECH STACK

| Layer | Technology |
|-------|------------|
| Frontend | Vanilla HTML5 / CSS3 / JavaScript (no framework) |
| Auth & Database | Supabase (PostgreSQL + Auth + PostgREST) |
| AI — Claude | Anthropic Claude API (claude-sonnet-4-6) via direct browser fetch |
| AI — OpenAI | OpenAI GPT-4o via direct browser fetch |
| Image Gen | OpenAI DALL-E 3 |
| Competitor Research | Apify (reddit-posts-scraper, meta-ads-demographics-actor) |
| CRM Integration | GoHighLevel (GHL) REST API v1 |
| Hosting | Replit |
| Version Control | GitHub (westmatty92-alt/meta-ads-agent) |

**Key CDN:**
- Supabase JS: https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js

---

## 3. ARCHITECTURE

### Single-File SPA Pattern
The entire application lives in index.html. There is no build step, no bundler, and no framework. All CSS, HTML structure, and JavaScript are inline.

### State Object
A global \`S\` object holds all pipeline state:
\`\`\`js
let S = {
  adData, product, price, usp, audience, budget, goal,
  pain, desire, objection, voice, competitors, compCopy,
  auditScore, auditIssues, auditSummary,
  researchSummary, adCopy, audienceDemographics,
  launchMode, adFormat, niche,
  brandName, brandColors, brandFont, brandLogoUrl, brandVibe,
  dallePrompt, lastImageUrl, visualConcept, lastAdId, adDataSaved,
  history: { audit, research, build, visual },
  stagesDone: new Set(), targetCpa, targetRoas
}
\`\`\`

### API Keys Object
\`\`\`js
let KEYS = { claude, openai, apify, ghl, ghlLocation, provider }
\`\`\`
Loaded from Supabase \`user_keys\` table on login. Never stored in localStorage.

### Navigation Model
The \`go(name)\` function controls which panel is visible. Main pipeline panels (\`data\`, \`audit\`, \`research\`, \`build\`, \`visual\`) are \`.spanel\` divs shown/hidden with the \`.active\` class. Settings and Auto-Research are overlays shown/hidden with the \`.open\` class.

### AI Call Pattern
All AI calls go through the \`ai(system, messages)\` function which routes to Claude or OpenAI based on \`KEYS.provider\`. Direct browser fetch — no backend proxy.

### Auth Flow
1. \`getSession()\` on page load — calls \`initApp()\` if session exists
2. \`onAuthStateChange\` — handles INITIAL_SESSION, SIGNED_IN, SIGNED_OUT
3. Guard: \`currentUser?.id !== session.user.id\` prevents double-init race

---

## 4. DATABASE TABLES

### user_keys
Stores API keys per user. Keys optionally encrypted via pgcrypto.
\`\`\`sql
CREATE TABLE user_keys (
  id          uuid default gen_random_uuid() primary key,
  user_id     uuid references auth.users not null unique,
  claude_key      text default '',
  openai_key      text default '',
  apify_key       text default '',
  ghl_key         text default '',
  ghl_location_id text default '',
  ai_provider     text default 'claude',
  updated_at  timestamp with time zone default now()
);
\`\`\`

### businesses
Multi-tenant: each user can manage multiple businesses/clients.
\`\`\`sql
CREATE TABLE businesses (
  id         uuid default gen_random_uuid() primary key,
  user_id    uuid references auth.users not null,
  name       text not null,
  industry   text default '',
  meta       jsonb default '{}',
  created_at timestamp with time zone default now()
);
\`\`\`

### pipeline_runs
Saves the full pipeline state per business (upserted on conflict of business_id).
\`\`\`sql
CREATE TABLE pipeline_runs (
  id                uuid default gen_random_uuid() primary key,
  business_id       uuid references businesses not null unique,
  user_id           uuid references auth.users not null,
  product           text, price text, usp text,
  audience          text, budget text, goal text,
  pain              text, desire text, objection text,
  competitors       text, ad_data text, comp_copy text, voice text,
  audit_score       integer, audit_summary text,
  research_summary  text, ad_copy text,
  launch_mode       boolean default false,
  stages_done       text[],
  brand_kit         jsonb,
  updated_at        timestamp with time zone default now()
);
\`\`\`

### generated_ads
Ad Library — stores every completed ad package.
\`\`\`sql
CREATE TABLE generated_ads (
  id           uuid default gen_random_uuid() primary key,
  business_id  uuid references businesses,
  user_id      uuid references auth.users not null,
  product      text, audience text,
  hook         text, primary_text text, headlines text,
  cta          text, strategy text, full_copy text,
  visual_brief text, image_url text,
  audit_score  integer,
  created_at   timestamp with time zone default now()
);
\`\`\`

### ad_performance
Stores CSV-uploaded or GHL-synced campaign performance history.
\`\`\`sql
CREATE TABLE ad_performance (
  id              uuid default gen_random_uuid() primary key,
  business_id     uuid references businesses,
  user_id         uuid references auth.users not null,
  campaign_name   text,
  spend           numeric, impressions integer, clicks integer,
  ctr             numeric, cpc numeric, cpa numeric,
  conversions     integer, roas numeric,
  raw_data        jsonb,
  created_at      timestamp with time zone default now()
);
\`\`\`

### sop_documents
Stores project SOP and documentation.
\`\`\`sql
CREATE TABLE IF NOT EXISTS sop_documents (
  id         uuid default gen_random_uuid() primary key,
  title      text not null,
  content    text not null,
  version    text default '1.0',
  created_at timestamp with time zone default timezone('utc'::text, now()),
  updated_at timestamp with time zone default timezone('utc'::text, now())
);
\`\`\`

---

## 5. SUPABASE SQL SETUP (run in SQL Editor)

### Step 1: Create all tables (see Section 4 above)

### Step 2: Enable pgcrypto encryption for API keys (optional but recommended)
\`\`\`sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION _try_decrypt(val text, enc_pass text)
RETURNS text LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  IF val IS NULL OR val = '' THEN RETURN ''; END IF;
  BEGIN
    RETURN pgp_sym_decrypt(decode(val,'base64'), enc_pass);
  EXCEPTION WHEN OTHERS THEN RETURN val; END;
END; $$;

CREATE OR REPLACE FUNCTION upsert_user_keys(
  p_user_id uuid, p_claude text, p_openai text, p_apify text,
  p_ghl text, p_ghl_loc text, p_provider text
) RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE enc text := '1cd873eb7b17c06ec69a47d845e8509ed0882e7768b233e23d8e72b8d975bf02';
BEGIN
  INSERT INTO user_keys(user_id,claude_key,openai_key,apify_key,ghl_key,ghl_location_id,ai_provider,updated_at)
  VALUES (p_user_id,
    CASE WHEN p_claude  <> '' THEN encode(pgp_sym_encrypt(p_claude, enc),'base64') ELSE '' END,
    CASE WHEN p_openai  <> '' THEN encode(pgp_sym_encrypt(p_openai, enc),'base64') ELSE '' END,
    CASE WHEN p_apify   <> '' THEN encode(pgp_sym_encrypt(p_apify,  enc),'base64') ELSE '' END,
    CASE WHEN p_ghl     <> '' THEN encode(pgp_sym_encrypt(p_ghl,    enc),'base64') ELSE '' END,
    CASE WHEN p_ghl_loc <> '' THEN encode(pgp_sym_encrypt(p_ghl_loc,enc),'base64') ELSE '' END,
    p_provider, now())
  ON CONFLICT (user_id) DO UPDATE SET
    claude_key=EXCLUDED.claude_key, openai_key=EXCLUDED.openai_key,
    apify_key=EXCLUDED.apify_key, ghl_key=EXCLUDED.ghl_key,
    ghl_location_id=EXCLUDED.ghl_location_id,
    ai_provider=EXCLUDED.ai_provider, updated_at=now();
END; $$;

CREATE OR REPLACE FUNCTION get_user_keys(p_user_id uuid)
RETURNS TABLE(claude_key text, openai_key text, apify_key text,
              ghl_key text, ghl_location_id text, ai_provider text)
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE enc text := '1cd873eb7b17c06ec69a47d845e8509ed0882e7768b233e23d8e72b8d975bf02';
        raw user_keys%ROWTYPE;
BEGIN
  SELECT * INTO raw FROM user_keys WHERE user_keys.user_id = p_user_id;
  IF NOT FOUND THEN RETURN; END IF;
  RETURN QUERY SELECT
    _try_decrypt(raw.claude_key,enc), _try_decrypt(raw.openai_key,enc),
    _try_decrypt(raw.apify_key, enc), _try_decrypt(raw.ghl_key,enc),
    _try_decrypt(raw.ghl_location_id,enc), raw.ai_provider;
END; $$;

GRANT EXECUTE ON FUNCTION upsert_user_keys TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_keys     TO authenticated;
GRANT EXECUTE ON FUNCTION _try_decrypt      TO authenticated;
\`\`\`

### Step 3: RLS Policies
Enable RLS on all tables and add user-scoped policies:
\`\`\`sql
-- user_keys
ALTER TABLE user_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY "user_keys: own rows" ON user_keys
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- businesses
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
CREATE POLICY "businesses: own rows" ON businesses
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- pipeline_runs
ALTER TABLE pipeline_runs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "pipeline_runs: own rows" ON pipeline_runs
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- generated_ads
ALTER TABLE generated_ads ENABLE ROW LEVEL SECURITY;
CREATE POLICY "generated_ads: own rows" ON generated_ads
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

-- ad_performance
ALTER TABLE ad_performance ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ad_performance: own rows" ON ad_performance
  USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
\`\`\`

---

## 6. ALL API KEYS REQUIRED

| Key | Where to get | Settings field |
|-----|-------------|----------------|
| Claude API Key | console.anthropic.com → API Keys | Claude API |
| OpenAI API Key | platform.openai.com → API Keys | OpenAI API |
| Apify API Key | console.apify.com → Integrations | Apify API |
| GHL API Key | GoHighLevel → Settings → API Keys | GHL API |
| GHL Location ID | GoHighLevel → Settings → Business Info | GHL Location ID |

**AI Provider:** User selects Claude or OpenAI in Settings. Claude is default.
**Apify Actors used:**
- \`parseforge/reddit-posts-scraper\` — Reddit voice-of-customer research (~$3/1k)
- \`xanthic_mead/meta-ads-demographics-actor\` — Competitor Meta ads discovery

**⚠️ SECURITY NOTE:** The pgcrypto passphrase in setup-encryption.sql (\`1cd873eb7b17c06ec69a47d845e8509ed0882e7768b233e23d8e72b8d975bf02\`) is hardcoded in the deployed SQL functions. This is a known risk — treat it as a symmetric key and rotate by redeploying the functions with a new passphrase.

---

## 7. PIPELINE — 5 STAGES

### Stage 1 — Data Collection
User inputs: product, price, USP, monthly budget, goal (purchase/lead/traffic), target CPA/ROAS, audience, pain point, desire, objection, voice-of-customer, competitor names, competitor ad copy. Also supports CSV upload of existing campaign performance data.

Two modes: **Existing Advertiser** (has performance data) and **New Advertiser** (launching fresh, triggers pre-launch checklist mode in Audit).

### Stage 2 — Audit
**Existing mode:** Runs 50-check framework. Scoring: Creative 20pts + Budget 20pts + Audience 15pts + Structure 15pts + Pixel 15pts + Compliance 15pts. Outputs SCORE/GRADE + CRITICAL → IMPORTANT → OPTIMIZATIONS → TOP 3 ACTIONS.
**Launch mode:** Pre-launch checklist covering account setup, pixel, campaign structure, budget, audience, creative requirements, launch sequence. Outputs READY TO LAUNCH SCORE: 0-100.

### Stage 3 — Market Research
Maps competitive landscape, identifies messaging angles, surfaces what's working in the market. Uses competitor names + ad copy from Stage 1 as context.

### Stage 4 — Ad Builder
Synthesizes audit + research + customer voice → complete ad package: hook, primary text, headlines, CTA, strategy notes.

### Stage 5 — Visual
Produces detailed visual brief (layout, mood, subject, text overlay) + 3 DALL-E 3 image generation prompts. Can generate images directly via OpenAI DALL-E 3 if OpenAI key is set.

### Run All
"Run All" button auto-runs stages 2→3→4→5 sequentially. Each stage unlocks after the previous completes.

---

## 8. ADDITIONAL FEATURES

### Ad Library
Auto-saves every completed Stage 4+5 run to \`generated_ads\` table. Users can browse, copy, or "Use as Starting Point" to feed a previous ad into a new pipeline run. Tabs: My Ads / Top Performers.

### Dashboard
Pulls from \`ad_performance\` (CSV upload or GHL sync). Shows: 6 metrics cards (spend, impressions, clicks, CTR, CPA, ROAS), SVG line/bar charts, campaigns table (sortable), AI-generated suggestions panel. AI Suggestions button calls Claude with full performance context and returns actionable recommendations.

### Auto-Research Overlay
Runs 3 Apify actors in parallel: Reddit posts (voice of customer), Meta ads demographics (competitor discovery), and optionally a custom actor. Results are injected into the Stage 1 context for downstream stages.

### Multi-Business / CRM
Users create multiple businesses. The business switcher in the header changes context for pipeline runs, ad library, and performance data. All data is scoped to \`business_id\`.

### Brand Kit
Per-business brand configuration: brand name, 2–6 color palette (with color picker), font style, logo URL, brand vibe/tone. Injected into Stage 5 visual prompts.

### GHL Integration
Syncs campaigns and performance data from GoHighLevel via REST API v1. Auto-sync runs silently every 24h if a GHL key is present. Manual sync available in the Dashboard and Stage 1 panels.

---

## 9. BUILD HISTORY (chronological)

### 2026-06-14: Initial Build
- **335e57d / 71f0dee** — Initial file upload (starting codebase)
- **a20bc59** — First index.html update
- **eb61e6a** — Fix Supabase key upsert conflict resolution; surface Claude API errors
- **a66f782** — Progress save checkpoint
- **ab6706f** — Update Supabase CDN to fix runtime errors (switched to jsDelivr CDN for supabase-js v2)
- **37c629a** — Update server.py: add no-cache headers, SO_REUSEADDR for port reuse on Replit restarts
- **a67e5ef** — Add Brand Kit to Stage 1 + DALL-E 3 image generation to Stage 5
- **81a7155** — Fix Stage 1 scroll overflow and Brand Kit visibility
- **c229506** — Replace static Brand Kit color fields with dynamic 2–6 color palette builder
- **203f678** — Add Ad Library: auto-save generated ad packages, card grid UI, pipeline context injection
- **b8d0de5** — Add ad_performance table: CSV upload, Supabase storage, performance history, audit context injection
- **49e68d5** — Add GHL Dashboard: analytics cards, SVG charts, sortable campaigns table, AI suggestions
- **af8186c** — Stage 1 intelligence hub redesign (overview panel, health alerts, GHL sync button)

### 2026-06-15: Encryption & Bug Fixes
- **16ce146** — Add pgcrypto encryption: upsert_user_keys + get_user_keys RPCs via setup-encryption.sql
- **255e34f** — Wire pgcrypto encryption into saveKeys/loadKeys in the app
- **b7e863c** — Debug session: fix silent error swallowing in saveKeys/loadKeys, add console.log tracing
- **7db260a** — Fix settings overlay CSS: replace \`inset\` shorthand with explicit top/right/bottom/left (Replit browser compat)
- **5222a00** — saveKeys: skip RPC, use direct upsert (debugging step, encryption RPC not yet reliably deployed)
- **a55e508 / c0f1902 / 1afc20c / 1953efc** — Replit auto-publishes during iteration

### 2026-06-17: Key Persistence Debugging Sprint
- **f9f993f** — Restore encrypted RPC path with plaintext fallback: try upsert_user_keys first, fall back to direct upsert if RPC not deployed
- **9a2e954** — GHL settings: live connection test (testGHLConnection), pending/connected/error states, Location ID field type=text, "Test Connection" button
- **eef9b6b** — Fix key persistence infrastructure: load status indicator bar in Settings, PGRST116 treated as "no keys yet" (not an error), onAuthStateChange scoped to INITIAL_SESSION + SIGNED_IN only, SIGNED_OUT reloads page, guard against signIn()+onAuthStateChange double-init race
- **e98f5bf** — Fix key field population: decouple _applyKeyData from DOM (only writes KEYS object), add populateKeyInputs() called when Settings panel opens via go('settings')
- **58f0c1c** — Debug logging: console.log raw Supabase row in _applyKeyData, KEYS state after loadKeys in initApp
- **c15b615** — Fix loadKeys early-return bug: RPC returning empty array [] is truthy in JS → was short-circuiting before direct read. Fix GHL test endpoint: /v1/locations/ requires agency access → changed to /v1/contacts/?limit=1
- **6e7255a** — Replace loadKeys with simple direct-read version: no RPC, maximum logging, no early returns
- **249c483** — Fix session restore: getSession() now calls initApp() when session exists (was only showing/hiding auth screen; was relying on INITIAL_SESSION event which is not guaranteed to fire reliably on all Replit page loads)

---

## 10. BUGS ENCOUNTERED AND FIXES

### BUG-001: Supabase CDN runtime error
**Symptom:** App crashed on load with JS error.
**Cause:** Wrong CDN URL for supabase-js.
**Fix (ab6706f):** Switched to jsDelivr CDN: \`https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js\`

### BUG-002: Port reuse error on Replit restart
**Symptom:** server.py failed to bind on restart — "Address already in use".
**Fix (37c629a):** Added \`allow_reuse_address = True\` to ReusableTCPServer subclass.

### BUG-003: Settings overlay positioning (CSS \`inset\` shorthand)
**Symptom:** Settings panel not covering the full viewport on some browsers.
**Cause:** \`inset: 0\` shorthand not supported in all Replit preview browsers.
**Fix (7db260a):** Replaced with explicit \`top:0; right:0; bottom:0; left:0;\`.

### BUG-004: saveKeys silent failure
**Symptom:** "Keys saved" toast shown but keys weren't persisted.
**Cause:** Error was being swallowed — no console output, no UI feedback on failure.
**Fix (b7e863c):** Added console.error with full error object, setSt('Save failed') on error path.

### BUG-005: saveKeys RPC vs direct upsert confusion
**Symptom:** After encryption RPCs were added, saveKeys broke intermittently.
**Cause:** The \`upsert_user_keys\` RPC was not deployed in Supabase yet; code had no fallback.
**Fix (f9f993f):** Restored try-RPC-first, fall-back-to-direct-upsert pattern. Status message says "encrypted" or plain based on which path succeeded.

### BUG-006: GHL status badge showed "Connected" without testing
**Symptom:** GHL status always showed "● Connected" as soon as a key was typed, regardless of validity.
**Cause:** \`updateAllKeyStatuses()\` set status to Connected based purely on key string presence.
**Fix (9a2e954):** Added \`testGHLConnection()\` function that does a real HTTP test. Status is "Not Tested" on load; becomes "✓ Connected" or "✗ [error]" after test.

### BUG-007: GHL connection test always showed "Unauthorized"
**Symptom:** testGHLConnection showed error even with a valid GHL key.
**Cause:** Test used \`GET /v1/locations/\` which requires agency-level API access. Most users have location-level keys that get 401 from that endpoint.
**Fix (c15b615):** Changed test endpoint to \`GET /v1/contacts/?limit=1\` which works for both access levels.

### BUG-008: API keys not persisting between sessions (multi-root cause)
This was the most complex bug — multiple compounding issues:

**Root cause A — _applyKeyData writing to hidden DOM elements:**
_applyKeyData() tried to set input.value on Settings panel inputs immediately after load, before the overlay was opened. While hidden elements ARE in the DOM, separating data load from UI population is cleaner and more reliable.
**Fix (e98f5bf):** _applyKeyData() only writes KEYS object. New \`populateKeyInputs()\` fills inputs. Called from \`go('settings')\` when panel opens.

**Root cause B — loadKeys() early return on empty RPC array:**
\`get_user_keys\` RPC (Postgres RETURNS TABLE) wraps results in an array. Empty result = \`[]\` which is truthy in JS. Code entered the \`if (!rpcErr && rpcData)\` block, found \`rpcData[0] === undefined\`, hit a hard \`return\` labelled "No keys saved yet" — never reaching the direct table read that would have found the keys.
**Fix (c15b615):** Removed early return; falls through to direct read when RPC yields no row.

**Root cause C — onAuthStateChange double-init race:**
\`signIn()\` called \`initApp()\` directly, then \`onAuthStateChange\` fired \`SIGNED_IN\` and called \`initApp()\` again. Two concurrent \`loadKeys()\` fetches could interleave.
**Fix (eef9b6b):** Guard: \`currentUser?.id !== session.user.id\` — skips re-init if already initialized for same user. onAuthStateChange scoped to INITIAL_SESSION + SIGNED_IN only (not TOKEN_REFRESHED).

**Root cause D — getSession() not calling initApp() for returning users:**
On page refresh, \`getSession()\` found the existing session but only showed/hid the auth screen. Relied entirely on \`onAuthStateChange(INITIAL_SESSION)\` to call \`initApp()\`, which was not reliably firing on Replit's page load environment.
**Fix (249c483):** \`getSession().then()\` now calls \`initApp(session.user)\` directly when session exists.

---

## 11. DEPLOYMENT SETUP

### Replit
- Project runs on Replit with \`server.py\` as the run command
- Port: 5000 (configured in .replit)
- server.py serves the directory with no-cache headers and SO_REUSEADDR
- Files: index.html (app), server.py (server), setup-encryption.sql (DB setup reference)

### .replit config
\`\`\`
run = "python3 server.py"
\`\`\`

### Git / GitHub Workflow
- Remote: https://github.com/westmatty92-alt/meta-ads-agent
- Branch: main
- Auth: PAT embedded in remote URL (ghp_... token in remote origin)
- Workflow: edit on Replit/Claude → \`git add index.html && git commit -m "..." && git push origin main\`
- Most commits are direct pushes to main; no PR workflow currently

---

## 12. KNOWN ISSUES

1. **Encryption passphrase hardcoded in SQL** — The pgcrypto passphrase (\`1cd873eb7b17c06ec69a47d845e8509ed0882e7768b233e23d8e72b8d975bf02\`) is embedded in the deployed Postgres functions. Anyone with Supabase dashboard access can read it. Mitigation: rotate by redeploying functions with a new passphrase.

2. **API keys stored in plaintext if RPC not deployed** — If \`setup-encryption.sql\` has not been run, keys are stored unencrypted in \`user_keys\`. The code handles this gracefully (direct upsert fallback) but keys are at-rest plaintext.

3. **Debug console.logs in production** — Several \`console.log\` statements added during key-persistence debugging are still present in the production build (commits 58f0c1c, 6e7255a). These log user IDs and KEYS object (not key values, but presence). Should be removed before public release.

4. **Claude/OpenAI called directly from browser** — API keys are sent in browser fetch() calls. \`anthropic-dangerous-direct-browser-access: true\` header is required for Claude. This works for internal tools but exposes keys to browser devtools. A server-side proxy is recommended for multi-user production deployments.

5. **No RLS policies confirmed** — RLS was designed but not confirmed deployed on all tables. If RLS is misconfigured (enabled but no policy), all reads return empty, causing silent "no keys" symptoms.

6. **GHL API v1 deprecation risk** — App uses GHL REST API v1 (\`rest.gohighlevel.com/v1/...\`). GHL is migrating to v2. Monitor for deprecation notices.

---

## 13. NEXT STEPS / ROADMAP

1. **Remove debug logs** — Strip console.log statements added during debugging sprint
2. **Confirm and document RLS policies** — Verify all tables have correct RLS policies enabled
3. **Deploy setup-encryption.sql** — Ensure all users have encrypted key storage
4. **Test full end-to-end key persistence** — Login → save keys → reload → verify keys appear in Settings
5. **Server-side AI proxy** — Move Claude/OpenAI calls to a backend to protect keys
6. **Multi-user agency tier** — Share businesses/pipeline runs across team members
7. **Webhook-based GHL sync** — Replace polling with GHL webhooks for real-time data
8. **Export features** — PDF/CSV export of audit reports and ad packages
9. **Stripe billing** — Add subscription gating for agency vs. solo tiers
10. **Mobile responsive layout** — Current layout is desktop-optimized

---

*SOP generated 2026-06-17 by Claude Sonnet 4.6*
*Repository: https://github.com/westmatty92-alt/meta-ads-agent*
`.trim();

async function main() {
  const headers = {
    'apikey': SUPA_KEY,
    'Authorization': `Bearer ${SUPA_KEY}`,
    'Content-Type': 'application/json',
    'Prefer': 'return=representation',
  };

  // Step 1: Verify table exists by attempting a select
  console.log('Checking sop_documents table...');
  const check = await fetch(`${SUPA_URL}/rest/v1/sop_documents?limit=1`, { headers });
  if (!check.ok) {
    const err = await check.text();
    console.error('Table check failed:', check.status, err);
    console.error('\nRun this SQL in the Supabase SQL Editor first:\n');
    console.error(`CREATE TABLE IF NOT EXISTS sop_documents (
  id uuid default gen_random_uuid() primary key,
  title text not null,
  content text not null,
  version text default '1.0',
  created_at timestamp with time zone default timezone('utc'::text, now()),
  updated_at timestamp with time zone default timezone('utc'::text, now())
);`);
    process.exit(1);
  }
  console.log('Table exists.');

  // Step 2: Delete any existing SOP with this title (upsert-style via delete+insert)
  console.log('Removing any previous version...');
  await fetch(
    `${SUPA_URL}/rest/v1/sop_documents?title=eq.${encodeURIComponent(SOP_TITLE)}`,
    { method: 'DELETE', headers }
  );

  // Step 3: Insert the SOP
  console.log('Inserting SOP...');
  const res = await fetch(`${SUPA_URL}/rest/v1/sop_documents`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      title:   SOP_TITLE,
      content: SOP_CONTENT,
      version: '1.0',
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error('Insert failed:', res.status, err);
    process.exit(1);
  }

  const data = await res.json();
  console.log('\nSOP saved successfully.');
  console.log('  ID:      ', data[0]?.id);
  console.log('  Title:   ', data[0]?.title);
  console.log('  Version: ', data[0]?.version);
  console.log('  Created: ', data[0]?.created_at);
  console.log('\nCharacter count:', SOP_CONTENT.length.toLocaleString());
}

main().catch(err => { console.error('Fatal:', err); process.exit(1); });
