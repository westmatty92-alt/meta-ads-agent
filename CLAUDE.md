# Runbase Pulse — Claude Code Project Context

## How to start every session
1. Read REFERENCES.md
2. Read META_ADS_AGENT_FRAMEWORK.md  
3. If .claude/context/codebase-context.xml exists, it contains the full packed codebase

## Project
Runbase Pulse — Meta Ads Agent (Tool 1 of 17 in Runbase CRM platform)
Single file app: index.html (~3500 lines)
Stack: Vanilla JS + Supabase + Claude API + Apify + GHL

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
