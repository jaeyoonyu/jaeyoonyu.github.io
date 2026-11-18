#!/usr/bin/env python3
"""Ch9 opening activity: Crocs' property and equipment (Form 10-K, FY2024, the filing Ch8 uses).

Usage: python _tools/acc250_case/gen_ch9_ppe.py assets/ACC250
Writes Ch9-PPE-Worksheet.html (one page, key via #key) and Ch9-PPE-RealLife.html (slides).
Worksheet helpers come from gen_worksheets.py; the slide shell is Ch8-BadDebt-RealLife.html.
Amounts are from Crocs' 10-K for the year ended Dec 31, 2024 (accession 0001334036-25-000009):
balance sheet, Note 4 (property and equipment) and the cash flow statement. $ thousands.
Every statement line stays on one line (user, 2026-11-18).
"""
import os, sys

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_worksheets.py'), encoding='utf-8').read()
ns = {'__file__': os.path.join(HERE, 'gen_worksheets.py')}
exec(src.split('# Ch8: Crocs bad debts')[0].replace('OUT = sys.argv[1]', "OUT = ''"), ns)
stmt, qlist, page, inl, pick = ns['stmt'], ns['qlist'], ns['page'], ns['inl'], ns['pick']
ns['CSS'] += '\n.stmt td:first-child { white-space:nowrap; }\n'
page.__globals__['CSS'] = ns['CSS']

CROX_URL = 'https://www.sec.gov/Archives/edgar/data/1334036/000133403625000009/crox-20241231.htm'

# ---------------------------------------------------------------- data ($ thousands)
BS = [('Cash and cash equivalents', ('180,485', '149,288'), '$'),
      ('Accounts receivable, net', ('257,657', '305,747'), ''),
      ('Inventories', ('356,254', '385,054'), ''),
      ('Other current assets', ('77,873', '70,615'), 'u'),
      ('Total current assets', ('872,269', '910,704'), 'i'),
      ('Property and equipment, net', ('244,335', '238,315'), 'hl'),
      ('Goodwill and intangible assets', ('2,488,571', '2,504,150'), ''),
      ('Other noncurrent assets', ('1,206,978', '990,665'), 'u'),
      ('Total assets', ('4,812,153', '4,643,834'), 'i uu $')]
NOTE = [('Machinery and equipment', ('190,134', '163,919'), '$'),
        ('Leasehold improvements', ('156,091', '149,132'), ''),
        ('Furniture, fixtures, and other', ('40,702', '32,356'), ''),
        ('Construction in progress', ('10,863', '13,418'), 'u'),
        ('Property and equipment, at cost', ('?', '?'), 'i hl'),
        ('Less: Accumulated depreciation', ('(153,455)', '(120,510)'), 'u hl'),
        ('Property and equipment, net', ('244,335', '238,315'), 'i uu $ hl')]
DEP = [('In cost of sales', '20,673', '$'),
       ('In SG&amp;A expenses', '26,233', 'u'),
       ('Total depreciation expense', '46,906', 'i uu $ hl')]

# ---------------------------------------------------------------- worksheet
front = f'''<h1>Crocs: Property and Equipment in Real Financial Statements</h1>
<p class="intro2">In Ch8 we read Crocs&rsquo;s receivables. Now look at the machines, warehouses and stores it uses for years: property and equipment (PPE).</p>
<p class="filing"><b>Source:</b> Crocs, Inc. Form 10-K, year ended December 31, 2024 (condensed<sup>**</sup>; amounts in thousands) &middot;
<a href="{CROX_URL}" target="_blank">{CROX_URL.replace("https://www.", "")}</a></p>
<style>.stmt {{ font-size:9pt; }} .stmt td {{ padding:1.2pt 2pt; }} ol.qs li {{ padding:4pt 0 1pt; }} .defs {{ font-size:9.2pt !important; }}</style>
<div class="cols">
<div>
{stmt('Crocs, Inc.', 'Consolidated Balance Sheets (assets)', ('Dec 31, 2024', 'Dec 31, 2023'), BS)}
</div>
<div>
{stmt('Crocs, Inc.', 'Note 4: Property and Equipment', ('Dec 31, 2024', 'Dec 31, 2023'), NOTE)}
<div style="height:8pt"></div>
{stmt('Crocs, Inc.', 'Depreciation Expense, 2024', '2024', DEP)}
</div>
</div>
<div class="box quote"><b class="t">From the 10-K (accounting policy)</b>&ldquo;Property, equipment, furniture, and fixtures are stated at <mark>original cost, less accumulated depreciation</mark>. Depreciation is provided using the <mark>straight-line method</mark> over the estimated useful asset lives. The useful lives &hellip; typically range from <mark>2 to 10 years</mark> for machinery and equipment and furniture, fixtures and others.&rdquo;</div>
<h2>Accounts &amp; Terms</h2>
<div class="defs" style="font-size:9.6pt">
<dl>
<dt>Property and equipment (PPE), at cost</dt><dd>What the company paid to buy the assets and get them ready to use (cost principle). An asset.</dd>
<dt>Accumulated depreciation (AccDep)</dt><dd>The total depreciation recorded so far on the assets still owned. A contra-asset subtracted from PPE.</dd>
</dl>
<dl>
<dt>PPE, net (book value)</dt><dd>PPE at cost &minus; AccDep: the cost not yet depreciated. It is not the market value.</dd>
<dt>Depreciation expense</dt><dd>This year&rsquo;s share of the cost. Straight-line: (Cost &minus; Residual value) &divide; Useful life.</dd>
</dl>
</div>
<h2>Find it in the statements <small>Write the amount ($ thousands, or %).</small></h2>
<p class="sub2">Answer as of <b>December 31, 2024</b>, unless a question says otherwise.</p>
{qlist([("What did Crocs originally pay for the property and equipment it still owns (the &ldquo;?&rdquo; in Note 4)?", "397,790"),
        ("How much of that cost has been depreciated so far?", "153,455"),
        ("What is the book value of Crocs&rsquo;s property and equipment?", "244,335"),
        ("What percentage of the cost has been depreciated so far?", "38.6%"),
        ("What percentage of Crocs&rsquo;s total assets is property and equipment, net?<sup>&dagger;</sup>", "5.1%"),
        ("How much depreciation expense did Crocs record in 2024?", "46,906"),
        ("Crocs buys a warehouse machine for <b>$100,000</b>, to be used for <b>10 years</b> with <b>no residual value</b>. Straight-line depreciation per year?", "$10,000")], 1, full=True)}
<p class="fn"><sup>&dagger;</sup> Only about 5%: &ldquo;All of our footwear products are manufactured by third-party manufacturers,&rdquo; so Crocs owns no shoe factories. Compare an airline, whose airplanes are about half of its assets.</p>
<p class="fn" style="margin-top:2pt"><sup>**</sup> &ldquo;Other current assets,&rdquo; &ldquo;goodwill and intangible assets&rdquo; and &ldquo;other noncurrent assets&rdquo; combine reported lines. Depreciation also lowers net income through cost of sales and SG&amp;A; it uses no cash.</p>
'''
open(os.path.join(OUT, 'Ch9-PPE-Worksheet.html'), 'w', encoding='utf-8').write(
    page('PPE Worksheet', 'Crocs', 'ACC 250 &middot; Ch9 Opening Activity', front, '', ''))
print('wrote Ch9-PPE-Worksheet')

# ---------------------------------------------------------------- slides
SHELL = os.path.join(OUT, 'Ch8-BadDebt-RealLife.html')
lines = open(SHELL, encoding='utf-8').read().split('\n')
cut1 = next(i for i, l in enumerate(lines) if l.startswith('<div id="stage">')) + 1
cut2 = next(i for i, l in enumerate(lines) if l.startswith('<div id="bar">'))
head = '\n'.join(lines[:cut1]).replace('<title>Bad Debts in Real Life</title>', '<title>PPE in Real Life</title>')
head = head.replace('</style>', '.stmt td:first-child { white-space:nowrap; }\n</style>', 1)
tail = '\n'.join(lines[cut2:])


def rows(rs):
    out = []
    for r in rs:
        lab, v = r[0], r[1]
        cls = ' class="total"' if len(r) > 2 and r[2] == 'total' else ''
        st = ' style="background:#fdf6e3"' if len(r) > 2 and r[2] == 'hl' else ''
        out.append(f'<tr{cls}{st}><td>{lab}</td><td>{v}</td></tr>')
    return '\n'.join(out)


body = f'''
<section class="s title" data-nav="Cover">
<div class="tstack">
<p class="eyebrow">ACC 250 &middot; Ch9 Long-lived Assets</p>
<h1>A machine lasts 10 years. When is it an expense?</h1>
<p class="lede">How Crocs reports its property and equipment in its 10-K.</p>
</div>
<p class="title-date">Crocs: Form 10-K, year ended Dec 31, 2024 ($ thousands)</p>
</section>

<section class="s" data-nav="The problem">
<p class="eyebrow">The problem</p>
<h2>A purchase that lasts for years</h2>
<div class="tests">
<div class="test"><span class="n">1</span><div>Crocs pays <b>$100,000</b> cash for a machine for its distribution center.</div></div>
<div class="test"><span class="n">2</span><div>The machine will help ship shoes, and earn revenue, for about <b>10 years</b>.</div></div>
<div class="test"><span class="n">3</span><div>After 10 years it will be worth <b>nothing</b>.</div></div>
</div>
<div class="ask" style="margin-top:22px"><span class="qlab">Think about it</span><p>Should the whole $100,000 be an <b>expense</b> this year? If not, when?</p></div>
</section>

<section class="s" data-nav="Crocs balance sheet">
<p class="eyebrow">Crocs &middot; Balance sheet, Dec 31, 2024</p>
<h2>Back to the balance sheet</h2>
<div class="two">
<div class="stmt">
<h3>Assets, condensed ($ thousands)</h3>
<table>
<tr><th></th><th>$K</th></tr>
{rows([("Cash and cash equivalents", "180,485"), ("Accounts receivable, net", "257,657"), ("Inventories", "356,254"),
       ("Other current assets", "77,873"), ("Total current assets", "872,269", "total"),
       ('<b class="hl">Property and equipment, net</b>', '<span class="hl">244,335</span>', "hl"),
       ("Goodwill and intangible assets", "2,488,571"), ("Other noncurrent assets", "1,206,978"),
       ("Total assets", "4,812,153", "total")])}
</table>
</div>
<div>
<div class="note">Ch8 looked at <b>accounts receivable</b>. Now look further down: <b>property and equipment</b>.</div>
<div class="note">Crocs&rsquo;s PPE: machinery in its distribution centers, its retail stores, and furniture and computers.</div>
<div class="ask" style="margin-top:14px"><span class="qlab">Look closely</span><p>&ldquo;<b>Net</b>&rdquo; again. Net of what, this time?</p></div>
</div>
</div>
</section>

<section class="s" data-nav="Zoom in: Note 4">
<p class="eyebrow">Crocs &middot; Note 4, property and equipment</p>
<h2>Zoom in: cost, used up, and what is left</h2>
<div class="two">
<div class="stmt">
<h3>December 31, 2024 ($ thousands)</h3>
<table>
<tr><th></th><th>$K</th></tr>
{rows([("Machinery and equipment", "190,134"), ("Leasehold improvements", "156,091"),
       ("Furniture, fixtures, and other", "40,702"), ("Construction in progress", "10,863"),
       ("Property and equipment, at cost", "397,790", "total")])}
<tr><td>Less: Accumulated depreciation</td><td class="neg">(153,455)</td></tr>
<tr class="total"><td>Property and equipment, net</td><td class="hl">244,335</td></tr>
</table>
</div>
<div class="def" style="border-left-color:#b8901f"><p class="term" style="color:#8a6d1f">Accumulated depreciation</p><p>All the depreciation recorded so far on the assets Crocs still owns. A <b>contra-asset</b>: it is subtracted from cost.</p></div>
</div>
<div class="key"><span class="klab">Net = book value</span>$244.3 million is the cost <b>not yet depreciated</b>. It is not what the assets would sell for.</div>
</section>

<section class="s" data-nav="How much is used up?">
<p class="eyebrow">Crocs &middot; Putting it in perspective</p>
<h2>Out of every $100 Crocs paid for its PPE&hellip;</h2>
<div class="hbars">
<div class="hbar"><span>Not yet depreciated</span><div class="track"><div class="fill" style="width:61.4%;background:#1a7a5e"></div></div><span class="v">$61</span></div>
<div class="hbar"><span>Already depreciated</span><div class="track"><div class="fill" style="width:38.6%;background:#b3200f"></div></div><span class="v">$39</span></div>
</div>
<div class="note" style="margin-top:26px">153,455 &divide; 397,790 &asymp; <b>38.6%</b> of the cost has been depreciated so far.</div>
<div class="note">With useful lives of 2 to 10 years, Crocs keeps replacing its equipment: it paid <b>69,347</b> for new property, equipment and software in 2024.</div>
</section>

<section class="s" data-nav="How big is PPE?">
<p class="eyebrow">Crocs &middot; An asset-light company</p>
<h2>Why so little PPE?</h2>
<div class="hbars">
<div class="hbar"><span>PPE, net / total assets</span><div class="track"><div class="fill" style="width:5.1%;background:#1a7a5e"></div></div><span class="v">5.1%</span></div>
</div>
<div class="def" style="margin-top:24px"><p class="term">From the 10-K</p><p style="font-family:Charter,Georgia,serif">&ldquo;All of our footwear products are manufactured by third-party manufacturers, the majority of which are located in Vietnam, China, Indonesia, India, and Mexico.&rdquo;</p></div>
<div class="key"><span class="klab">Compare</span>Crocs owns no shoe factories. An airline&rsquo;s airplanes are about <b>half</b> of its total assets.</div>
</section>

<section class="s" data-nav="Crocs's policy">
<p class="eyebrow">Crocs &middot; Accounting policy</p>
<h2>How Crocs depreciates</h2>
<div class="def"><p class="term">From the 10-K</p><p style="font-family:Charter,Georgia,serif">&ldquo;Property, equipment, furniture, and fixtures are stated at original cost, less accumulated depreciation. Depreciation is provided using the straight-line method over the estimated useful asset lives &hellip; typically &hellip; 2 to 10 years.&rdquo;</p></div>
<div class="two" style="margin-top:18px">
<div class="note"><b>Cost</b>: what Crocs paid (cost principle).</div>
<div class="note"><b>Method</b>: straight-line, the same amount every year.</div>
</div>
<div class="note"><b>Useful life</b>: 2 to 10 years for machinery, furniture and fixtures.</div>
</section>

<section class="s" data-nav="One machine">
<p class="eyebrow">Apply Crocs&rsquo;s policy</p>
<h2>One $100,000 machine</h2>
<div class="two">
<div>
<p class="big">(100,000 &minus; 0) &divide; 10 = <span class="hl">10,000</span> per year</p>
<table class="je">
<tr><th>Every Dec 31 (adjusting entry)</th><th>Dr</th><th>Cr</th></tr>
<tr><td>Depreciation expense (+E)</td><td>10,000</td><td></td></tr>
<tr><td class="cr">Accumulated depreciation (+xA)</td><td></td><td>10,000</td></tr>
</table>
</div>
<div class="stmt">
<table>
<tr><th>After 4 years</th><th>$</th></tr>
<tr><td>Machine, at cost</td><td>100,000</td></tr>
<tr><td>Less: Accumulated depreciation</td><td class="neg">(40,000)</td></tr>
<tr class="total"><td>Machine, net (book value)</td><td class="hl">60,000</td></tr>
</table>
</div>
</div>
<div class="key"><span class="klab">Answer to slide 2</span>No. The $100,000 becomes an expense <b>10,000 at a time</b>, over the 10 years the machine helps earn revenue: the matching principle.</div>
</section>

<section class="s" data-nav="Where the expense goes">
<p class="eyebrow">Crocs &middot; 2024</p>
<h2>Depreciation expense: 46,906</h2>
<div class="two">
<div class="stmt">
<table>
<tr><th>Depreciation, 2024</th><th>$K</th></tr>
<tr><td>In cost of sales (warehouses)</td><td>20,673</td></tr>
<tr><td>In SG&amp;A (stores, offices)</td><td>26,233</td></tr>
<tr class="total"><td>Total depreciation expense</td><td class="hl">46,906</td></tr>
</table>
</div>
<div>
<div class="note">There is no separate &ldquo;depreciation&rdquo; line on Crocs&rsquo;s income statement: it is <b>inside</b> cost of sales and SG&amp;A.</div>
<div class="note">Recording it uses <b>no cash</b>. Crocs paid cash when it bought the assets.</div>
</div>
</div>
</section>

<section class="s" data-nav="Discuss">
<p class="eyebrow">Before we start Ch9</p>
<h2>Questions for you</h2>
<ol class="steps">
<li><b>Q1.</b> Crocs pays $5,000 to deliver and install a new machine. Expense this year, or part of the machine&rsquo;s cost?</li>
<li><b>Q2.</b> Crocs decides its machines will last 8 years instead of 10. What happens to yearly depreciation expense? To net income?</li>
<li><b>Q3.</b> A machine&rsquo;s book value is $60,000, but a buyer would pay $75,000 for it. Which number is on the balance sheet? Why?</li>
</ol>
</section>

<section class="s" data-nav="Ch9 &middot; Acquisition cost">
<p class="eyebrow">Ch9 Concepts &middot; Review</p>
<h2>Acquisition cost (cost principle)</h2>
<div class="two">
<div class="def"><p class="term">What goes into cost</p><p>Everything paid to buy the asset and get it ready to use: purchase price, sales tax, delivery, installation, legal fees; minus discounts. These costs are <b>capitalized</b>, not expensed.</p></div>
<div class="def"><p class="term">Entry at purchase</p><p>Dr PPE (+A) / Cr Cash (&minus;A) or Notes payable (+L)</p>
<p class="fine" style="margin-top:10px">EX. Price $50K &minus; discount $10K, signed a note &rarr; Dr PPE 40K / Cr Notes payable 40K</p></div>
</div>
</section>

<section class="s" data-nav="Ch9 &middot; Two methods">
<p class="eyebrow">Ch9 Concepts &middot; Review</p>
<h2>Straight-line vs. double-declining balance</h2>
<div class="two">
<div class="def"><p class="term">Straight-line (SLM)</p><p>Annual DepExp = (Cost &minus; Residual value) &divide; Useful life. The <b>same</b> amount every year.</p></div>
<div class="def" style="border-left-color:#b8901f"><p class="term" style="color:#8a6d1f">Double-declining balance (DDM)</p><p>Annual DepExp = 2 &divide; Useful life &times; (Cost &minus; AccDep). <b>More</b> expense early, less later. The last year brings book value down to the residual value.</p></div>
</div>
<div class="key"><span class="klab">Same total</span>Both methods depreciate Cost &minus; Residual value in total and end at the residual value.</div>
</section>

<section class="s" data-nav="Ch9 &middot; Journal entries">
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
<li><a href="{CROX_URL}" target="_blank">Crocs, Inc. Form 10-K, year ended Dec 31, 2024: balance sheet, Note 4 (property and equipment), cash flow statement, accounting policies</a></li>
</ul>
<p class="fine" style="margin-top:22px">Amounts in $ thousands. Condensed lines (other current assets, goodwill and intangible assets, other noncurrent assets) combine reported lines. The $100,000 machine is a made-up example that uses Crocs&rsquo;s stated policy.</p>
</section>
'''
open(os.path.join(OUT, 'Ch9-PPE-RealLife.html'), 'w', encoding='utf-8').write(head + '\n' + body + '\n' + tail)
print('wrote Ch9-PPE-RealLife')
