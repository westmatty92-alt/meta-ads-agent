# BASELEAP APP BUILDING AGENT — SOP FRAMEWORK

## WHEN TO USE THIS SKILL
Read this skill at the start of EVERY session.
It defines the operating procedures the agent follows for all builds.

---

## SOP-001 — REQUIREMENTS GATHERING
Before writing any code confirm:
- What does this tool do in one sentence?
- Who uses it and what CRM?
- What does user input and get back?
- Which APIs are needed?
- What is MVP scope?

Decision: If any answer is unknown → STOP and ask. Never assume.

---

## SOP-002 — PROJECT SETUP CHECKLIST
First session of any new tool:
- [ ] GitHub repo created (format: [name]-agent)
- [ ] Single index.html file only
- [ ] CLAUDE.md written with ai() wrapper location
- [ ] REFERENCES.md written with full ai() wrapper code
- [ ] Relevant skills installed (linear always, others by task)
- [ ] Supabase project created, Canada East region
- [ ] RLS enabled on all tables (check nulls first)
- [ ] Vercel connected and deploying

---

## SOP-003 — SESSION START PROTOCOL
Every Claude Code session starts with:
1. Read CLAUDE.md
2. Read REFERENCES.md
3. Read MASTER_BUILD_GUIDE.md
4. Read relevant SKILL.md files for today's task
5. Fetch Notion todo list
6. State highest priority item
7. Confirm before coding

---

## SOP-004 — MANDATORY CODING RULES
These rules are non-negotiable in every session:

NEVER:
- Raw fetch to api.anthropic.com (CORS error) → use ai() wrapper
- Raw fetch to api.replicate.com (CORS error) → stub for Phase 3
- Use regex to parse AI output → use another AI call with JSON return
- Hardcode colors → use CSS variables or getBrandColors()
- Use response_format in GPT Image 2 calls (deprecated)
- Enable RLS without checking NULL user_ids first
- Read global state in async loops → pass as parameter directly
- Use .textContent for AI output → use innerHTML + renderMarkdown()
- Use CSS variables for modal backgrounds → hardcode hex (#0D1F2D)
- Use <a href download> for base64 images → use downloadImageBlob()

ALWAYS:
- Use IF NOT EXISTS for all SQL changes
- Pass image size directly to generation functions
- Apply Canvas brand overlay after image generation
- Open relevant skills before writing any feature code
- Run brace balance check before every commit
- Update Notion after every session

---

## SOP-004 — PRE-COMMIT CHECKLIST
Run before every git commit:

ARCHITECTURE:
- [ ] Single index.html file
- [ ] No raw Anthropic fetch
- [ ] No raw Replicate fetch
- [ ] All tables have RLS enabled

AI PATTERNS:
- [ ] All Claude calls use ai() wrapper
- [ ] All AI text uses innerHTML + renderMarkdown()
- [ ] Structured extraction uses AI call not regex

IMAGE GENERATION:
- [ ] No response_format parameter
- [ ] Size passed as parameter not read from global state
- [ ] Canvas overlay applied after generation
- [ ] Download uses blob not direct href

STATE:
- [ ] Critical S state loaded from Supabase in initApp()
- [ ] S state reset on new pipeline run

QUALITY:
- [ ] Brace balance check passes
- [ ] No uncaught console errors

---

## SOP-005 — DEPLOYMENT VERIFICATION
After every push:
1. Wait 30-45 seconds for Vercel
2. Hard refresh browser (Cmd+Shift+R)
3. Test the changed feature
4. Check browser console for errors

If broken:
- Old behavior → cache issue → incognito window
- Console error → read it → fix in Claude Code → push again
- No deployment → check Vercel dashboard for build error

---

## SOP-006 — BUG RESOLUTION ORDER
1. Check known bugs in Master Rules Document FIRST
2. Read the console error
3. Match to known pattern table
4. Apply documented fix
5. If new bug → document it in Master Rules Document

Known patterns:
- Failed to fetch + anthropic → replace with ai() wrapper
- Failed to fetch + replicate → needs backend proxy
- UNBALANCED braces → find and fix before commit
- violates row-level security → user_id missing in payload
- Unknown parameter response_format → remove it
- Markdown showing as **text** → use renderMarkdown()
- Download not working → use downloadImageBlob()
- Image wrong size/same size → pass size as parameter not global

---

## SOP-007 — SESSION END PROTOCOL
Every session ends with:
1. Update Notion todo list (mark complete, add new items)
2. Update Tool Build Document (feature status)
3. Update Master Rules if new patterns found
4. Update Skills Reference if new use cases found
5. State session summary:
   - What was built (with commit hashes)
   - What is still pending
   - What next session should start with

---

## DECISION TREES

### Which objective for Meta campaign?
```
Has verified pixel AND payment at booking page online?
  YES → Sales objective (Meta UI name)
        Conversion event: Purchase
        Old name was "Conversions" — same thing
  NO  → Leads objective
        Instant Form required
        No pixel needed
```
Quick reference:
- Sales          = find people likely to purchase (pixel required)
- Leads          = collect contact info (no pixel needed)
- Traffic        = send clicks (no conversion optimization)
- Awareness      = reach and recall (no conversion)
- Engagement     = likes/comments/messages
- App Promotion  = app installs (SDK required)

### Which skills to install?
```
UI work?          → linear (always)
Ad copy?          → marketing + ad-hooks + copywriting
Campaign setup?   → ad-strategy + meta-ads-setup
Images?           → gpt-image-2 (Phase 1) / higgsfield (Phase 2+)
New tool/project? → sop-framework (always)
```

### Is this a known bug?
Check the Master Rules Document first:
https://app.notion.com/p/38b6d6be0d4181b689f9fc443b66e1df
- Match found → apply the documented fix exactly
- No match   → diagnose fresh, then document the new bug

### RLS safe to enable?
```
SELECT COUNT(*) FROM [table] WHERE user_id IS NULL;
  0 rows   → safe to enable RLS
  1+ rows  → fix the nulls first, then enable
```

### Supabase write verified?
- Always chain `.select().single()` on writes
- A 0-row update returns success silently (Rule #11)
- Verify a row came back before rendering success

### LLM output truncated vs malformed?
- Check `stop_reason === 'max_tokens'` first (Rule #17)
- Set `max_tokens` explicitly on large generation calls
- Never inherit the default 4000 for structured output

---

## ARCHITECTURE PRINCIPLES
1. Standalone first — tool works independently
2. Single HTML file — all CSS and JS inline
3. GHL-embeddable — iframe via custom menu item
4. Canadian SMB — CAD, CASL, Ontario context
5. ai() wrapper always — never raw Anthropic fetch
6. Supabase RLS always — every table, every time
7. Brand kit from Base Profile — never hardcode colors
8. Verify at every boundary — Rule #14
