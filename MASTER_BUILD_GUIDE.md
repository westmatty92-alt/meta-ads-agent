# Runbase — Master Build Guide
# Copy this to EVERY new project before starting
# This document captures everything learned building Runbase Pulse
# Last updated: June 2026

---

## 🚀 HOW TO START ANY NEW PROJECT

1. Create GitHub repo
2. Clone to local machine
3. Copy these files from meta-ads-agent:
   - MASTER_BUILD_GUIDE.md (this file)
   - SKILLS_GUIDE.md
   - BUILD_RULES.md
   - SUPABASE_FIXES.md
   - .claude/hooks/pre-session.sh
4. Create CLAUDE.md for the new project
5. Create REFERENCES.md for the new project
6. Run: npx agent-skills-cli@latest add @Jeffallan/claude-skills
7. Start Claude Code: cd /path/to/project && claude
8. First command: "Read MASTER_BUILD_GUIDE.md and REFERENCES.md first"

---

## 🔴 CRITICAL RULES (Never Break)

1. Read reference docs at the start of every session
2. Use architecture-designer skill BEFORE writing any code
3. Check JS brace balance with Node.js before every commit
4. Every module must be iFrame-embeddable for GHL from day one
5. Never use Replit git UI — shell only (bash sync.sh)
6. Never hardcode API keys or tokens in source code
7. Always add WITH CHECK to RLS policies
8. Always add UNIQUE constraint before using onConflict in upsert
9. shadcn/ui first — check if component exists before building from scratch
10. Human checkpoint required between every AI agent phase

---

## 🐛 BUGS WE HIT AND HOW WE FIXED THEM

### BUG 1: API keys not loading after page refresh
**Symptom:** Keys save fine but disappear on refresh
**Root cause:** getSession() returns stale JWT → RLS blocks read → shows "no keys"
**Fix:** Use onAuthStateChange for boot + getUser() inside data-fetching functions
**Code pattern:**
```javascript
// WRONG
const { data: { session } } = await sb.auth.getSession();

// CORRECT  
const { data: { user } } = await sb.auth.getUser();
```

### BUG 2: Buttons not clicking (header/settings)
**Symptom:** Clicking Save, Sign Out, or header buttons does nothing
**Root cause:** CSS inset shorthand not parsing → overlay covers header → z-index conflict
**Fix:** Replace inset:0 with explicit top/right/bottom/left + set z-index:200 on header
```css
/* WRONG */
.overlay { inset: 0; }

/* CORRECT */
.overlay { top:0; right:0; bottom:0; left:0; }
.hdr { position:relative; z-index:200; }
```

### BUG 3: Form inputs empty after data loads
**Symptom:** Data loads from Supabase but form fields stay empty
**Root cause:** Populating inputs while panel is hidden (display:none)
**Fix:** Call populateInputs() when panel OPENS not when data loads

### BUG 4: JS brace balance false positive
**Symptom:** Python brace counter shows imbalanced but code works fine
**Root cause:** Python regex parser counts braces inside regex literals like /"/g
**Fix:** Always use Node.js for brace balance check:
```bash
node -e "require('fs').readFileSync('index.html','utf8')" 2>&1
```

### BUG 5: Supabase upsert silently failing (no error shown)
**Symptom:** Save button shows success but data never appears in table
**Root cause 1:** Missing UNIQUE constraint on conflict column (error code 42P10)
**Root cause 2:** RLS policy missing WITH CHECK clause (inserts blocked silently)
**Fix:**
```sql
-- Add unique constraint
ALTER TABLE your_table ADD CONSTRAINT name UNIQUE (column);

-- Fix RLS policy
DROP POLICY "name" ON your_table;
CREATE POLICY "name" ON your_table
FOR ALL TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

### BUG 6: RLS blocking reads despite valid session
**Symptom:** PGRST116 error even though user is logged in
**Root cause:** JWT expired → auth.uid() returns null → policy fails
**Fix:** Use getUser() before any RLS-protected query to force token refresh

### BUG 7: Replit corrupting git history
**Symptom:** Git log shows "Published your App" commits, real commits disappear
**Root cause:** Replit's git UI creates its own commits on top of real ones
**Fix:** Never use Replit git UI. Shell only:
```bash
bash sync.sh
```
**Nuclear fix if corrupted:**
```bash
# In Claude Code terminal
git add -A && git commit -m "restore" && git push origin main --force
# In Replit Shell
bash sync.sh
```

### BUG 8: Product deletes visually but returns on refresh
**Symptom:** Delete button removes card from UI but it comes back after refresh
**Root cause:** Delete only removes from DOM, not from Supabase
**Fix:** Always delete from Supabase first, then remove from DOM:
```javascript
async function deleteProduct(id) {
  await sb.from('products').delete().eq('id', id);
  document.querySelector('[data-product-id="' + id + '"]')?.remove();
}
```

### BUG 9: Brand Kit duplicate ID conflict
**Symptom:** Color picker in Base Profile not working, Add Color button does nothing
**Root cause:** Two elements with same ID (bk-palette) — getElementById finds wrong one
**Fix:** Rename Base Profile version to bp-colors-list to avoid collision

### BUG 10: onAuthStateChange vs getSession race condition
**Symptom:** App initializes before session is confirmed, data loads with null user
**Root cause:** getSession() doesn't validate token server-side
**Fix:** Use onAuthStateChange for all session initialization:
```javascript
let _appBooted = false;
sb.auth.onAuthStateChange((event, session) => {
  if (session && !_appBooted) {
    _appBooted = true;
    initApp(session.user);
  } else if (!session && !_appBooted) {
    _appBooted = true;
    showAuthScreen();
  }
});
```

---

## 🗄️ SUPABASE SETUP TEMPLATE (Every New Table)

```sql
-- 1. Create table with required columns
CREATE TABLE IF NOT EXISTS your_table (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  business_id uuid REFERENCES businesses(id) ON DELETE CASCADE,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  -- your columns here
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- 2. Add UNIQUE constraint (required for upsert onConflict)
ALTER TABLE your_table 
  ADD CONSTRAINT your_table_business_id_unique UNIQUE (business_id);

-- 3. Enable RLS
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- 4. Create policy WITH CHECK (critical — without this inserts are blocked)
CREATE POLICY "users_own_your_table" ON your_table
FOR ALL
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

---

## 💻 REPLIT + GITHUB WORKFLOW

### Rules
- NEVER click Sync in Replit UI
- NEVER click Republish in Replit UI  
- ALWAYS use bash sync.sh in Replit Shell
- ALWAYS let Claude Code handle git commits

### Setup sync.sh in every project
```bash
cat > sync.sh << 'EOF'
#!/bin/bash
echo "🔄 Syncing from GitHub..."
git fetch origin
git reset --hard origin/main
echo "✅ All changes synced"
echo "🟢 Done. App is live."
EOF
chmod +x sync.sh
```

### Daily workflow
Claude Code builds → git push to GitHub

Replit Shell → bash sync.sh

Browser Ctrl+Shift+R → changes live

### If git corrupted
```bash
# Claude Code terminal
git add -A && git commit -m "restore: full build" && git push origin main --force
# Replit Shell  
git init && git remote add origin [url] && git fetch origin && git checkout -B main origin/main
bash sync.sh
```

### GitHub token setup
- Scope: repo only
- Expiry: No expiration
- Set: git remote set-url origin https://[TOKEN]@github.com/[user]/[repo].git
- Revoke immediately if exposed in any chat or commit log

---

## 🎨 CSS RULES

```css
/* NEVER use inset shorthand — use explicit values */
/* WRONG */ .overlay { inset: 0; }
/* CORRECT */ .overlay { top:0; right:0; bottom:0; left:0; }

/* ALWAYS set z-index on header to prevent overlay blocking */
.hdr { position:relative; z-index:200; }

/* Modal overlays need explicit positioning */
.modal-overlay { 
  position:fixed; 
  top:0; right:0; bottom:0; left:0; 
  z-index:100; 
}
```

---

## 🔐 SECURITY RULES

1. Never store API keys in localStorage as primary storage
2. Never hardcode encryption passphrases (use env vars in production)
3. Always enable RLS immediately after table creation
4. Always use TO authenticated not TO public on RLS policies
5. Always include WITH CHECK on RLS policies
6. Never use service_role key in client-side code
7. Revoke GitHub tokens immediately if exposed in chat
8. Never commit .env files to GitHub

---

## 📦 STANDARD PROJECT FILES

Every project needs these files:
project/

├── index.html (or src/ for React)

├── CLAUDE.md              ← session starter + doc index

├── MASTER_BUILD_GUIDE.md  ← this file

├── REFERENCES.md          ← business context

├── BUILD_RULES.md         ← build standards

├── SUPABASE_FIXES.md      ← DB debugging

├── SKILLS_GUIDE.md        ← Claude Code skills

├── sync.sh                ← Replit sync command

├── .gitignore             ← exclude node_modules etc

└── .claude/

└── hooks/

└── pre-session.sh ← auto-runs Repomix

---

## 🛠️ SKILLS QUICK REFERENCE

| Situation | Skill |
|-----------|-------|
| New feature | architecture-designer |
| Bug hunting | debugging-wizard |
| Auth/security | secure-code-guardian |
| Supabase/SQL | postgres-pro + sql-pro |
| Vanilla JS | javascript-pro |
| React components | react-expert + typescript-pro |
| Code review | fullstack-guardian |
| Before production | security-reviewer |
| AI prompts | prompt-engineer |

---

## 📋 SESSION START CHECKLIST

- [ ] cd to project directory
- [ ] Run claude (pre-session.sh runs Repomix automatically)
- [ ] Tell Claude: "Read CLAUDE.md and REFERENCES.md first"
- [ ] State what you are building today
- [ ] Activate relevant skills before writing code

## 📋 SESSION END CHECKLIST

- [ ] All changes committed and pushed to GitHub
- [ ] bash sync.sh run in Replit Shell
- [ ] Live URL tested in browser
- [ ] No debug console.log left in code
- [ ] REFERENCES.md updated if business context changed
- [ ] MASTER_BUILD_GUIDE.md updated if new bug pattern found
