#!/usr/bin/env python3
"""Ch9 opening activity: Delta Air Lines' property and equipment (Form 10-K, FY2025).

Usage: python _tools/acc250_case/gen_ch9_ppe.py assets/ACC250
Writes Ch9-PPE-Worksheet.html (one page, key via #key) and Ch9-PPE-RealLife.html (slides).
Worksheet helpers come from gen_worksheets.py; the slide shell is Ch8-BadDebt-RealLife.html.
Amounts are from Delta's 10-K for the year ended Dec 31, 2025 (accession 0000027904-26-000013).
"""
import os, sys

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_worksheets.py'), encoding='utf-8').read()
ns = {'__file__': os.path.join(HERE, 'gen_worksheets.py')}
exec(src.split('# Ch8: Crocs bad debts')[0].replace('OUT = sys.argv[1]', "OUT = ''"), ns)
stmt, qlist, page, inl, pick = ns['stmt'], ns['qlist'], ns['page'], ns['inl'], ns['pick']

DAL_URL = 'https://www.sec.gov/Archives/edgar/data/27904/000002790426000013/dal-20251231.htm'

# ---------------------------------------------------------------- data ($ millions)
BS = [('Cash and cash equivalents', ('4,310', '3,069'), '$'),
      ('Other current assets', ('6,658', '6,775'), 'u'),
      ('Total current assets', ('10,968', '9,844'), 'i'),
      ('Property and equipment, net<sup>*</sup>', ('39,743', '37,595'), 'hl'),
      ('Other noncurrent assets', ('30,606', '27,933'), 'u'),
      ('Total assets', ('81,317', '75,372'), 'i uu $'),
      ('Total liabilities', ('60,464', '60,079'), 'hd $'),
      ('Total stockholders&rsquo; equity', ('20,853', '15,293'), 'u'),
      ('Total liabilities and equity', ('81,317', '75,372'), 'i uu $')]
NOTE = [('Flight equipment (aircraft, engines, parts) &middot; 30&ndash;34 yrs', ('47,981', '44,722'), '$'),
        ('Ground property and equipment &middot; 3&ndash;40 yrs', ('11,165', '10,695'), ''),
        ('Information technology assets &middot; 3&ndash;15 yrs', ('3,167', '3,135'), ''),
        ('Equipment under finance leases', ('1,185', '1,196'), ''),
        ('Advance payments for equipment', ('964', '1,075'), 'u'),
        ('Property and equipment, at cost', ('?', '?'), 'i hl'),
        ('Less: Accumulated depreciation', ('(24,719)', '(23,228)'), 'u hl'),
        ('Property and equipment, net', ('39,743', '37,595'), 'i uu $ hl')]
IS = [('Operating revenue', '63,364', '$'),
      ('Depreciation and amortization', '(2,443)', 'hl'),
      ('All other operating expenses', '(55,099)', 'u'),
      ('Operating income', '5,822', 'i'),
      ('Non-operating items and income tax, net', '(817)', 'u'),
      ('Net income', '5,005', 'i uu $')]

# ---------------------------------------------------------------- worksheet
front = f'''<h1>Delta Air Lines: Property and Equipment in Real Financial Statements</h1>
<p class="intro2">An airline needs airplanes, engines, hangars and computer systems for decades. Delta records them as property and equipment (PPE) and spreads their cost over the years it uses them.</p>
<p class="filing"><b>Source:</b> Delta Air Lines, Inc. Form 10-K, year ended December 31, 2025 (condensed<sup>**</sup>; $ millions) &middot;
<a href="{DAL_URL}" target="_blank">{DAL_URL.replace("https://www.", "")}</a></p>
<style>.stmt {{ font-size:9pt; }} .stmt td {{ padding:1.2pt 2pt; }} .defs dt {{ margin-top:2pt; }} ol.qs li {{ padding:4pt 0 1pt; }} .defs {{ font-size:9.2pt !important; }}
.stmt.note td:first-child {{ font-size:8.6pt; }}</style>
<div class="cols">
<div>
{stmt('Delta Air Lines, Inc.', 'Consolidated Balance Sheets', ('Dec 31, 2025', 'Dec 31, 2024'), BS)}
<div style="height:8pt"></div>
{stmt('Delta Air Lines, Inc.', 'Statement of Operations, 2025', '2025', IS)}
</div>
<div>
{stmt('Delta Air Lines, Inc.', 'Note: Property and Equipment', ('Dec 31, 2025', 'Dec 31, 2024'), NOTE).replace('class="stmt"', 'class="stmt note"', 1)}
<p class="fn" style="margin-top:4pt">From the note: &ldquo;We record property and equipment at cost and depreciate &hellip; on a <b>straight-line basis</b> to their estimated <b>residual values</b> over their estimated <b>useful lives</b>.&rdquo; Residual values for owned aircraft and engines are generally <b>5% to 10% of cost</b>.</p>
</div>
</div>
<h2>Accounts &amp; Terms</h2>
<div class="defs" style="font-size:9.6pt">
<dl>
<dt>Property and equipment (PPE), at cost</dt><dd>What the company paid to buy the assets and get them ready to use (cost principle). An asset.</dd>
<dt>Accumulated depreciation (AccDep)</dt><dd>The total depreciation recorded so far on the assets still owned. A contra-asset subtracted from PPE.</dd>
</dl>
<dl>
<dt>PPE, net (book value)</dt><dd>PPE at cost &minus; AccDep: the cost not yet depreciated. It is not the market value.</dd>
<dt>Depreciation expense</dt><dd>This year&rsquo;s share of the cost, on the income statement. Straight-line: (Cost &minus; Residual value) &divide; Useful life.</dd>
</dl>
</div>
<h2>Find it in the statements <small>Write the amount ($ millions, or %).</small></h2>
<p class="sub2">Answer as of <b>December 31, 2025</b>, unless a question says otherwise.</p>
{qlist([("What did Delta originally pay for the property and equipment it still owns (PPE at cost, the &ldquo;?&rdquo; in the note)?", "64,462"),
        ("How much of that cost has been depreciated so far?", "24,719"),
        ("What is the book value of Delta&rsquo;s property and equipment?", "39,743"),
        ("What percentage of the cost has been depreciated so far?", "38.3%"),
        ("What percentage of Delta&rsquo;s total assets is property and equipment, net?", "48.9%"),
        ("How much depreciation and amortization expense did Delta record in 2025?<sup>&dagger;</sup>", "2,443"),
        ("Delta buys a new airplane for <b>$100</b> million. It expects to use it for <b>30 years</b> and to sell it then for <b>10%</b> of cost. Straight-line depreciation per year?", "3")], 1, full=True)}
<p class="fn"><sup>&dagger;</sup> Recording depreciation does not use cash: Delta paid cash when it bought the assets. In 2025 Delta paid <b>4,499</b> for new property and equipment, almost twice its depreciation.</p>
<p class="fn" style="margin-top:2pt"><sup>*</sup> As printed in the 10-K: &ldquo;Property and equipment, net of accumulated depreciation and amortization of $24,719 and $23,228.&rdquo; &ldquo;Depreciation&rdquo; here includes the amortization of a small amount of leased equipment.</p>
<p class="fn" style="margin-top:2pt"><sup>**</sup> Other current assets, other noncurrent assets, total liabilities, all other operating expenses and non-operating items are derived from reported totals.</p>
'''
open(os.path.join(OUT, 'Ch9-PPE-Worksheet.html'), 'w', encoding='utf-8').write(
    page('PPE Worksheet', 'Delta', 'ACC 250 &middot; Ch9 Opening Activity', front, '', ''))
print('wrote Ch9-PPE-Worksheet')

# ---------------------------------------------------------------- slides
SHELL = os.path.join(OUT, 'Ch8-BadDebt-RealLife.html')
lines = open(SHELL, encoding='utf-8').read().split('\n')
cut1 = next(i for i, l in enumerate(lines) if l.startswith('<div id="stage">')) + 1
cut2 = next(i for i, l in enumerate(lines) if l.startswith('<div id="bar">'))
head = '\n'.join(lines[:cut1]).replace('<title>Bad Debts in Real Life</title>', '<title>PPE in Real Life</title>')
tail = '\n'.join(lines[cut2:])


def rows(rs, hl=()):
    out = []
    for lab, v, *f in rs:
        cls = ' class="total"' if f and 'total' in f[0] else ''
        st = ' style="background:#fdf6e3"' if lab in hl else ''
        out.append(f'<tr{cls}{st}><td>{lab}</td><td>{v}</td></tr>')
    return '\n'.join(out)


body = f'''
<section class="s title" data-nav="Cover">
<div class="tstack">
<p class="eyebrow">ACC 250 &middot; Ch9 Long-lived Assets</p>
<h1>An airplane lasts 30 years. When is it an expense?</h1>
<p class="lede">How Delta Air Lines reports its property and equipment in its 10-K.</p>
</div>
<p class="title-date">Delta Air Lines: Form 10-K, year ended Dec 31, 2025 ($ millions)</p>
</section>

<section class="s" data-nav="The problem">
<p class="eyebrow">The problem</p>
<h2>A big purchase that lasts for decades</h2>
<div class="tests">
<div class="test"><span class="n">1</span><div>Delta pays <b>$100 million</b> cash for a new airplane.</div></div>
<div class="test"><span class="n">2</span><div>The airplane will carry passengers and earn revenue for about <b>30 years</b>.</div></div>
<div class="test"><span class="n">3</span><div>At the end, Delta expects to sell it for about <b>10%</b> of what it paid.</div></div>
</div>
<div class="ask" style="margin-top:22px"><span class="qlab">Think about it</span><p>Should the whole $100 million be an <b>expense</b> this year? If not, when?</p></div>
</section>

<section class="s" data-nav="Delta balance sheet">
<p class="eyebrow">Delta &middot; Balance sheet, Dec 31, 2025</p>
<h2>Start with the balance sheet</h2>
<div class="two">
<div class="stmt">
<h3>Condensed ($ millions)</h3>
<table>
<tr><th></th><th>$M</th></tr>
{rows([("Cash and cash equivalents", "4,310"), ("Other current assets", "6,658"), ("Total current assets", "10,968", "total"),
       ('<b class="hl">Property and equipment, net</b>', '<span class="hl">39,743</span>'),
       ("Other noncurrent assets", "30,606"), ("Total assets", "81,317", "total")],
      hl=('<b class="hl">Property and equipment, net</b>',))}
</table>
</div>
<div>
<div class="note">Delta owns hundreds of <b>airplanes</b>, plus engines, spare parts, hangars and computer systems.</div>
<div class="note">Property and equipment is Delta&rsquo;s <b>largest asset</b>: about <b>half</b> of everything it owns.</div>
<div class="ask" style="margin-top:14px"><span class="qlab">Look closely</span><p>Why does the line say &ldquo;<b>net</b>&rdquo;? Net of what?</p></div>
</div>
</div>
</section>

<section class="s" data-nav="Zoom in: PPE">
<p class="eyebrow">Delta &middot; Property and equipment note</p>
<h2>Zoom in: cost, used up, and what is left</h2>
<div class="def"><p class="term">As printed in the 10-K</p>
<p style="font-family:Charter,Georgia,serif">Property and equipment, net of accumulated depreciation and amortization of $24,719 and $23,228 &nbsp;&nbsp; <b>39,743</b> &nbsp;&nbsp; 37,595</p></div>
<div class="two" style="margin-top:20px">
<div class="stmt">
<h3>December 31, 2025 ($ millions)</h3>
<table>
<tr><th></th><th>$M</th></tr>
<tr><td>Flight equipment (30&ndash;34 years)</td><td>47,981</td></tr>
<tr><td>Ground equipment, IT, leases, advances</td><td>16,481</td></tr>
<tr class="total"><td>Property and equipment, at cost</td><td>64,462</td></tr>
<tr><td>Less: Accumulated depreciation</td><td class="neg">(24,719)</td></tr>
<tr class="total"><td>Property and equipment, net</td><td class="hl">39,743</td></tr>
</table>
</div>
<div class="def" style="border-left-color:#b8901f"><p class="term" style="color:#8a6d1f">Accumulated depreciation</p><p>All the depreciation recorded so far on the assets Delta still owns. A <b>contra-asset</b>: it is subtracted from cost.</p></div>
</div>
<div class="key"><span class="klab">Net = book value</span>$39.7 billion is the cost <b>not yet depreciated</b>. It is not what the airplanes would sell for.</div>
</section>

<section class="s" data-nav="How much is used up?">
<p class="eyebrow">Delta &middot; Putting it in perspective</p>
<h2>Out of every $100 Delta paid for its PPE&hellip;</h2>
<div class="hbars">
<div class="hbar"><span>Not yet depreciated</span><div class="track"><div class="fill" style="width:61.7%;background:#1a7a5e"></div></div><span class="v">$62</span></div>
<div class="hbar"><span>Already depreciated</span><div class="track"><div class="fill" style="width:38.3%;background:#b3200f"></div></div><span class="v">$38</span></div>
</div>
<div class="note" style="margin-top:26px">24,719 &divide; 64,462 &asymp; <b>38.3%</b> of the cost has been depreciated so far.</div>
<div class="note">Property and equipment, net is 39,743 &divide; 81,317 &asymp; <b>48.9%</b> of Delta&rsquo;s total assets.</div>
</section>

<section class="s" data-nav="Delta's policy">
<p class="eyebrow">Delta &middot; Accounting policy</p>
<h2>How Delta depreciates</h2>
<div class="def"><p class="term">From the 10-K</p><p style="font-family:Charter,Georgia,serif">&ldquo;We record property and equipment at cost and depreciate or amortize these assets on a straight-line basis to their estimated residual values over their estimated useful lives.&rdquo;</p></div>
<div class="two" style="margin-top:18px">
<div class="stmt">
<table>
<tr><th>Estimated useful life</th><th>Years</th></tr>
<tr><td>Flight equipment</td><td>30&ndash;34</td></tr>
<tr><td>Ground property and equipment</td><td>3&ndash;40</td></tr>
<tr><td>Information technology assets</td><td>3&ndash;15</td></tr>
</table>
</div>
<div>
<div class="note"><b>Cost</b>: what Delta paid (cost principle).</div>
<div class="note"><b>Residual value</b>: generally <b>5% to 10% of cost</b> for owned aircraft and engines.</div>
<div class="note"><b>Method</b>: straight-line, the same amount every year.</div>
</div>
</div>
</section>

<section class="s" data-nav="One airplane">
<p class="eyebrow">Apply Delta&rsquo;s policy</p>
<h2>One $100 million airplane</h2>
<div class="two">
<div>
<p class="big">(100 &minus; 10) &divide; 30 = <span class="hl">3</span> million per year</p>
<table class="je">
<tr><th>Every Dec 31 (adjusting entry)</th><th>Dr</th><th>Cr</th></tr>
<tr><td>Depreciation expense (+E)</td><td>3</td><td></td></tr>
<tr><td class="cr">Accumulated depreciation (+xA)</td><td></td><td>3</td></tr>
</table>
</div>
<div class="stmt">
<table>
<tr><th>After 10 years ($M)</th><th>$M</th></tr>
<tr><td>Airplane, at cost</td><td>100</td></tr>
<tr><td>Less: Accumulated depreciation</td><td class="neg">(30)</td></tr>
<tr class="total"><td>Airplane, net (book value)</td><td class="hl">70</td></tr>
</table>
</div>
</div>
<div class="key"><span class="klab">Answer to slide 2</span>No. The $100 million becomes an expense <b>3 million at a time</b>, over the 30 years the airplane earns revenue: the matching principle.</div>
</section>

<section class="s" data-nav="Expense vs. cash">
<p class="eyebrow">Delta &middot; 2025</p>
<h2>Depreciation is an expense, not a cash payment</h2>
<div class="hbars">
<div class="hbar wide"><span>Paid for new property and equipment</span><div class="track"><div class="fill" style="width:100%;background:#5b7f95"></div></div><span class="v">4,499</span></div>
<div class="hbar wide"><span>Depreciation and amortization expense</span><div class="track"><div class="fill" style="width:54.3%;background:#b3200f"></div></div><span class="v">2,443</span></div>
</div>
<div class="note" style="margin-top:26px">The <b>cash</b> left when Delta bought the assets (investing activities). Depreciation is recorded later with <b>no cash</b>, so the cash flow statement adds it back to net income.</div>
<div class="note">Delta spent almost <b>twice</b> its depreciation on new equipment, so property and equipment, net <b>grew</b>: 37,595 &rarr; 39,743.</div>
</section>

<section class="s" data-nav="Discuss">
<p class="eyebrow">Before we start Ch9</p>
<h2>Questions for you</h2>
<ol class="steps">
<li><b>Q1.</b> Delta pays $2 million to deliver and install a new flight simulator. Expense this year, or part of the simulator&rsquo;s cost?</li>
<li><b>Q2.</b> Delta decides its airplanes will last 34 years instead of 30. What happens to yearly depreciation expense? To net income?</li>
<li><b>Q3.</b> An airplane&rsquo;s book value is $70 million, but a buyer would pay $85 million for it. Which number is on the balance sheet? Why?</li>
</ol>
</section>

<section class="s" data-nav="Ch9 · Acquisition cost">
<p class="eyebrow">Ch9 Concepts &middot; Review</p>
<h2>Acquisition cost (cost principle)</h2>
<div class="two">
<div class="def"><p class="term">What goes into cost</p><p>Everything paid to buy the asset and get it ready to use: purchase price, sales tax, delivery, installation, legal fees; minus discounts. These costs are <b>capitalized</b>, not expensed.</p></div>
<div class="def"><p class="term">Entry at purchase</p><p>Dr PPE (+A) / Cr Cash (&minus;A) or Notes payable (+L)</p>
<p class="fine" style="margin-top:10px">EX. Price $50K &minus; discount $10K, signed a note &rarr; Dr PPE 40K / Cr Notes payable 40K</p></div>
</div>
</section>

<section class="s" data-nav="Ch9 · Two methods">
<p class="eyebrow">Ch9 Concepts &middot; Review</p>
<h2>Straight-line vs. double-declining balance</h2>
<div class="two">
<div class="def"><p class="term">Straight-line (SLM)</p><p>Annual DepExp = (Cost &minus; Residual value) &divide; Useful life. The <b>same</b> amount every year.</p></div>
<div class="def" style="border-left-color:#b8901f"><p class="term" style="color:#8a6d1f">Double-declining balance (DDM)</p><p>Annual DepExp = 2 &divide; Useful life &times; (Cost &minus; AccDep). <b>More</b> expense early, less later. The last year brings book value down to the residual value.</p></div>
</div>
<div class="key"><span class="klab">Same total</span>Both methods depreciate Cost &minus; Residual value in total and end at the residual value.</div>
</section>

<section class="s" data-nav="Ch9 · Journal entries">
<p class="eyebrow">Ch9 Concepts &middot; Review</p>
<h2>The two entries</h2>
<table class="recap">
<tr><th>Event</th><th>Entry</th><th>Effect</th></tr>
<tr><td>Buy the asset</td><td>Dr PPE (+A) / Cr Cash (&minus;A)</td><td>One asset becomes another; no expense</td></tr>
<tr><td>Year-end depreciation (AJE)</td><td>Dr Depreciation expense (+E) / Cr Accumulated depreciation (+xA)</td><td>PPE, net &darr;, net income &darr;, no cash</td></tr>
</table>
<p class="fine" style="margin-top:16px">Book value (PPE, net) = Cost &minus; Accumulated depreciation.</p>
</section>

<section class="s" data-nav="Sources">
<p class="eyebrow">Sources</p>
<h2>Where the numbers come from</h2>
<ul class="srcs">
<li><a href="{DAL_URL}" target="_blank">Delta Air Lines, Inc. Form 10-K, year ended Dec 31, 2025: balance sheet, statement of operations, cash flows, and the property and equipment note</a></li>
</ul>
<p class="fine" style="margin-top:22px">Amounts in $ millions. Condensed lines (other current assets, other noncurrent assets, total liabilities, all other operating expenses) are derived from reported totals. &ldquo;Depreciation&rdquo; includes the amortization of equipment under finance leases. The $100 million airplane is a made-up example that uses Delta&rsquo;s stated policy.</p>
</section>
'''
open(os.path.join(OUT, 'Ch9-PPE-RealLife.html'), 'w', encoding='utf-8').write(head + '\n' + body + '\n' + tail)
print('wrote Ch9-PPE-RealLife')
