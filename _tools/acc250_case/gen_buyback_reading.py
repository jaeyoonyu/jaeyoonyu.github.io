#!/usr/bin/env python3
"""Ch11 reading assignment: stock buybacks, shares outstanding and EPS (two pages, Letter).

Usage: python _tools/acc250_case/gen_buyback_reading.py assets/ACC250
Writes Ch11-Buyback-Reading.html; print it to Ch11-Buyback-Reading.pdf and -Key.pdf (#key view).
Terms and examples follow the Ch11 handout (authorized/issued/treasury/outstanding shares,
SHE, EPS = NI / average shares outstanding).
"""
import math, os, sys

OUT = sys.argv[1]
BLUE, PINK, GRAY, GREEN = '#3333b3', '#e57373', '#c9c9c9', '#1a7a5e'
FONT = 'font-family="Arial,Helvetica,sans-serif"'


def pizza(cx, cy, r, n, owned=(), gone=(), label_inside=None):
    """A company as a pizza cut into n slices. owned: slice indexes shaded blue; gone: slices removed (dashed outline)."""
    s = []
    for k in range(n):
        a0, a1 = -math.pi / 2 + 2 * math.pi * k / n, -math.pi / 2 + 2 * math.pi * (k + 1) / n
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        d = f'M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z'
        if k in gone:
            s.append(f'<path d="{d}" fill="#fff" stroke="#999" stroke-width="1.2" stroke-dasharray="4 3"/>')
        else:
            s.append(f'<path d="{d}" fill="{BLUE if k in owned else "#f4c26b"}" stroke="#fff" stroke-width="2.5"/>')
    if label_inside:
        s.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="13" font-weight="700" {FONT}>{label_inside}</text>')
    return ''.join(s)


def eq_pizza(cx, cy, r, n, sliced, slice_angle=None):
    """Pizza of n equal slices (all yellow) — used for the EPS figure."""
    return pizza(cx, cy, r, n, gone=sliced)


# Figure 1: a share is a slice of the company
FIG1 = f'''<svg viewBox="0 0 640 170" {FONT}>
{pizza(95, 85, 70, 10, owned=(0,))}
<text x="190" y="52" font-size="14"><tspan font-weight="700">The company</tspan> = the whole pizza</text>
<text x="190" y="76" font-size="14">10 shares outstanding = 10 equal slices</text>
<rect x="190" y="92" width="14" height="14" fill="{BLUE}"/><text x="210" y="104" font-size="14">You own 1 share = 1 slice = <tspan font-weight="700">10% of the company</tspan></text>
<text x="190" y="128" font-size="14">Each slice gets an equal share of the profit (net income)</text>
<text x="190" y="150" font-size="14">and of what is left for owners (SHE = A &minus; L).</text>
</svg>'''

# Figure 2: authorized / issued / unissued / treasury / outstanding (Ch11 handout example)
W = 560 / 1000   # px per thousand shares
x0 = 40
FIG2 = f'''<svg viewBox="0 0 640 150" {FONT}>
<line x1="{x0}" y1="22" x2="{x0 + 1000*W}" y2="22" stroke="#000"/><line x1="{x0}" y1="16" x2="{x0}" y2="28" stroke="#000"/><line x1="{x0 + 1000*W}" y1="16" x2="{x0 + 1000*W}" y2="28" stroke="#000"/>
<text x="{x0 + 500*W}" y="14" text-anchor="middle" font-size="13" font-weight="700">Authorized 1,000K</text>
<line x1="{x0}" y1="44" x2="{x0 + 700*W}" y2="44" stroke="#000"/><line x1="{x0}" y1="38" x2="{x0}" y2="50" stroke="#000"/><line x1="{x0 + 700*W}" y1="38" x2="{x0 + 700*W}" y2="50" stroke="#000"/>
<text x="{x0 + 350*W}" y="38" text-anchor="middle" font-size="13" font-weight="700">Issued 700K (sold to investors at some point)</text>
<rect x="{x0}" y="56" width="{600*W}" height="40" fill="{BLUE}"/>
<rect x="{x0 + 600*W}" y="56" width="{100*W}" height="40" fill="{PINK}"/>
<rect x="{x0 + 700*W}" y="56" width="{300*W}" height="40" fill="{GRAY}"/>
<text x="{x0 + 300*W}" y="81" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Outstanding 600K</text>
<text x="{x0 + 650*W}" y="81" text-anchor="middle" font-size="12" font-weight="700">Treasury</text>
<text x="{x0 + 850*W}" y="81" text-anchor="middle" font-size="13" font-weight="700">Unissued 300K</text>
<text x="{x0 + 300*W}" y="114" text-anchor="middle" font-size="12">held by shareholders</text>
<text x="{x0 + 650*W}" y="114" text-anchor="middle" font-size="12">100K, bought back;</text>
<text x="{x0 + 650*W}" y="128" text-anchor="middle" font-size="12">held by the company</text>
<text x="{x0 + 850*W}" y="114" text-anchor="middle" font-size="12">never sold</text>
</svg>'''

# Figure 3: what happens in a buyback (cash out, shares back)
FIG3 = f'''<svg viewBox="0 0 640 120" {FONT}>
<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="11" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 Z" fill="context-stroke"/></marker></defs>
<rect x="20" y="30" width="200" height="60" rx="8" fill="#fff" stroke="#000" stroke-width="1.5"/>
<text x="120" y="56" text-anchor="middle" font-size="14" font-weight="700">The company</text><text x="120" y="76" text-anchor="middle" font-size="12">holds them as treasury stock</text>
<rect x="420" y="30" width="200" height="60" rx="8" fill="#fff" stroke="#000" stroke-width="1.5"/>
<text x="520" y="56" text-anchor="middle" font-size="14" font-weight="700">Shareholders</text><text x="520" y="76" text-anchor="middle" font-size="12">who choose to sell</text>
<line x1="226" y1="46" x2="414" y2="46" stroke="{GREEN}" stroke-width="3" marker-end="url(#ar)"/>
<text x="320" y="38" text-anchor="middle" font-size="13" fill="{GREEN}" font-weight="700">Cash</text>
<line x1="414" y1="74" x2="226" y2="74" stroke="{BLUE}" stroke-width="3" marker-end="url(#ar)"/>
<text x="320" y="96" text-anchor="middle" font-size="13" fill="{BLUE}" font-weight="700">Shares</text>
</svg>'''


# Figure 4: balance sheet before / after a $100 buyback (stacked bars)
def bs_bar(x, a, l, she, title):
    k = 0.16
    y0 = 200
    return f'''<rect x="{x}" y="{y0 - a*k}" width="70" height="{a*k}" fill="{GREEN}"/>
<text x="{x+35}" y="{y0 - a*k/2 + 5}" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">A {a:,}</text>
<rect x="{x+78}" y="{y0 - l*k}" width="70" height="{l*k}" fill="{GRAY}"/>
<text x="{x+113}" y="{y0 - l*k/2 + 5}" text-anchor="middle" font-size="13" font-weight="700">L {l:,}</text>
<rect x="{x+78}" y="{y0 - (l+she)*k}" width="70" height="{she*k}" fill="{BLUE}"/>
<text x="{x+113}" y="{y0 - l*k - she*k/2 + 5}" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">SHE {she:,}</text>
<text x="{x+74}" y="{y0 + 18}" text-anchor="middle" font-size="13" font-weight="700">{title}</text>'''


FIG4 = f'''<svg viewBox="0 28 640 197" {FONT}>
{bs_bar(30, 1000, 400, 600, 'Before')}
{bs_bar(462, 900, 400, 500, 'After a $100 buyback')}
<text x="320" y="96" text-anchor="middle" font-size="26">&rarr;</text>
<text x="320" y="124" text-anchor="middle" font-size="12">Cash &darr; 100 &rArr; A &darr; 100</text>
<text x="320" y="141" text-anchor="middle" font-size="12">Treasury stock &uarr; 100 &rArr; SHE &darr; 100</text>
<text x="320" y="158" text-anchor="middle" font-size="12">L: no change</text>
</svg>'''

# Figure 5: EPS — same pizza (net income), fewer slices
FIG5 = f'''<svg viewBox="0 0 640 190" {FONT}>
{pizza(150, 85, 70, 10)}
<text x="150" y="172" text-anchor="middle" font-size="13"><tspan font-weight="700">Before:</tspan> $100 &divide; 10 shares = <tspan font-weight="700">$10.00</tspan> each</text>
<text x="320" y="92" text-anchor="middle" font-size="26">&rarr;</text>
<text x="320" y="62" text-anchor="middle" font-size="12">buy back</text><text x="320" y="122" text-anchor="middle" font-size="12">2 shares</text>
{pizza(490, 85, 70, 8)}
<text x="490" y="172" text-anchor="middle" font-size="13"><tspan font-weight="700">After:</tspan> $100 &divide; 8 shares = <tspan font-weight="700">$12.50</tspan> each</text>
<text x="150" y="8" text-anchor="middle" font-size="12" dy="4">Net income $100 (same pizza)</text>
<text x="490" y="8" text-anchor="middle" font-size="12" dy="4">Net income $100 (same pizza)</text>
</svg>'''


def blank(ans, w='1.0in'):
    return f'<span class="ans" style="min-width:{w}" data-a="{ans}"></span>'


CSS = '''*{box-sizing:border-box}html{background:#e9ecea}body{margin:0;font:10.5pt/1.36 "Times New Roman",Times,serif;color:#000}
.page{width:8.5in;height:11in;margin:18px auto;background:#fff;padding:.45in .65in .4in;position:relative;box-shadow:0 6px 24px rgba(0,0,0,.15);overflow:hidden}
header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2pt solid #000;padding-bottom:3pt;margin-bottom:8pt;font:700 8.5pt Arial,sans-serif}
header .name span{display:inline-block;width:2in;border-bottom:.8pt solid #000}
h1{font-size:15pt;margin:0 0 2pt}.sub{margin:0 0 8pt;font-style:italic}
h2{font:700 11pt Arial,sans-serif;margin:9pt 0 3pt;color:#3333b3}
p{margin:0 0 5pt;text-align:justify}
svg{display:block;width:100%;height:auto;margin:2pt 0 2pt}
.fig{margin:2pt 0 6pt}.fig svg{margin:2pt auto}.w70 svg{width:68%}.w75 svg{width:76%}.w80 svg{width:80%}.w88 svg{width:88%}.cap{font:8.5pt Arial,sans-serif;text-align:center;margin:0}
.def{border:.8pt solid #e57373;border-radius:6pt;padding:4pt 9pt;margin:4pt 0 6pt}
.def p{margin:1pt 0;text-align:left}
.je{display:inline-block;border:.8pt solid #e57373;border-radius:6pt;padding:3pt 10pt;margin:2pt 0 4pt 18pt}
.je table{border-collapse:collapse}.je td{padding:1pt 0;white-space:nowrap}
.je .d{font-weight:700;padding-right:9pt}.je .a{border-left:1pt solid #000;padding:1pt 30pt 1pt 9pt}.je .in{padding-left:18pt}
.je .dr{text-align:right;width:.55in}.je .cr{text-align:right;width:.55in}
table.bt{border-collapse:collapse;margin:3pt auto 6pt;font-size:10pt}
table.bt th{border-top:1.2pt solid #000;border-bottom:.6pt solid #000;padding:2pt 10pt;text-align:right;font-weight:400;white-space:nowrap}
table.bt td{padding:1.5pt 10pt;text-align:right;white-space:nowrap}table.bt tr:last-child td{border-bottom:1.2pt solid #000}
table.bt th:first-child,table.bt td:first-child{text-align:left}table.bt tr.y td{background:#fff26b;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.ex{background:#ffeb3b;font-weight:700;text-decoration:underline;padding:0 2pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
ol.q{margin:2pt 0 0;padding-left:16pt}ol.q>li{margin:0 0 9pt}
.ans{display:inline-block;border-bottom:.8pt solid #000;text-align:center;margin-left:4pt}
.ans::after{content:"\\00a0"}html.key .ans::after{content:attr(data-a);color:#b3200f;font-weight:700}
.keytag{display:none;color:#b3200f}html.key .keytag{display:inline}
.fn{position:absolute;left:.65in;right:.65in;bottom:.35in;font-size:8.5pt;border-top:.6pt solid #000;padding-top:2pt}
.fn p{margin:0 0 1pt;text-align:left}.fn a{color:#000}
.bar{position:sticky;top:0;display:flex;gap:10px;justify-content:center;padding:10px;background:#16263a;z-index:5}
.bar button{font:600 13px Arial,sans-serif;padding:7px 16px;border-radius:6px;border:0;background:#fff;cursor:pointer}
@media print{@page{size:letter;margin:0}html{background:#fff}.bar{display:none}.page{margin:0;box-shadow:none}}'''

HEAD = '<header><span>ACC250: Intro to Financial Accounting &middot; Ch11 Reading<span class="keytag"> &middot; Answer key</span></span><span class="name">Name <span></span></span></header>'

P1 = f'''<div class="page">
{HEAD}
<h1>Stock Buybacks: Fewer Shares, Bigger Slices</h1>
<p class="sub">Read before class. No prior knowledge needed; each idea builds on the one before it.</p>

<h2>1. A share is a slice of the company</h2>
<p>A corporation divides its ownership into equal pieces called <b>shares</b>. If you own some of the shares, you own that fraction of the company: a fraction of its profit and a fraction of its <b>shareholders&rsquo; equity (SHE)</b>, which is what would be left for the owners if the company sold its assets and paid off its liabilities (SHE = A &minus; L).</p>
<div class="fig w80">{FIG1}<p class="cap">Figure 1. Owning 1 of 10 shares means owning 10% of the company.</p></div>

<h2>2. Four ways to count shares</h2>
<div class="def">
<p><b>Authorized</b>: the most shares the board of directors allows the company to issue.</p>
<p><b>Issued</b>: shares the company has sold to investors at some point.</p>
<p><b>Treasury</b>: issued shares the company has <b>bought back</b> and now holds itself.</p>
<p><b>Outstanding</b>: issued shares still held by shareholders. <b>Outstanding = Issued &minus; Treasury.</b></p>
</div>
<div class="fig w88">{FIG2}<p class="cap">Figure 2. The Ch11 example: 1M authorized, 700K issued, 100K repurchased &rArr; 600K outstanding.</p></div>
<p>Only <b>outstanding</b> shares count as owners. Treasury shares get no vote, no dividends and no slice of the profit: the company cannot own a piece of itself.</p>

<h2>3. What is a buyback?</h2>
<p>In a <b>stock buyback</b> (also called a <b>share repurchase</b>), the company uses its own cash to buy its shares from investors who want to sell. The shares become <b>treasury stock</b>.</p>
<div class="fig w75">{FIG3}<p class="cap">Figure 3. Cash goes out to the sellers; the shares come back to the company.</p></div>

<h2>4. The accounting: cash down, SHE down, no expense</h2>
<p><span class="ex">EX.</span> A company pays $100 cash to buy back its own shares.</p>
<div class="je"><table>
<tr><td class="d" rowspan="2">Date:</td><td class="a">Treasury Stock (+xSE, &minus;SE)</td><td class="dr">100</td><td class="cr"></td></tr>
<tr><td class="a"><span class="in">Cash (&minus;A)</span></td><td class="dr"></td><td class="cr">100</td></tr>
</table></div>
</div>'''

P2 = f'''<div class="page">
{HEAD}
<p>Treasury stock is a <b>contra-equity</b> account: it is subtracted from SHE. It is <b>not</b> an asset and <b>not</b> an expense, so <b>net income does not change</b> (see Figure 4).</p>

<div class="fig w70">{FIG4}<p class="cap">Figure 4. A buyback shrinks both sides of the balance sheet by the cash paid.</p></div>

<h2>5. Fewer shares &rArr; higher earnings per share (EPS)</h2>
<p><b>EPS</b> = Net income &divide; Average shares outstanding.* It tells you how much profit each slice earns. A buyback does not change net income (the pizza), but there are fewer slices, so <b>each slice gets bigger</b>.</p>
<div class="fig w80">{FIG5}<p class="cap">Figure 5. Same profit, fewer shares, higher EPS.</p></div>
<p><span class="ex">EX.</span> Net income $100K; 50K shares outstanding. The company buys back 10K shares.</p>
<table class="bt"><tr><th></th><th>No buyback</th><th>Buy back 10K</th></tr>
<tr><td>Net income</td><td>$100K</td><td>$100K</td></tr><tr><td>Shares outstanding</td><td>50K</td><td>40K</td></tr>
<tr class="y"><td>EPS</td><td>$2.00</td><td>$2.50</td></tr></table>

<h2>6. Is a bigger slice always good?</h2>
<p>Not automatically. The cash paid to sellers is gone, so the company owns less. Remaining owners win only if the price paid is <b>below</b> what the shares are really worth. That is why firms tend to buy back when they think their stock price is <b>low</b> and they have more cash than good investments. <b>In the news:</b> Berkshire Hathaway, holding about $377 billion of cash, bought back $9.6 billion of its stock in Q3 2026, more than double the prior quarter.&dagger;</p>

<h2>Check your understanding</h2>
<ol class="q">
<li>A company has issued 900K shares and holds 150K treasury shares. How many shares are outstanding? {blank('750K')}</li>
<li>Net income is $240K and 60K shares are outstanding all year. What is EPS? {blank('$4.00')}</li>
<li>Same company, but it buys back 20K shares on the first day of the year. Net income is still $240K. What is EPS now? {blank('$6.00')}</li>
<li>A company buys back $50K of its own shares. Write increase, decrease or no change. Cash {blank('decrease', '.85in')} &nbsp; SHE {blank('decrease', '.85in')} &nbsp; Net income {blank('no change', '.85in')}</li>
</ol>

<div class="fn">
<p>* The examples assume the buyback happens at the start of the year, so average shares outstanding = shares after the buyback.</p>
<p>&dagger; Berkshire Hathaway Q3 2026 results (reported Nov 7, 2026); <a href="https://www.berkshirehathaway.com/reports.html">berkshirehathaway.com/reports</a>. All other numbers are made up.</p>
</div>
</div>'''

html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ch11 Reading: Stock Buybacks</title><style>{CSS}</style></head><body>
<div class="bar"><button onclick="document.documentElement.classList.toggle('key')">Show/hide answers</button><button onclick="print()">Print</button></div>
{P1}
{P2}
<script>if(location.hash==='#key')document.documentElement.classList.add('key')</script></body></html>'''
open(os.path.join(OUT, 'Ch11-Buyback-Reading.html'), 'w', encoding='utf-8').write(html)
print('wrote Ch11-Buyback-Reading.html')
