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

## Slide Structure (6 slides)

| Slide | Content |
|-------|---------|
| 1 | Cover — headline, source badge, one-sentence hook |
| 2 | Story A — one vivid detail, left/right split layout |
| 3 | Story B — second angle or quote |
| 4 | Big Picture — two cards: the rule / the tension |
| 5 | Implications for Accounting Students — why this matters, connections to financial statements, disclosures, standards, or career relevance |
| 6 | Read More — prominent link to original article |

**Slide 5 guidance (Implications):**
- Explain *how* and *why* this story matters to accounting majors
- Connect to specific accounting concepts: financial statement line items, disclosure requirements (ASC, IFRS), audit risk, tax treatment, management reporting, etc.
- Use concrete examples: "This affects how firms disclose R&D costs under ASC 730" or "Auditors must now assess AI-generated estimates under AS 2501"
- Keep it actionable: what should an accounting student watch for in real filings?

**Design rules:**
- One idea per slide, minimal text
- CMU maroon `#6A0032` + gold `#F9A21B`
- Large fonts, high contrast — built for projection
- Keyboard navigation: ← → arrows, ESC returns to index
- **Must work on both desktop and mobile** — see responsive requirements below

---

## Responsive Design Requirements

Every slide deck must include a `@media (max-width: 640px)` block and touch swipe JS. Use `20260324-meta-harmed-children.html` as the canonical template.

### Mobile CSS block (add at end of `<style>`)

```css
@media (max-width: 640px) {
  #header { padding: 0 16px; height: 44px; }
  .h-left, .h-right { display: none; }
  .h-mid { font-size: 12px; }

  #deck { top: 44px; bottom: 48px; }
  #progress { bottom: 48px; }

  .slide {
    width: 100vw;
    height: calc(100dvh - 44px - 48px - 10px);
    border-radius: 6px;
    overflow-y: auto;
  }

  /* Cover */
  .slide-cover { padding: 28px 22px; gap: 16px; }
  .slide-cover h1 { font-size: 24px; }
  .slide-cover .subtitle { font-size: 14px; padding-left: 12px; }

  /* Story: collapse 2-column → single column */
  .slide-story { grid-template-columns: 1fr; height: auto; min-height: 100%; }
  .story-left  { padding: 22px 22px 14px; gap: 10px; justify-content: flex-start; }
  .story-left h2 { font-size: 20px; }
  .story-left .role { font-size: 13px; }
  .story-right { padding: 14px 22px 22px; gap: 14px; }
  .story-right .big-quote { font-size: 15px; }
  .story-right .big-quote::before { font-size: 48px; }
  .story-right .detail { font-size: 14px; padding: 14px 16px; }

  /* Big picture: collapse 2-column cards → single column */
  .slide-big { padding: 28px 20px; gap: 18px; }
  .slide-big h2 { font-size: 22px; }
  .two-points { grid-template-columns: 1fr; gap: 12px; }
  .point-card { padding: 16px 18px; }
  .point-card p { font-size: 15px; }

  /* Implications */
  .slide-implications { padding: 24px 18px; gap: 14px; }
  .slide-implications h2 { font-size: 19px; }
  .impl-list { gap: 10px; }
  .impl-item { padding: 12px 14px; gap: 10px; }
  .impl-icon { font-size: 18px; min-width: 22px; }
  .impl-label { font-size: 10px; }
  .impl-body  { font-size: 13px; }

  /* Read more */
  .slide-read { padding: 32px 22px; gap: 20px; }
  .slide-read h2 { font-size: 26px; }
  .slide-read p  { font-size: 15px; }
  .wsj-link, .ft-link {
    font-size: 15px; padding: 14px 24px;
    width: 100%; text-align: center;
  }

  /* Footer */
  #footer { height: 48px; padding: 0 16px; }
  #nav-hint { display: none; }
  #back-link { font-size: 12px; }
  #counter   { font-size: 12px; }

  /* Nav buttons */
  .nav-btn { width: 36px; height: 36px; font-size: 16px; }
  #btn-prev { left: 4px; }
  #btn-next { right: 4px; }
}
```

If the slide has a numeric comparison layout (like the KPMG fee slide), also add:

```css
  .fee-comparison { grid-template-columns: 1fr; gap: 10px; }
  .fee-arrow { font-size: 28px; padding: 0; transform: rotate(90deg); }
  .fee-amount { font-size: 38px; }
  .fee-delta  { font-size: 16px; padding: 12px 16px; }
```

### Touch swipe JS (add inside `<script>`, before `update()`)

```js
let touchStartX = 0, touchStartY = 0;
document.addEventListener('touchstart', e => {
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
}, { passive: true });
document.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - touchStartX;
  const dy = e.changedTouches[0].clientY - touchStartY;
  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) navigate(dx < 0 ? 1 : -1);
}, { passive: true });
```

### Key rules
- Use `100dvh` (not `100vh`) for slide height — fixes iOS Safari address-bar bug
- Story slides: always `grid-template-columns: 1fr` on mobile with `height: auto; min-height: 100%`
- Tall slides (Implications, Big Picture with long text) must have `overflow-y: auto` on `.slide` so they scroll rather than clip

---

## Tags

Each article is tagged with one or more of the following on the main index page:

| Tag | Scope |
|-----|-------|
| `FinAcc` | Financial accounting, GAAP/IFRS standards, financial statements, disclosures |
| `MgtAcc` | Managerial/cost accounting, internal reporting, performance measurement |
| `Tax` | Tax law, tax planning, IRS/regulatory guidance |
| `Auditing` | External/internal audit, PCAOB/AICPA standards, audit risk |
| `Market` | Capital markets, investor behavior, stock prices, analyst forecasts |

- Assign all tags that apply — one article can carry multiple tags
- Tags appear as colored badges on the index card for each slide deck

---

## Article Intake

WSJ and FT are behind paywalls that block Claude Code's WebFetch tool.
**Standard intake:** open article in browser → Select All → Copy → paste into `.txt` file.

---

## Currently Published

| Date | Title | Source | Tags |
|------|-------|--------|------|
| Feb 6, 2026 | KPMG Pressed Its Auditor to Pass On AI Cost Savings | FT | `Auditing` `Market` |
| Mar 24, 2026 | Landmark Verdict Says Meta Harmed Children | WSJ | `FinAcc` `Auditing` `Market` |
| Apr 11, 2026 | The Dirty Job That Accountants Desperately Wish AI Would Take Over | WSJ | `Auditing` `FinAcc` `MgtAcc` |
