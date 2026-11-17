---
name: acc-lecture-materials
description: Make ACC250 (and other accounting course) teaching materials in Jaeyoon Yu's own style - slides that look like the Beamer lecture notes, in-class worksheets with answer keys, and "Accounting in the News" decks built on real company filings. Use whenever asked to make or revise slides, a worksheet, a handout, an in-class case, or a news deck for a course on jaeyoonyu.github.io.
---

# ACC course materials in Jaeyoon's style

These rules come from the instructor's own feedback. Follow them without being asked again.

## Before writing anything

1. **Match the lecture notes' scope.** Read the chapter handout (`assets/ACC250/ChN-Handout.pdf`, e.g. with `pypdf`) and use its terms, notation and methods. Anything the notes mark "Appendix (Not for exam)" stays out of worksheets and slides (e.g. Ch8 uses the % of credit sales method, not aging).
2. **Real numbers must be verified.** Use the company's 10-K/10-Q/8-K (SEC EDGAR) or its earnings release; cross-check across sources. If a line is computed from reported totals, say so in a footnote. If the user's figure disagrees with the filing, use the filing and tell the user.
3. **Ask nothing you can decide.** Pick sensible defaults and mention them at the end.

## Slides: look like the Beamer lecture notes

Template: `_tools/acc250_case/gen_berkshire_slides.py` (copy its CSS, footer and navigation script).

- **4:3**, 1200×900 stage, white background, sans-serif.
- Frame title in Beamer blue (`#3333b3`) with a thin blue rule underneath. Title slide: "ACC250: Intro to Financial Accounting" / deck title / "Jaeyoon Yu, Ph.D. / Central Michigan University", centered.
- Footer bar in three blue segments: course name | topic | `n / N`.
- Round blue bullets; numbered items in small blue circles.
- Tables: booktabs style (rule above and below the header, thick rule at the bottom), sized to their content. Highlight rows in pink (`#f6c6c6`) or yellow (`#fff26b`).
- Examples start with a yellow, underlined, bold **EX.** label.
- **Journal entries** follow the lecture notes exactly: a rounded red-bordered box; the bold date (e.g. `Jan 1:`) at left, then a vertical rule; the debit account flush left and the credit account **indented** under it; the debit amount in its own column and the credit amount in a **separate column further right** (never both amounts in one column). Build it as a small table (date | account | debit | credit) so the columns line up.
- **One column.** Never put things side by side unless the slide is literally comparing two things (and even then prefer a table).
- **No "Claude style"**: no cream backgrounds, cards with colored left borders, eyebrow labels, pill chips, big tinted "key idea" boxes or decorative icons.
- **Never all caps.** No `text-transform: uppercase`, no letter-spaced small caps labels.
- Company + CEO introduction goes on **one** slide.
- Photos: freely licensed (Wikimedia Commons: public domain or CC BY), with the credit and license in a small caption. Save them in `assets/ACC250/img/`. Prefer people (CEO) over buildings.
- **Show data as a chart, not a table, when the point is the shape of the numbers**: shares of a whole (a portfolio, revenue by segment) are a **pie chart**; flows through the income statement are a Sankey (`_tools/acc250_case/sankey.py`). Draw charts as inline SVG (see `pie()` in `gen_berkshire_slides.py`): percent inside each slice, label and dollar amount outside, the total and the "as of" date underneath. Keep a table only when students need to read or compute exact numbers.
- **Use company logos** whenever companies are named in a chart or list: download the SVG from Wikimedia Commons (`https://commons.wikimedia.org/wiki/Special:FilePath/<File>.svg`, with a descriptive User-Agent; space requests a few seconds apart), check the file has no `<script>`, save it in `assets/ACC250/img/logos/`, and note "Logos via Wikimedia Commons; trademarks of their owners." on the slide.
- End with discussion questions, then a Sources slide with links.

## Worksheets (one sheet, printed on Letter)

Generators: `_tools/acc250_case/` (`gen_case.py`, `gen_worksheets.py`, `gen_ch8_practice.py`, shared `case.css`).

- Student version and answer key have the **identical layout**. The key only fills the blanks in red. **No explanations or worked steps in the key.**
- Real-company sheets: SEC filing link at the top; statements in 10-K format ($ on first and total lines, single rule before subtotals, double rule under totals, parentheses for negatives); statement titles on a **yellow background**; side-by-side statements are fine (that is a comparison of statements).
- Questions under the statements ask for **amounts**, worded by concept so students who know the term can find it (e.g. "How much does Walmart expect to collect from its customers?"). Say *expense recorded*, never *spend*, for accrual amounts. Add one line stating the date to answer as of.
- Definitions go on the back as **Accounts & Terms**: a plain list, no journal entries.
- Procedure practice (e.g. Ch8): per month, a timeline graphic, then journal entries next to the T-account (A/R), the AJE next to the ADA T-account, then a **Summary** at the bottom: inputs (e.g. credit sales, then BDE on the line below) and one vertical table (Gross A/R / Less: ADA / Net A/R) with a "What it means" column (Total A/R / Noncollectible A/R (estimated) / Collectible portion of A/R).
- Use different numbers for different amounts in the same month so they cannot be confused (e.g. a write-off and BDE must not both be 100).
- Journal entry tables: no underlines; keep the writing space.
- **Every table row stays on one line**: no wrapped cells (`white-space:nowrap` on `th`/`td`; shorten labels or let the table scroll horizontally on the web instead).
- Compact tables; never stretch a table to full width just to fill space. Spread free space between sections, not at the bottom.
- Footnotes are real footnotes: a marker (*, †, ‡) in the text and a black footnote with a rule at the page bottom. Never small gray text dropped under a table. Notes about simplifications (e.g. "Cost of goods sold entries are omitted for brevity. See Ch6.") are footnotes.
- Check every page fits (one page for openers, front/back for practice) by rendering to PDF with Playwright and looking at the images.

## Notation (from the lecture notes)

`Cash (+A)`, `A/R (+A)`, `Sales Rev (+R)` (not "Sales revenues"), `BDE (+E)`, `ADA (+xA, −A)`, `ADA (−xA, +A)`, `A/R (−A)`, `CGS`, `Inventory`, `Treasury Stock (+xSE, −SE)`. Gross A/R, ADA, Net A/R. The A/R T-account is just "A/R" (the AJE does not touch A/R), balance line "End. bal.".

## Publishing

1. Put files in `assets/ACC250/` (HTML + PDF + `-Key.pdf`), generators in `_tools/acc250_case/`.
2. Link new material on the Test page (`test.md`) first. Chapter material later goes in the ACC250 Lecture Notes table's **Worksheet** column (`ACC250.md`).
3. Every link to `/assets/...pdf|html` carries `?v=<first 8 hex of md5>`; recompute only for the files you changed (do not restamp unrelated links).
4. Commit on the working branch, push, open a PR to `main`, merge it, and tell the user it takes 1-2 minutes to show on the site.
5. Show the user screenshots of the result (student and key pages, or a grid of slides).
