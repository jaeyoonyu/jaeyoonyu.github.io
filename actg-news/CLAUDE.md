# Accounting & Capital Markets News — Working Guide

## Location
This folder lives inside `jaeyoonyu.github.io/actg-news/` and is served at:
`https://jaeyoonyu.github.io/actg-news/`

---

## Folder Structure

```
actg-news/
├── CLAUDE.md            ← this file
├── index.html           ← main news page (auto-updated when slides are added)
├── Articles/            ← drop raw article text files here
│   └── YYYYMMDD-title.txt
└── slides/              ← auto-generated HTML presentations
    └── YYYYMMDD-title.html
```

---

## Workflow

1. Paste article text into `Articles/YYYYMMDD-title.txt`
2. Ask Claude to generate slides for it
3. Claude writes to `slides/` and updates `index.html`
4. From `jaeyoonyu.github.io/`:
   ```
   git add actg-news/
   git commit -m "Add: article title"
   git push
   ```

---

## Article File Naming

```
YYYYMMDD-short-title.txt
```

Examples:
- `20260411-dirty-job-accountants-ai.txt`
- `20260407-kpmg-ai-audit-fees`

---

## Slide Structure (5 slides)

| Slide | Content |
|-------|---------|
| 1 | Cover — headline, source badge, one-sentence hook |
| 2 | Story A — one vivid detail, left/right split layout |
| 3 | Story B — second angle or quote |
| 4 | Big Picture — two cards: the rule / the tension |
| 5 | Read More — prominent link to original article |

**Design rules:**
- One idea per slide, minimal text
- CMU maroon `#6A0032` + gold `#F9A21B`
- Large fonts, high contrast — built for projection
- Keyboard navigation: ← → arrows, ESC returns to index

---

## Article Intake

WSJ and FT are behind paywalls that block Claude Code's WebFetch tool.
**Standard intake:** open article in browser → Select All → Copy → paste into `.txt` file.

---

## Currently Published

| Date | Title | Source |
|------|-------|--------|
| Feb 6, 2026 | KPMG Pressed Its Auditor to Pass On AI Cost Savings | FT |
| Apr 11, 2026 | The Dirty Job That Accountants Desperately Wish AI Would Take Over | WSJ |
