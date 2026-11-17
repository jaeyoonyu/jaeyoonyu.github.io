#!/usr/bin/env python3
"""Reading packets: for each theme, a summary followed by the relevant excerpts from its key letters.

Usage: python _tools/buffett/gen_readings.py LETTER_TEXT_DIR
LETTER_TEXT_DIR holds 1977.txt ... 2024.txt (plain text of each letter, from berkshirehathaway.com/letters).
Writes assets/Buffett/R01.html ... R17.html (print to PDF separately).
"""
import os, re, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TXT = sys.argv[1]
spec = importlib.util.spec_from_file_location('gb', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_buffett.py'))
src = open(spec.origin).read().split('\nrows = []')[0]   # reuse T, url() without writing files
ns = {'__file__': spec.origin}; exec(src, ns)
T, url = ns['T'], ns['url']

# keyword pattern used to pick passages, and a plain-English summary, per theme (same order as T)
K = [
 (r'goodwill', 'When one company buys another for more than the fair value of its identifiable net assets, the excess is recorded as goodwill. Buffett separates this <b>accounting goodwill</b> from <b>economic goodwill</b>: the ability of a great business to earn high returns on its tangible assets. Economic goodwill that a company builds itself never appears on its balance sheet, so book value can understate what a business is worth.'),
 (r'owner earnings|capitalized expenditures|non-cash charges', '<b>Owner earnings</b> = reported earnings + depreciation, depletion, amortization and other non-cash charges &minus; the capital spending needed to keep the business competitive. Buffett argues this, not GAAP earnings, is what matters for valuing a business, because some non-cash charges are not real costs while maintenance capital spending is.'),
 (r'look-through', 'Under GAAP, Berkshire reports only the dividends from companies it owns less than 20% of, so its share of their <b>retained earnings</b> never shows up in Berkshire&rsquo;s profit. <b>Look-through earnings</b> add that share back (less the tax that would be due if it were paid out) to show the economic earnings of everything Berkshire owns.'),
 (r'option', 'For years, companies did not record an expense when they paid employees with <b>stock options</b>. Buffett argues options are compensation, compensation is an expense, and an expense belongs in net income, even when its exact amount is hard to estimate. U.S. GAAP has required option expensing since 2006.'),
 (r'restructuring|smooth|manipulat|managed earnings|big bath|cookie', 'Buffett warns against <b>managing earnings</b>: booking oversized &ldquo;restructuring charges&rdquo; (a &ldquo;big bath&rdquo;) so later years look better, or adjusting estimates to make results smooth. He prefers honest, lumpy results. For auditors, unusually smooth earnings and large one-time charges are signals of possible manipulation.'),
 (r'EBITDA|depreciation', '<b>EBITDA</b> (earnings before interest, taxes, depreciation and amortization) leaves out depreciation as if it were not a real cost. Buffett points out that the cash for plant and equipment is paid up front, before the assets produce anything, so depreciation is a very real expense.'),
 (r'pooling|purchase accounting|purchase-accounting', 'Until 2001, U.S. GAAP allowed two methods for acquisitions. <b>Pooling</b> combined the two companies&rsquo; book values and created no goodwill; the <b>purchase</b> method recorded assets at fair value and created goodwill that was then amortized against earnings. Managers favored pooling to avoid those charges. Today only the purchase (acquisition) method is allowed.'),
 (r'derivative|mark-to-market|mark-to-model', 'Many <b>derivatives</b> have no market price, so their fair value is estimated with models. Buffett shows how traders and companies booked large &ldquo;earnings&rdquo; from optimistic estimates (&ldquo;mark-to-myth&rdquo;) that later vanished, and calls derivatives &ldquo;financial weapons of mass destruction.&rdquo;'),
 (r'audit committee|auditor', 'Buffett says <b>audit committees can&rsquo;t audit</b>; their job is to get the external auditors to tell them what they know. He proposes four questions the committee should ask the auditors, starting with whether the statements would differ if the auditor alone had prepared them.'),
 (r'pension', 'Pension expense depends on the <b>assumed return</b> on pension assets. A higher assumption lowers reported expense and raises earnings, with no change in the plan&rsquo;s real economics. Buffett shows that many companies used assumptions (about 8%) that their actual asset mix could not support.'),
 (r'\bfloat\b', 'Insurers collect premiums before they pay claims. The money held in between, <b>float</b>, appears on the balance sheet as liabilities (loss reserves and unearned premiums), but if the insurer earns an underwriting profit, it is money that costs nothing to use. Berkshire invests its float.'),
 (r'deferred tax', 'When stocks rise in value, Berkshire records a <b>deferred tax liability</b> for the tax that would be owed if they were sold. Buffett explains that this liability is real, but it is paid only when a gain is realized, so it works like an interest-free loan from the government.'),
 (r'book value|intrinsic value', '<b>Book value</b> is what the balance sheet says shareholders&rsquo; equity is; <b>intrinsic value</b> is the discounted value of the cash a business will produce. Because assets are recorded at historical cost and internally built value is not recorded, the two can differ widely. In 2018 Buffett stopped using book value as Berkshire&rsquo;s headline measure.'),
 (r'unrealized|new rule|GAAP rule|operating earnings', 'Since 2018, U.S. GAAP requires changes in the market value of stocks a company holds to be reported in <b>net income</b>, even if nothing is sold. For Berkshire this makes net income swing by billions each quarter. Buffett tells shareholders to focus on <b>operating earnings</b>, which leave these gains and losses out.'),
 (r'adjusted|stock-based|compensation|real cost', 'Many companies feature <b>&ldquo;adjusted&rdquo; earnings</b> that leave out costs such as stock-based compensation or restructuring. Buffett argues these are real costs, and that excluding them makes performance look better than it is.'),
 (r'repurchas|buy ?back', 'A <b>share repurchase</b> helps the shareholders who stay only if the price paid is below the company&rsquo;s intrinsic value. Buffett explains Berkshire&rsquo;s rule: buy back shares only when they are clearly cheap, and only with cash not needed for the business.'),
 (r'inflation', 'In the late 1970s and early 1980s, inflation ran above 10%. Financial statements built on <b>historical cost</b> overstated real earnings, because depreciation and inventory costs were based on old, lower prices. Buffett explains why a business earning a respectable return on equity could still give its owners little or no real return.'),
]

CSS = open(os.path.join(ROOT, 'assets', 'Buffett', 'Q01.html')).read().split('<style>')[1].split('</style>')[0]
CSS += '''.page{height:auto;min-height:11in}.sum{border:.8pt solid #e57373;border-radius:8pt;padding:8pt 12pt;margin:0 0 12pt;font-size:11pt}
.sum b.t{display:block;font:700 9pt Arial,sans-serif;margin-bottom:2pt}h2{font:700 11pt Arial,sans-serif;margin:12pt 0 4pt;border-bottom:.8pt solid #000;padding-bottom:2pt}
p.ex{margin:0 0 6pt;font-size:10.5pt;text-align:justify}p.gap{text-align:center;margin:0 0 6pt;color:#555}
.src{position:static;margin-top:14pt}
@media print{.page{min-height:0;height:auto}}'''

MAXW = 600   # words of excerpts per letter


def excerpts(year, rx):
    t = open(os.path.join(TXT, f'{year}.txt')).read()
    t = re.sub(r'\s*[\uf8e7\uf8e8]\s*', ' \u2014 ', t)      # private-use glyphs used for em dashes in some PDFs
    t = re.sub(r'[\uf000-\uf8ff]', '', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'(?<=[a-z])- (?=[a-z])', '', t)
    s = re.split(r'(?<=[.!?])\s+(?=[A-Z"“(])', t)
    hit = [i for i, x in enumerate(s) if re.search(rx, x, re.I)]
    keep = set()
    for i in hit:
        keep.update(range(max(0, i - 1), min(len(s), i + 2)))
    out, words, prev = [], 0, None
    for i in sorted(keep):
        w = len(s[i].split())
        if words + w > MAXW:
            break
        if prev is not None and i != prev + 1:
            out.append(None)
        out.append(s[i]); words += w; prev = i
    paras, cur = [], []
    for x in out:
        if x is None:
            if cur: paras.append(' '.join(cur)); cur = []
            paras.append(None)
        else:
            cur.append(x)
            if len(cur) >= 4: paras.append(' '.join(cur)); cur = []
    if cur: paras.append(' '.join(cur))
    return paras


def esc(x):
    return x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


for i, ((theme, years, diff, *_), (rx, summary)) in enumerate(zip(T, K), 1):
    body = []
    for y in years:
        ps = excerpts(y, rx)
        if not ps:
            continue
        body.append(f'<h2>{y} letter</h2>')
        for p in ps:
            body.append('<p class="gap">&hellip;</p>' if p is None else f'<p class="ex">{esc(p)}</p>')
    links = ', '.join(f'<a href="{url(y)}">{y}</a>' for y in years)
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buffett Letters Reading {i}</title><style>{CSS}</style></head><body>
<div class="bar"><button onclick="print()">Print</button></div>
<div class="page">
<header><span>Buffett&rsquo;s Letters &middot; Accounting Theme {i} &middot; Reading</span><span></span></header>
<h1>{theme}</h1>
<p class="meta">Letters: {', '.join(str(y) for y in years)} &middot; Difficulty: {diff}</p>
<div class="sum"><b class="t">Summary</b>{summary}</div>
{chr(10).join(body)}
<p class="src">Source: Warren E. Buffett, Letters to Berkshire Hathaway Shareholders: {links} (berkshirehathaway.com/letters). Excerpts &copy; Berkshire Hathaway Inc., all rights reserved; reproduced in part for non-commercial teaching. &ldquo;&hellip;&rdquo; marks skipped text. The summary is original course material by Jaeyoon Yu; not affiliated with or endorsed by Berkshire Hathaway Inc.</p>
</div></body></html>'''
    open(os.path.join(ROOT, 'assets', 'Buffett', f'R{i:02d}.html'), 'w').write(html)
print('wrote', len(T), 'readings')
