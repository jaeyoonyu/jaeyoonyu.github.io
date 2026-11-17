#!/usr/bin/env python3
"""Buffett letters: accounting themes page + one question sheet (and key) per theme.

Usage (from the repo root): python _tools/buffett/gen_buffett.py
Writes assets/Buffett/Q01.html ... and buffett-letters.md. PDFs are printed separately.
"""
import os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'assets', 'Buffett')
os.makedirs(OUT, exist_ok=True)


def url(y):
    y = int(y)
    if y <= 1997: return f'https://www.berkshirehathaway.com/letters/{y}.html'
    special = {1998: '1998pdf.pdf', 1999: 'final1999pdf.pdf', 2000: '2000pdf.pdf', 2001: '2001pdf.pdf', 2002: '2002pdf.pdf'}
    return 'https://www.berkshirehathaway.com/letters/' + special.get(y, f'{y}ltr.pdf')


# theme, key letters (bold first), difficulty, ACC250, ACC531, quote, questions
# question: ('mc', stem, [options], index of answer) or ('num', stem, answer)
T = [
 ('Economic vs. accounting goodwill', [1983, 1999, 2015], 'Intermediate', 'Ch9', '',
  'We own several businesses that possess economic Goodwill ... far larger than the accounting Goodwill that is carried on our balance sheet. (1983)',
  [('num', 'A company pays $500 million for another company whose identifiable net assets have a fair value of $380 million. How much goodwill does it record ($ millions)?', '120'),
   ('mc', 'Why can a business&rsquo;s economic goodwill be far larger than the goodwill on its balance sheet?',
    ['Goodwill is recorded only when a business is purchased; goodwill a company builds internally is never recorded', 'Goodwill is always amortized to zero within one year', 'Auditors require goodwill to be recorded at half its value', 'Goodwill is a liability, not an asset'], 0)]),
 ('Owner earnings', [1986], 'Intermediate', 'Ch9', '',
  'We consider the owner earnings figure, not the GAAP figure, to be the relevant item for valuation purposes. (1986)',
  [('num', 'Net income is $100, depreciation and amortization are $40, and the capital spending needed just to maintain the business is $50. What are owner earnings (net income + D&amp;A &minus; maintenance capital spending)?', '90'),
   ('mc', 'Compared with EBITDA, owner earnings&hellip;',
    ['subtracts the capital spending needed to keep the business running', 'ignores depreciation', 'adds back income taxes', 'is always larger'], 0)]),
 ('Look-through earnings', [1990, 1991, 1992], 'Advanced', '', '',
  'The retained operating earnings of major investees that, under GAAP accounting, are not reflected in our profits. (1991)',
  [('num', 'Berkshire owns 10% of a company that earns $500 million and pays $100 million of dividends. Berkshire records only its dividends as income. Before taxes, how much of the investee&rsquo;s retained earnings belongs to Berkshire but is not in its profit ($ millions)?', '40'),
   ('mc', 'Look-through earnings add which item to Berkshire&rsquo;s reported operating earnings?',
    ['Berkshire&rsquo;s share of investees&rsquo; retained earnings, less the tax that would be paid if distributed', 'The market value of all stocks owned', 'Insurance float', 'Dividends received'], 0)]),
 ('Stock options are an expense', [1992, 1998, 2007], 'Intro', 'Ch11', '',
  'How many legs does a dog have if you call his tail a leg? Four, because calling a tail a leg does not make it a leg. (1992)',
  [('num', 'A company grants employees options with a total fair value of $12 million that vest evenly over 4 years. How much compensation expense does it record each year ($ millions)?', '3'),
   ('mc', 'Recording stock-option compensation expense&hellip;',
    ['lowers net income but uses no cash', 'lowers cash and net income', 'raises net income', 'affects only the cash flow statement'], 0)]),
 ('Earnings management', [1998, 1992, 2000], 'Intermediate', '', 'Fraud risk',
  'The distortion du jour is the &ldquo;restructuring charge,&rdquo; an accounting entry that ... too often is a device for manipulating earnings. (1998)',
  [('mc', 'A company books an unusually large restructuring charge in a bad year (a &ldquo;big bath&rdquo;). What does this most likely do to the following years&rsquo; reported earnings?',
    ['Makes them look better, because future costs were charged early', 'Makes them look worse', 'Has no effect', 'Eliminates all future expenses'], 0),
   ('mc', 'Buffett writes, &ldquo;We prefer a lumpy 15% return to a smooth 12%.&rdquo; Why should an auditor be skeptical of very smooth earnings?',
    ['Smoothness can come from adjusting estimates and reserves rather than from the business', 'Smooth earnings are illegal under GAAP', 'Auditors cannot audit smooth earnings', 'Smooth earnings mean no taxes are paid'], 0)]),
 ('EBITDA ignores a real cost', [2000, 2002], 'Intro', 'Ch9', '',
  'References to EBITDA make us shudder &mdash; does management think the tooth fairy pays for capital expenditures? (2000)',
  [('num', 'Net income $50, interest $10, income taxes $20, depreciation and amortization $30. What is EBITDA?', '110'),
   ('mc', 'Why does Buffett call depreciation a real cost even though it is a &ldquo;non-cash&rdquo; expense?',
    ['The cash was paid up front when the asset was bought', 'Depreciation is paid in cash every year', 'Depreciation increases taxes owed', 'Depreciation is a liability'], 0)]),
 ('Purchase vs. pooling for acquisitions', [1999, 2000], 'Advanced', '', '',
  'Managements usually detest purchase accounting because it almost always requires that a &ldquo;goodwill&rdquo; account be established and subsequently written off. (1999)',
  [('mc', 'Which method must U.S. companies use today to record an acquisition?',
    ['The acquisition (purchase) method: assets and liabilities at fair value, the excess as goodwill', 'Pooling of interests', 'Either method, at management&rsquo;s choice', 'No entry until the target is sold'], 0),
   ('mc', 'Why did many managers prefer pooling?',
    ['No goodwill was created, so there was no later charge against earnings', 'It required more disclosure', 'It raised income taxes', 'It recorded assets at fair value'], 0)]),
 ('Derivatives and mark-to-market', [2002, 2008], 'Advanced', '', 'Fair value',
  '&ldquo;Mark-to-market&rdquo; then turned out to be truly &ldquo;mark-to-myth.&rdquo; ... Derivatives are financial weapons of mass destruction. (2002)',
  [('num', 'A derivative contract had a fair value of +$20 million at the start of the year and &minus;$15 million at year-end. What gain (loss) is reported for the year ($ millions; use a minus sign for a loss)?', '&minus;35'),
   ('mc', 'Why are many derivatives hard to audit?',
    ['With no active market, fair value comes from management&rsquo;s models and assumptions', 'Derivatives are never recorded on the balance sheet', 'They are always worth zero', 'They are recorded at historical cost'], 0)]),
 ('Audit committees and auditors', [2002, 1998], 'Intermediate', '', 'Governance',
  'Audit committees can&rsquo;t audit. ... The key job of the audit committee is simply to get the auditors to divulge what they know. (2002)',
  [('mc', 'Under the Sarbanes-Oxley Act, who appoints and oversees a public company&rsquo;s external auditor?',
    ['The audit committee of the board', 'The CEO', 'The CFO', 'The SEC'], 0),
   ('mc', 'Buffett suggests the audit committee ask the auditor whether the financial statements would differ if the auditor had prepared them alone. What is the main purpose of such questions?',
    ['To make auditors share their concerns about management&rsquo;s accounting choices', 'To lower the audit fee', 'To replace the internal audit function', 'To prepare the tax return'], 0)]),
 ('Pension return assumptions', [2007, 2016], 'Advanced', '', 'Estimates',
  'Other accounting choices remain &ndash; important among these the investment-return assumption a company uses in calculating pension expense. (2007)',
  [('num', 'Pension plan assets are $1,000 million. If the company assumes an 8% expected return instead of 5%, by how much does reported pension expense fall ($ millions)?', '30'),
   ('mc', 'A higher assumed return on pension assets&hellip;',
    ['lowers pension expense and raises reported earnings', 'raises pension expense', 'has no effect on earnings', 'increases the cash paid to retirees'], 0)]),
 ('Insurance float and loss reserves', [2007, 2011, 2014], 'Intermediate', 'Ch10', 'Estimates',
  'Insurance float &ndash; money we temporarily hold in our insurance operations that does not belong to us &ndash; funds $59 billion of our investments. (2007)',
  [('num', 'An insurer collects $100 million of premiums and incurs $95 million of losses and expenses. What is its underwriting profit ($ millions)?', '5'),
   ('mc', 'On the balance sheet, insurance float appears mainly as&hellip;',
    ['liabilities (loss reserves and unearned premiums)', 'revenue', 'stockholders&rsquo; equity', 'goodwill'], 0)]),
 ('Deferred tax liability', [1989, 1986], 'Intermediate', '', '',
  'In effect, this deferred tax liability is equivalent to a very large transfer tax that is payable only if we elect to move from one asset to another. (1989)',
  [('num', 'Berkshire holds stocks with an unrealized gain of $1,000 million. At a 21% tax rate, what deferred tax liability is recorded ($ millions)?', '210'),
   ('mc', 'When would that deferred tax actually be paid?',
    ['When the stocks are sold and the gain is realized', 'Every year', 'Never', 'When dividends are received'], 0)]),
 ('Book value vs. intrinsic value', [1992, 1994, 2018], 'Intro', 'Ch2, Ch11', '',
  'The annual change in Berkshire&rsquo;s book value ... is a metric that has lost the relevance it once had. (2018)',
  [('num', 'Total stockholders&rsquo; equity is $600 million and 2 million shares are outstanding. What is book value per share ($)?', '300'),
   ('mc', 'Why can intrinsic value be far above book value?',
    ['Assets are mostly recorded at historical cost, and internally built value (brands, goodwill) is not recorded', 'Book value includes market prices of all assets', 'Liabilities are ignored in book value', 'Book value is measured in future dollars'], 0)]),
 ('Unrealized gains in net income', [2017, 2018, 2024], 'Intermediate', 'Ch3', 'Analytics',
  'The new rule says that the net change in unrealized investment gains and losses in stocks we hold must be included in all net income figures we report to you. (2017)',
  [('num', 'Stocks Berkshire holds rose from $100 billion to $130 billion during the year, and none were sold. Under the current rule, what pre-tax gain is included in net income ($ billions)?', '30'),
   ('mc', 'Which measure does Buffett tell shareholders to focus on instead?',
    ['Operating earnings, which exclude investment gains and losses', 'EBITDA', 'Revenue', 'Total comprehensive income'], 0)]),
 ('"Adjusted" earnings', [2016], 'Intro', 'Ch3', '',
  'Too many managements ... are looking for any means to report, and indeed feature, &ldquo;adjusted earnings&rdquo; that are higher than their company&rsquo;s GAAP earnings. (2016)',
  [('num', 'GAAP net income is $80 million. Management adds back $15 million of stock-based compensation and $10 million of amortization. What &ldquo;adjusted earnings&rdquo; does it report ($ millions)?', '105'),
   ('mc', 'Which add-back does Buffett argue is clearly a real cost?',
    ['Stock-based compensation', 'Income tax refund', 'Gain on sale of land', 'Dividends paid'], 0)]),
 ('Share repurchases', [1999, 2011, 2016], 'Intro', 'Ch11', '',
  'We will not repurchase shares unless we believe Berkshire stock is selling well below intrinsic value, conservatively calculated. (1999)',
  [('num', 'Net income is $500 and 250 shares are outstanding. The company buys back 50 shares. What is EPS after the buyback ($)?', '2.50'),
   ('mc', 'Which account is debited when a company buys back its own shares?',
    ['Treasury Stock (contra-equity)', 'Cash', 'Retained Earnings', 'Common Stock expense'], 0)]),
 ('Inflation and reported returns', [1979, 1980, 1981], 'Advanced', '', '',
  'In past reports we have explained how inflation has caused our apparently satisfactory long-term corporate performance to be illusory as a measure of true investment results for our owners. (1981)',
  [('num', 'A company earns a 12% return on equity while inflation is 10%. Roughly what is the real (inflation-adjusted) return, in %?', '2'),
   ('mc', 'Why do historical-cost financial statements overstate earnings when prices rise?',
    ['Depreciation and cost of goods sold are based on older, lower prices', 'Revenue is recorded at old prices', 'Assets are marked to market', 'Taxes are ignored'], 0)]),
]

CSS = '''*{box-sizing:border-box}html{background:#e9ecea}body{margin:0;font:11pt/1.4 "Times New Roman",Times,serif;color:#000}
.page{width:8.5in;height:11in;margin:18px auto;background:#fff;padding:.6in .7in;position:relative;box-shadow:0 6px 24px rgba(0,0,0,.15)}
header{display:flex;justify-content:space-between;border-bottom:1.2pt solid #000;padding-bottom:3pt;margin-bottom:10pt;font:700 9pt Arial,sans-serif}
header .n span{display:inline-block;width:2.2in;border-bottom:.8pt solid #000}
h1{font-size:16pt;margin:0 0 4pt}.meta{font-size:10pt;margin:0 0 10pt}
.q{border:.8pt solid #e57373;border-radius:8pt;padding:8pt 12pt;font-size:10.5pt;font-style:italic;margin:0 0 14pt}
ol.qs{padding-left:18pt;margin:0}ol.qs>li{margin:0 0 22pt}
ol.op{list-style:upper-alpha;margin:6pt 0 0;padding-left:20pt}ol.op li{margin:3pt 0}
.ans{display:inline-block;min-width:1.4in;border-bottom:.9pt solid #000;text-align:right;margin-left:8pt}
.ans::after{content:"\\00a0"}html.key .ans::after{content:attr(data-a);color:#b3200f;font-weight:700}
html.key li.r{color:#b3200f;font-weight:700}
.keytag{display:none;color:#b3200f}html.key .keytag{display:inline}
.src{position:absolute;left:.7in;right:.7in;bottom:.45in;font-size:9pt;border-top:.6pt solid #000;padding-top:3pt}
.src a{color:#000}
.bar{position:sticky;top:0;display:flex;gap:10px;justify-content:center;padding:10px;background:#16263a}
.bar button{font:600 13px Arial,sans-serif;padding:7px 16px;border-radius:6px;border:0;background:#fff;cursor:pointer}
@media print{@page{size:letter;margin:0}html{background:#fff}.bar{display:none}.page{margin:0;box-shadow:none}}'''

rows = []
for i, (theme, years, diff, a250, a531, quote, qs) in enumerate(T, 1):
    items = []
    for qn, q in enumerate(qs):
        if q[0] == 'mc':   # rotate options so the correct letter varies across sheets
            r = (i * 2 + qn * 3) % 4
            opts = q[2][r:] + q[2][:r]
            q = ('mc', q[1], opts, (q[3] - r) % 4)
        if q[0] == 'num':
            items.append(f'<li>{q[1]}<span class="ans" data-a="{q[2]}"></span></li>')
        else:
            ops = ''.join(f'<li{" class=\"r\"" if k == q[3] else ""}>{o}</li>' for k, o in enumerate(q[2]))
            items.append(f'<li>{q[1]}<ol class="op">{ops}</ol></li>')
    m = __import__('re').match(r'(.*) \((.*)\)$', quote)
    qt = f'&ldquo;{m.group(1)}&rdquo; ({m.group(2)})' if m else f'&ldquo;{quote}&rdquo;'
    links = ', '.join(f'<a href="{url(y)}">{y}</a>' for y in years)
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buffett Letters Q{i}</title><style>{CSS}</style></head><body>
<div class="bar"><button onclick="document.documentElement.classList.toggle('key')">Show/hide answers</button><button onclick="print()">Print</button></div>
<div class="page">
<header><span>Buffett&rsquo;s Letters &middot; Accounting Theme {i}<span class="keytag"> &middot; Answer key</span></span><span class="n">Name <span></span></span></header>
<h1>{theme}</h1>
<p class="meta">Letters: {', '.join(str(y) for y in years)} &middot; Difficulty: {diff}</p>
<div class="q">{qt}</div>
<ol class="qs">{''.join(items)}</ol>
<p class="src">Source: Warren E. Buffett, Letters to Berkshire Hathaway Shareholders: {links} (berkshirehathaway.com/letters). Quotation &copy; Berkshire Hathaway Inc., all rights reserved; quoted for non-commercial teaching. Numbers in the questions are made up unless stated.</p>
</div><script>if(location.hash==='#key')document.documentElement.classList.add('key')</script></body></html>'''
    open(os.path.join(OUT, f'Q{i:02d}.html'), 'w').write(html)
    rows.append((i, theme, years, diff, a250, a531))

print('wrote', len(rows), 'question sheets')


def h(p):
    f = os.path.join(ROOT, p.lstrip('/'))
    return hashlib.md5(open(f, 'rb').read()).hexdigest()[:8] if os.path.exists(f) else '0'


lines = ['| # | Accounting theme | Key letters | Reading | Difficulty | ACC250 | ACC531 | Questions | Key |',
         '|---|---|---|---|---|---|---|---|---|']
for i, theme, years, diff, a250, a531 in rows:
    yl = ', '.join(f'[{y}]({url(y)})' for y in years)
    q = f'/assets/Buffett/Q{i:02d}.pdf'; k = f'/assets/Buffett/Q{i:02d}-Key.pdf'; rd = f'/assets/Buffett/R{i:02d}.pdf'
    lines.append(f'| {i} | {theme} | {yl} | [PDF]({rd}?v={h(rd)}) | {diff} | {a250 or "—"} | {a531 or "—"} | [PDF]({q}?v={h(q)}) | [PDF]({k}?v={h(k)}) |')

md = f'''---
layout: page
title: "Buffett's Letters: Accounting Themes"
---

Warren Buffett&rsquo;s annual letters to Berkshire Hathaway shareholders ([berkshirehathaway.com/letters](https://www.berkshirehathaway.com/letters/letters.html), 1977&ndash;2024) explain many accounting issues in plain English. The table lists the main themes, the letters that discuss them most, and where they fit in ACC250 (Intro to Financial Accounting) and ACC531 (Auditing). For each theme, the **Reading** packet starts with a short summary and collects only the relevant passages from its key letters; a one-page question sheet and answer key follow.

<style>
.bt {{ overflow-x:auto; }}
.bt table {{ font-size:.8em; }}
.bt th, .bt td {{ white-space:nowrap; }}
</style>

<div class="bt" markdown="1">

{chr(10).join(lines)}

</div>

**Difficulty**: Intro = needs only ACC250 concepts; Intermediate = intermediate accounting or auditing; Advanced = beyond the intro sequence.
Questions use made-up numbers unless stated.

### Source and copyright

**Source:** Warren E. Buffett, *Letters to Berkshire Hathaway Shareholders*, 1977&ndash;2024, Berkshire Hathaway Inc., [berkshirehathaway.com/letters](https://www.berkshirehathaway.com/letters/letters.html).

**Copyright:** The letters are &copy; Berkshire Hathaway Inc. All rights reserved. The reading packets and question sheets quote short excerpts for non-commercial teaching only; each cites the letter it quotes and links to the full text. The summaries and questions are original course material by Jaeyoon Yu. This page is not affiliated with or endorsed by Berkshire Hathaway Inc.
'''
open(os.path.join(ROOT, 'buffett-letters.md'), 'w').write(md)
print('wrote buffett-letters.md')
