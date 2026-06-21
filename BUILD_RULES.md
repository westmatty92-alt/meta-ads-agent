# Runbase — Application Build Rules
# Apply these rules to EVERY project we build
# Last updated: June 2026

---

## 🟢 DEPLOYMENT WORKFLOW (Vercel + GitHub)

### How Deployment Works
Deployment is handled automatically by Vercel. Every `git push` to GitHub triggers an instant Vercel deploy. No manual sync, no shell commands, no republishing needed.

### Your Workflow (follow this every time)
1. Claude Code builds feature → commits and pushes to GitHub
2. Vercel detects the push and deploys automatically
3. Live URL is updated within seconds

Done. No clicking. No shell sync.

### sync.sh
The sync.sh file in this project is a no-op placeholder. Deployment is Vercel-automated:
```bash
#!/bin/bash
echo "✅ Deployment is handled automatically by Vercel"
echo "Every git push to GitHub deploys instantly to Vercel"
echo "No manual sync needed"
```

### GitHub Token Setup
- Scope: repo only
- Expiry: No expiration
- Set remote: `git remote set-url origin https://[TOKEN]@github.com/[username]/[repo].git`
- Never commit .env files or expose tokens in chat — revoke immediately if exposed

### Rules
1. ALWAYS let Claude Code handle git commits and pushes
2. NEVER hardcode API keys or tokens in source code
3. ONE token per repo, no expiry, repo scope only
4. If deploy is not updating — check Vercel dashboard for build errors

### For Every New Project
1. Create GitHub repo
2. Connect repo to Vercel (import project in Vercel dashboard)
3. Push to main — Vercel deploys automatically
4. Set environment variables in Vercel dashboard (never in code)

---

## ⚡ THE GOLDEN RULES (Never Break These)

1. Read REFERENCES.md and META_ADS_AGENT_FRAMEWORK.md at the start of every session
2. Use architecture-designer skill BEFORE writing any code for new features
3. Check JS brace balance before EVERY commit — do not commit if unbalanced
4. Every module must be iFrame-embeddable for GHL from day one
5. Canva Autofill API = Enterprise only — use Bannerbear/Templated.io instead
6. pgcrypto passphrase must move to environment variable before production
7. shadcn/ui first — always check if a component exists there before building from scratch
8. GHL is the engine. Runbase is the interface. Never reverse this.
9. Every new repo gets Repomix set up before first Claude Code session
10. Repomix runs once at session start, not continuously

---

## 🚀 PROJECT SETUP CHECKLIST
Run this checklist every time you start a new project

### Step 1 — Repository
- [ ] Create GitHub repo (public or private)
- [ ] Clone to local: `git clone [url]`
- [ ] Set up git config: `git config user.email` and `git config user.name`
- [ ] Set git pull strategy: `git config pull.rebase true`
- [ ] Create initial commit with README.md

### Step 2 — Claude Code Setup
- [ ] Install Claude Code if not present: `npm install -g @anthropic-ai/claude-code`
- [ ] Create .claude/ directory structure:
mkdir -p .claude/hooks .claude/context .claude/skills
- [ ] Copy pre-session.sh from meta-ads-agent: `.claude/hooks/pre-session.sh`
- [ ] Make executable: `chmod +x .claude/hooks/pre-session.sh`
- [ ] Create CLAUDE.md with project summary
- [ ] Create REFERENCES.md with business context
- [ ] Install skills: `npx agent-skills-cli@latest add @Jeffallan/claude-skills`

### Step 3 — Repomix
- [ ] Install if not present: `npm install -g repomix`
- [ ] Run initial pack: `repomix /path/to/project`
- [ ] Verify .claude/context/codebase-context.xml was created

### Step 4 — Supabase
- [ ] Create new Supabase project (or reuse existing)
- [ ] Copy URL and anon key to project config
- [ ] Run initial SQL schema in SQL editor
- [ ] Enable RLS on ALL tables immediately
- [ ] Create RLS policies: Users can only see their own data
- [ ] Enable pgcrypto: `CREATE EXTENSION IF NOT EXISTS pgcrypto;`
- [ ] Disable email confirmation for development: Authentication → Settings
- [ ] Create profiles table with handle_new_user() trigger

### Step 5 — Hosting
- [ ] Connect repo to Vercel (import project in Vercel dashboard)
- [ ] Set up git remote: `git remote add origin [url]`
- [ ] Set rebase strategy: `git config pull.rebase true`
- [ ] Test deployment: push to main → verify Vercel deploys (~30 seconds)
- [ ] Get live URL and save it

### Step 6 — API Keys
- [ ] Add all required keys to Supabase user_keys table
- [ ] Never hardcode API keys in source code
- [ ] Use environment variables for server-side keys
- [ ] pgcrypto encryption for keys stored in database

---

## 🏗️ ARCHITECTURE RULES

### Before Writing Any Code
1. Read all reference documents
2. Activate architecture-designer skill
3. Map out: inputs → process → outputs for the feature
4. Identify which Supabase tables are needed
5. Identify which existing functions can be reused
6. Get plan approved before writing code

### Database Design
- Every table needs: id (uuid), user_id, created_at
- Every table needs RLS enabled immediately after creation
- Every table needs at least one RLS policy before any data touches it
- Use `gen_random_uuid()` for primary keys
- Use `timestamp with time zone` for all timestamps
- Add `IF NOT EXISTS` to all CREATE TABLE statements
- Add `IF NOT EXISTS` to all ALTER TABLE ADD COLUMN statements
- Foreign keys always reference with `on delete cascade`

### Authentication
- Always use `onAuthStateChange` not `getSession()` alone for session restore
- Use `getUser()` not `getSession()` inside data-fetching functions (validates token server-side)
- Store session in localStorage with named key to avoid collisions
- Never trust `getSession()` for RLS-protected reads — token may be stale

### API Keys Storage
- Store in Supabase user_keys table, never in localStorage alone
- Encrypt with pgcrypto before storing
- Load via RPC function that decrypts server-side
- Fallback to direct read if RPC not deployed yet

### CSS Rules
- Never use `inset` shorthand — use explicit `top/right/bottom/left` (browser compatibility)
- Always set `position:relative; z-index:200` on header to prevent overlay blocking
- Use explicit `top:0;right:0;bottom:0;left:0` on modals not `inset:0`
- Test button clicks after adding any fixed/absolute positioned elements

### JavaScript Rules
- Check brace balance before every commit using Node.js (not Python — Python has false positives with regex literals)
- Use `?.` optional chaining on any DOM element that might not exist yet
- Hidden panels: populate input fields when panel opens, not when data loads (DOM elements may not exist yet)
- Never populate form inputs inside hidden `display:none` panels
- Use `async/await` consistently — never mix with `.then()` chains in the same function

---

## 🔄 DEPLOYMENT WORKFLOW

### Standard Push (Every Session)
```bash
git add [files]
git commit -m "descriptive message"
git push origin main
```
Vercel auto-deploys on push. No further action needed.

### If Merge Conflict
```bash
git fetch origin
git reset --hard origin/main
git cherry-pick [your-commit-hash]
git push origin main
```

### If Remote Ahead
```bash
git pull --rebase origin main && git push origin main
```

### Never Do
- Never `git push --force` without confirming what will be lost
- Never commit with unbalanced JS braces
- Never push API keys or secrets to GitHub
- Set environment variables in Vercel dashboard, not in source code

---

## 🐛 DEBUGGING RULES

### When a Bug Appears
1. Activate `debugging-wizard` skill first
2. Read the relevant function completely before touching it
3. State the root cause in plain English before writing any fix
4. Fix the root cause — never patch symptoms
5. Verify fix with brace balance check
6. Test in browser before pushing

### Common Bugs We've Hit (Learn From These)

**Bug: API keys not loading after page refresh**
Root cause: `getSession()` returns stale JWT → RLS blocks the read → silently shows "no keys"
Fix: Use `onAuthStateChange` for boot + `getUser()` inside data-fetching functions

**Bug: Buttons not clicking in header/settings**
Root cause: CSS `inset` shorthand not parsing → overlay covers header
Fix: Replace `inset:0` with explicit `top:0;right:0;bottom:0;left:0` + set `z-index:200` on header

**Bug: Settings panel renders empty**
Root cause: CSS `inset` on overlay causing zero-height collapse
Fix: Same as above — explicit positioning

**Bug: Form inputs empty after data loads**
Root cause: Populating inputs while panel is hidden (`display:none`)
Fix: Call `populateInputs()` when panel opens, not when data loads

**Bug: JS brace balance false positive**
Root cause: Python regex parser counts braces inside regex literals like `/"/g`
Fix: Always use Node.js for brace balance: `node -e "require('fs').readFileSync('index.html')" 2>&1`

**Bug: Supabase upsert silently failing**
Root cause: Missing `onConflict` parameter or wrong column name
Fix: Always include `{ onConflict: 'user_id' }` and verify column exists first

**Bug: RLS blocking reads despite valid session**
Root cause: JWT expired → `auth.uid()` returns null → policy fails silently as PGRST116
Fix: Use `getUser()` before any RLS-protected query to force token refresh

---

## 📦 COMMAND STRUCTURE RULES

### When Writing Claude Code Commands
1. Start with: "Read REFERENCES.md first. Then use [skill] skill."
2. Break large features into 2 commands maximum per session
3. Always include execution order at the end
4. Always end with: "Check JS brace balance before committing. Push to GitHub."
5. Never put more than 3 major features in one command
6. Test Command 1 before running Command 2

### Command Size Guidelines
- Small (1 feature, <100 lines): 1 command, 1 session
- Medium (2-3 features, 100-300 lines): 2 commands, 1 session
- Large (full panel rebuild, 300-500 lines): 2 commands, 2 sessions
- Huge (architecture change): Plan first, then 3+ commands over multiple sessions

---

## 🔐 SECURITY RULES

### Never Do
- Never store API keys in localStorage as primary storage
- Never hardcode encryption passphrases in source code (move to env var before production)
- Never disable RLS on any table
- Never use `service_role` key in client-side code
- Never share GitHub tokens in chat — revoke immediately if exposed
- Never commit .env files

### Always Do
- Enable RLS on every table immediately after creation
- Use `to authenticated` on all RLS policies
- Encrypt sensitive data with pgcrypto before storing
- Use HTTPS only (Vercel handles this automatically)
- Rotate API keys if they appear in any chat or commit

---

## 📋 SESSION START CHECKLIST

Every time you start a Claude Code session:
- [ ] `cd /home/admin/[project]` — navigate to project
- [ ] `claude` — start Claude Code (pre-session.sh runs Repomix automatically)
- [ ] Tell Claude: "Read REFERENCES.md and [any framework docs] first"
- [ ] State what you're building this session
- [ ] Activate relevant skills before writing code

---

## 📋 SESSION END CHECKLIST

Before ending every Claude Code session:
- [ ] All changes committed and pushed to GitHub
- [ ] Vercel deploy confirmed (auto-deploys ~30s after push — check https://meta-ads-agent-cyan.vercel.app/)
- [ ] Live URL tested in browser
- [ ] No debug console.log statements left in code
- [ ] REFERENCES.md updated if anything changed
- [ ] Framework docs updated if agent architecture changed

---

## 🛠️ SKILLS TO USE (When)

| Situation | Skill to activate |
|-----------|------------------|
| Starting any new feature | architecture-designer |
| Bug is hard to find | debugging-wizard |
| Auth or key storage work | secure-code-guardian |
| Supabase SQL or RLS | postgres-pro + sql-pro |
| Vanilla JS optimization | javascript-pro |
| Building React components | react-expert |
| API design | api-designer |
| Security review | security-reviewer |
| Code quality check | fullstack-guardian |

---

## 📁 STANDARD PROJECT FILE STRUCTURE

Every Runbase project should have:
project-root/

├── index.html              ← main app file (or src/ for React)

├── CLAUDE.md               ← Claude Code session starter

├── REFERENCES.md           ← business context + reference repos

├── BUILD_RULES.md          ← this file (copy to every project)

├── [TOOL]_FRAMEWORK.md     ← agent architecture for this tool

├── setup-encryption.sql    ← Supabase pgcrypto setup

├── save-sop.js             ← SOP document saver

├── SOP.md                  ← standard operating procedure

├── .claude/

│   ├── hooks/

│   │   └── pre-session.sh  ← auto-runs Repomix

│   ├── context/

│   │   └── codebase-context.xml  ← Repomix output

│   └── skills/             ← installed Claude Code skills

├── .gitignore

└── README.md

---

## 🎯 QUALITY STANDARDS

### Before Shipping Any Feature
- [ ] Works on page refresh (no state lost)
- [ ] Works after sign out and sign back in
- [ ] API keys persist across sessions
- [ ] No console errors in browser DevTools
- [ ] All buttons clickable (no z-index issues)
- [ ] Mobile responsive (basic check)
- [ ] Data saves to Supabase correctly
- [ ] RLS policies verified — users can only see their own data

### Code Quality
- [ ] No debug `alert()` or `console.log()` statements
- [ ] No hardcoded user IDs or test data
- [ ] No TODO comments in production code
- [ ] All async functions have try/catch
- [ ] All Supabase calls check for errors
- [ ] All AI calls check for ⚠️ error strings before parsing
