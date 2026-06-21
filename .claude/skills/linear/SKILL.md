---
name: linear
description: Linear-style dark SaaS design — deep navy backgrounds, teal accent, tight typography, high-density data UI optimized for tools and dashboards.
license: MIT
metadata:
  author: Runbase (custom — linear slug not in typeui.sh registry)
---

# Runbase Linear Design System Skill

## Mission
You are an expert UI implementer for Runbase — a Linear-style dark SaaS platform.
Apply this design system consistently across ALL Runbase tools (Pulse, SR&ED, Grant Writer, etc.).
Every tool must look identical — same colors, same spacing, same components.

## Color Tokens (NEVER deviate)
```css
--bg-primary: #0A1628;     /* Main background */
--bg-surface: #111D35;     /* Cards and panels */
--bg-elevated: #162240;    /* Elevated elements, dropdowns */
--border: #1E3A5F;         /* All borders */
--border-subtle: #162240;  /* Subtle dividers */
--t1: #E8EDF5;             /* Primary text */
--t2: #7A95B8;             /* Secondary text */
--t3: #4A6080;             /* Muted text, placeholders */
--volt: #00D4A0;           /* Primary accent — teal green */
--accent: #2563EB;         /* Secondary accent — blue */
--red: #FF5050;            /* Errors, risk flags, delete */
--yellow: #F5C842;         /* Warnings, pending states */
--green: #00C896;          /* Success, approved states */
```

## Typography
- Display/Hero: Barlow ExtraBold 800
- Section headers: Barlow SemiBold 600
- Body text: Inter Regular 400
- Labels/caps: Inter Medium 500 uppercase letter-spacing
- Data/metrics: Inter Bold 700
- NEVER use system fonts — always load Barlow + Inter from Google Fonts

## Spacing System (4px base unit)
- Component padding: 12px | 16px | 20px | 24px
- Section gaps: 24px | 32px | 48px
- Border radius: 6px (inputs) | 8px (buttons/cards) | 12px (modals) | 16px (large panels)
- NEVER use arbitrary pixel values outside this scale

## Component Standards

### Buttons
- Primary: `background: var(--volt); color: #000; font-weight: 600; border-radius: 8px; padding: 10px 20px;`
- Secondary: `border: 1px solid var(--border); background: transparent; color: var(--t1); border-radius: 8px; padding: 10px 20px;`
- Danger: `background: var(--red); color: #fff; border-radius: 8px; padding: 10px 20px;`

### Inputs
```css
border: 1px solid var(--border);
border-radius: 6px;
padding: 10px 12px;
background: var(--bg-elevated);
color: var(--t1);
font-size: 13px;
```
Focus state: `border-color: var(--volt); outline: none;`

### Cards
```css
background: var(--bg-surface);
border: 1px solid var(--border);
border-radius: 12px;
padding: 20px;
```

### Modals
```css
background: var(--bg-surface);
border: 1px solid var(--border);
border-radius: 16px;
max-width: 520px;
padding: 24px;
```

### Status Badges
```css
border-radius: 20px;
padding: 4px 10px;
font-size: 11px;
font-weight: 600;
```

## Status Color System
| State | Color | Token |
|-------|-------|-------|
| Approved / Complete | #00C896 | var(--green) |
| In Progress / Working | #00D4A0 | var(--volt) |
| Pending / Awaiting | #F5C842 | var(--yellow) |
| Error / Risk / Delete | #FF5050 | var(--red) |
| Locked / Disabled | #4A6080 | var(--t3) |
| AI Generated badge | #2563EB | var(--accent) |

## CSS Rules (NEVER Break)
- NEVER use `inset` shorthand — use `top/right/bottom/left` explicitly
- ALWAYS set `position: relative; z-index: 200` on header elements
- NEVER use `!important` — fix specificity properly
- ALWAYS use CSS variables for colors — never hardcode hex values
- NEVER use `margin: auto` on flex children — use `justify-content` on parent
- NEVER use system fonts

## Accessibility
- WCAG 2.2 AA contrast minimum
- All interactive elements keyboard-navigable
- Visible focus states using `var(--volt)` outline
- Minimum touch target: 44px

## Cross-Tool Consistency
All Runbase tools share this exact system:
- Runbase Pulse (Meta Ads Agent) — Tool 1 — index.html is the component reference
- SR&ED Grant Writer — Tool 2
- Grant Discovery Engine — Tool 3
- All future tools: copy components from Pulse index.html, never rebuild from scratch

## Before Any UI Work
1. Read this SKILL.md
2. Read MASTER_BUILD_GUIDE.md design system section
3. Check existing components in index.html first
4. Never introduce a new color, font, or spacing value not in this system

## Quality Gates
- [ ] All colors use CSS variables (no hardcoded hex)
- [ ] Fonts are Barlow or Inter only
- [ ] Spacing follows the 4px scale
- [ ] Border radius matches component type
- [ ] Status colors match the status color system
- [ ] No `inset` shorthand used
- [ ] Header has `z-index: 200`
- [ ] Works on mobile (min-width: 320px)
- [ ] No `!important` used
