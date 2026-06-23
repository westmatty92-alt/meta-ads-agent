# Baseleap Pulse — Claude Code Project Context

## How to start every session
1. Read REFERENCES.md
2. Read META_ADS_AGENT_FRAMEWORK.md  
3. If .claude/context/codebase-context.xml exists, it contains the full packed codebase

## Project
Baseleap Pulse — Meta Ads Agent (Tool 1 of 17 in Baseleap CRM platform)
Single file app: index.html (~4500 lines)
Stack: Vanilla JS + Supabase + Claude API + Apify + GHL

## Live URL
https://meta-ads-agent-cyan.vercel.app/
Deployed via Vercel — every git push deploys automatically in ~30 seconds.
Never use Replit for deployment — Vercel handles all deployments automatically.

## Key files
- index.html — entire application
- REFERENCES.md — business model, all 17 tools, tech stack, reference repos
- META_ADS_AGENT_FRAMEWORK.md — agent architecture blueprint
- setup-encryption.sql — pgcrypto RPC functions for Supabase

## Rules
- Always check JS brace balance before committing
- Use architecture-designer skill before building new features
- Use debugging-wizard skill for bugs
- Use postgres-pro skill for Supabase/SQL work
- Every module must be iFrame-embeddable for GHL

## Todo List
Baseleap Pulse (Tool 1): https://app.notion.com/p/3886d6be0d4181c5973bc130325f7ff8
At session start: fetch this page and suggest highest priority incomplete item.
