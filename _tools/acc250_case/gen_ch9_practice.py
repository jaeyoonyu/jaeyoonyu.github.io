#!/usr/bin/env python3
"""Ch9 practice: acquisition cost, straight-line and double-declining depreciation for one machine.

Usage: python _tools/acc250_case/gen_ch9_practice.py assets/ACC250
Writes Ch9-Practice-Worksheet.html (front: cost and straight-line, back: double-declining)
and Ch9-Practice-Slides.html (review slides; shell = Ch8-Practice-Slides.html).
Styles and helpers follow gen_ch8_practice.py.
"""
import os, re, sys

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
ch8 = open(os.path.join(HERE, 'gen_ch8_practice.py'), encoding='utf-8').read()
CSS = re.search(r"CSS = (open\(.*?'''.*?''')", ch8, re.S).group(1)
CSS = eval(CSS.replace("os.path.join(HERE, 'case.css')", repr(os.path.join(HERE, 'case.css'))))
CSS += '''
table.cost { border-collapse:collapse; font-size:10.5pt; width:100%; margin:2pt 0 4pt; }
table.cost td { padding:3pt 10pt 1pt; vertical-align:bottom; }
table.cost td.amt { width:1.1in; text-align:right; }
table.cost tr.tot td { border-top:.8pt solid #000; font-weight:700; padding-top:6pt; }
table.sched { border-collapse:collapse; font-size:10.5pt; width:100%; margin:3pt 0 2pt; }
table.sched th { font:700 8.8pt Arial,sans-serif; text-align:right; padding:3pt 8pt; background:#ffe14d;
  -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.sched th:first-child, table.sched td:first-child { text-align:center; width:.7in; }
table.sched td { padding:8pt 8pt 2pt; text-align:right; }
table.sched td.given { color:#000; }
table.sched tr.tot td { border-top:.8pt solid #000; font-weight:700; }
.formula { font-size:10.5pt; margin:3pt 0 5pt; }
.pair2 { display:grid; grid-template-columns:1fr 1fr; gap:.35in; align-items:start; margin-top:10pt; }
'''


def bl(a, cls='amt'):
    return f'<span class="bl {cls}" data-a="{a}"></span>'


def inl(a):
    return f'<span class="bl inl amt" data-a="{a}"></span>'


def pick(opts, right):
    return '<span class="pick">' + ' / '.join(f'<i{" class=\"r\"" if o == right else ""}>{o}</i>' for o in opts) + '</span>'


def je(entries):
    rows = ['<table class="je3"><tr><th>Date</th><th>Account</th><th class="r">Debit</th><th class="r">Credit</th></tr>']
    for d, dr, cr, amt in entries:
        rows.append(f'<tr class="first"><td class="d">{d}</td><td>{bl(dr, "nm")}</td><td class="amt">{bl(amt)}</td><td class="amt"></td></tr>')
        rows.append(f'<tr class="cr"><td></td><td>{bl(cr, "nm")}</td><td class="amt"></td><td class="amt">{bl(amt)}</td></tr>')
    rows.append('</table>')
    return ''.join(rows)


def tacct(title, debits, credits, bal_label, bal, side):
    n = max(len(debits), len(credits))
    rows = [f'<table class="tacct"><tr><th colspan="4">{title}</th></tr>']
    for i in range(n):
        dl, da = debits[i] if i < len(debits) else ('', None)
        cl, ca = credits[i] if i < len(credits) else ('', None)
        rows.append(f'<tr><td class="lab">{dl}</td><td class="amt dr">{bl(da) if da else ""}</td>'
                    f'<td class="lab cl">{cl}</td><td class="amt">{bl(ca) if ca else ""}</td></tr>')
    if side == 'dr':
        rows.append(f'<tr class="bal"><td class="lab">{bal_label}</td><td class="amt dr">{bl(bal)}</td><td class="lab cl"></td><td class="amt"></td></tr>')
    else:
        rows.append(f'<tr class="bal"><td class="lab"></td><td class="amt dr"></td><td class="lab cl">{bal_label}</td><td class="amt">{bl(bal)}</td></tr>')
    rows.append('</table>')
    return ''.join(rows)


COLORS = {'start': '#5c6863', 'buy': '#5b7f95', 'aje': '#8a6d1f', 'end': '#1a7a5e'}


def timeline(events, W=740, H=92, x0=70, x1=670, y=40, fs=(13, 12, 12), r=7, sw=2.5):
    """events: (position 0..1, label, line 1, line 2, kind)."""
    out = [f'<svg class="tl" viewBox="0 0 {W} {H}" role="img" aria-label="Timeline">',
           f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#16263a" stroke-width="{sw}"/>',
           f'<polygon points="{x1},{y-2*r//1.4} {x1+r*1.5},{y} {x1},{y+2*r//1.4}" fill="#16263a"/>']
    for p, lab, l1, l2, k in events:
        c = COLORS[k]; x = x0 + p * (x1 - x0 - 30)
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{c}" stroke="#fff" stroke-width="2"/>')
        out.append(f'<text x="{x:.1f}" y="{y-r*2.3:.0f}" text-anchor="middle" font-weight="700" font-size="{fs[0]}" fill="#16263a">{lab}</text>')
        out.append(f'<text x="{x:.1f}" y="{y+r*3.7:.0f}" text-anchor="middle" font-size="{fs[1]}" font-weight="700" fill="{c}">{l1}</text>')
        if l2:
            out.append(f'<text x="{x:.1f}" y="{y+r*6:.0f}" text-anchor="middle" font-size="{fs[2]}" fill="#333">{l2}</text>')
    out.append('</svg>')
    return ''.join(out)


EVENTS = [(0.0, "Jan 1, 2026", "Buy the roaster", "Cost = ?", "buy"),
          (0.25, "Dec 31, 2026", "AJE", "Year 1", "aje"),
          (0.5, "Dec 31, 2027", "AJE", "Year 2", "aje"),
          (0.75, "Dec 31, 2028", "AJE", "Year 3", "aje"),
          (1.0, "Dec 31, 2029", "AJE", "Year 4, BV = 4,000", "end")]

# ---------------------------------------------------------------- numbers
COST, RES, LIFE = 80000, 4000, 4
SLM = [(1, 80000, 19000, 19000, 61000), (2, 61000, 19000, 38000, 42000),
       (3, 42000, 19000, 57000, 23000), (4, 23000, 19000, 76000, 4000)]
DDM = [(1, 80000, 40000, 40000, 40000), (2, 40000, 20000, 60000, 20000),
       (3, 20000, 10000, 70000, 10000), (4, 10000, 6000, 76000, 4000)]
f = '{:,}'.format


def sched(rows, total):
    out = ['<table class="sched"><tr><th>Year</th><th>Beg BV</th><th>DepExp</th><th>AccDep (end)</th><th>Ending BV</th></tr>']
    for y, beg, dep, acc, end in rows:
        out.append(f'<tr><td>{y}</td><td>{bl(f(beg))}</td><td>{bl(f(dep))}</td><td>{bl(f(acc))}</td><td>{bl(f(end))}</td></tr>')
    out.append(f'<tr class="tot"><td>Total</td><td></td><td>{bl(total)}</td><td></td><td></td></tr></table>')
    return ''.join(out)


front = f'''<h1>Depreciation Step by Step: Straight-Line Method</h1>
<p class="intro2"><b>Campus Brew Co.</b> (a made-up company) roasts coffee for cafes. Its year ends on <b>December 31</b>.</p>

<div class="given"><b class="t">The purchase</b>
<ul>
<li><b>Jan 1, 2026:</b> Bought a coffee roaster. List price <b>$76,000</b>, less a <b>$4,000</b> discount. Also paid sales tax <b>$5,000</b>, delivery <b>$1,200</b> and installation <b>$1,800</b>. Everything was paid in <b>cash</b>.</li>
<li>Expected <b>useful life: 4 years</b>. Expected <b>residual value: $4,000</b> (what it can be sold for after 4 years).</li>
<li>Campus Brew uses the <b>straight-line method</b> and records depreciation in an adjusting entry every <b>Dec 31</b>.</li>
</ul></div>
{timeline(EVENTS)}

<div class="pair">
<div>
<h2>1. Acquisition cost</h2>
<table class="cost">
<tr><td>List price</td><td class="amt">76,000</td></tr>
<tr><td>Less: Discount</td><td class="amt">(4,000)</td></tr>
<tr><td>Sales tax</td><td class="amt">5,000</td></tr>
<tr><td>Delivery</td><td class="amt">1,200</td></tr>
<tr><td>Installation</td><td class="amt">1,800</td></tr>
<tr class="tot"><td>Acquisition cost</td><td class="amt">{bl("80,000")}</td></tr>
</table>
<p class="hint">All of these are capitalized: they get the roaster ready to use.</p>
</div>
<div>
<h2>2. Journal entry at purchase</h2>
{je([("Jan 1", "PPE (+A)", "Cash (&minus;A)", "80,000")])}
</div>
</div>

<div class="pair">
<div>
<h2>3. Adjusting journal entry (AJE), Dec 31, 2026</h2>
<p class="formula">Annual DepExp = (Cost &minus; Residual value) &divide; Useful life = {inl("19,000")}</p>
{je([("Dec 31", "DepExp (+E)", "AccDep (+xA)", "19,000")])}
</div>
<div>
<h2>4. T-account for AccDep</h2>
{tacct("Accumulated Depreciation", [], [("Dec 31, 2026", "19,000"), ("Dec 31, 2027", "19,000")], "End. bal. 2027", "38,000", "cr")}
</div>
</div>

<h2 class="sumh">5. Straight-line schedule</h2>
{sched(SLM, "76,000")}
<p class="hint">Beg BV = last year&rsquo;s Ending BV. &nbsp; Ending BV = Cost &minus; AccDep.</p>
'''

back = f'''<h1 style="margin-top:0">The Same Roaster: Double-Declining Balance Method</h1>
<p class="intro2">Suppose Campus Brew used the <b>double-declining balance method</b> instead. Cost <b>$80,000</b>, residual value <b>$4,000</b>, useful life <b>4 years</b>, bought Jan 1, 2026.</p>

<div class="pair">
<div>
<h2>6. The rate and Year 1</h2>
<p class="formula">Rate = 2 &divide; Useful life = {inl("50%")}</p>
<p class="formula">Year 1 DepExp = Rate &times; (Cost &minus; AccDep) = {inl("40,000")}</p>
<p class="formula">Year 4 (the last year): DepExp = Beg BV &minus; Residual value = {inl("6,000")}</p>
</div>
<div>
<h2>7. AJE, Dec 31, 2026 (DDM)</h2>
{je([("Dec 31", "DepExp (+E)", "AccDep (+xA)", "40,000")])}
</div>
</div>

<h2 class="sumh">8. Double-declining schedule</h2>
{sched(DDM, "76,000")}
<p class="hint">The last year is not 50% of Beg BV: it brings Ending BV down to the residual value.</p>

<div class="pair2">
<div>
<h2>9. Compare the two methods</h2>
<table class="sched">
<tr><th>Year</th><th>SLM DepExp</th><th>DDM DepExp</th></tr>
<tr><td>1</td><td>{bl("19,000")}</td><td>{bl("40,000")}</td></tr>
<tr><td>2</td><td>{bl("19,000")}</td><td>{bl("20,000")}</td></tr>
<tr><td>3</td><td>{bl("19,000")}</td><td>{bl("10,000")}</td></tr>
<tr><td>4</td><td>{bl("19,000")}</td><td>{bl("6,000")}</td></tr>
<tr class="tot"><td>Total</td><td>{bl("76,000")}</td><td>{bl("76,000")}</td></tr>
</table>
</div>
<div>
<h2>10. What it means</h2>
<div class="tq">
<p>Higher depreciation expense in 2026: {pick(["SLM", "DDM"], "DDM")}</p>
<p>Higher net income in 2026: {pick(["SLM", "DDM"], "SLM")}</p>
<p>Total depreciation over 4 years: {pick(["same", "different"], "same")}</p>
<p>Book value at Dec 31, 2029: {pick(["same", "different"], "same")}</p>
<p>Does the Dec 31 entry use cash? {pick(["yes", "no"], "no")}</p>
</div>
</div>
</div>
'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ch9 Practice Worksheet</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="bar">
  <button id="kbtn" onclick="toggleKey()">Show answers</button>
  <button onclick="print()">Print</button>
</div>
<div class="page">
<header>
  <div class="course">ACC 250 &middot; Ch9 Worksheet<span class="keytag"> &middot; Answer key</span></div>
  <div class="name">Name <span></span></div>
</header>
{front}
</div>
<div class="page">
{back}
</div>
<script>
function toggleKey() {{
  const on = document.documentElement.classList.toggle('key');
  const b = document.getElementById('kbtn');
  b.textContent = on ? 'Hide answers' : 'Show answers';
  b.classList.toggle('on', on);
}}
if (location.hash === '#key') toggleKey();
</script>
</body>
</html>
'''
open(os.path.join(OUT, 'Ch9-Practice-Worksheet.html'), 'w', encoding='utf-8').write(html)
print('wrote Ch9-Practice-Worksheet')

# ---------------------------------------------------------------- slides
lines = open(os.path.join(OUT, 'Ch8-Practice-Slides.html'), encoding='utf-8').read().split('\n')
cut1 = next(i for i, l in enumerate(lines) if l.startswith('<div id="stage">')) + 1
cut2 = next(i for i, l in enumerate(lines) if l.startswith('<div id="bar">'))
head = '\n'.join(lines[:cut1]).replace('<title>Ch8 Practice Review</title>', '<title>Ch9 Practice Review</title>')
tail = '\n'.join(lines[cut2:])
head = head.replace('</style>', '''
table.sch { border-collapse:collapse; font-size:28px; background:var(--card); width:100%; }
table.sch th { background:#ffe14d; padding:10px 20px; text-align:right; font:700 22px "Segoe UI",sans-serif; }
table.sch th:first-child, table.sch td:first-child { text-align:center; }
table.sch td { padding:12px 20px 6px; text-align:right; border-bottom:1px solid var(--line, #ddd); }
table.sch tr.tot td { border-top:2px solid var(--ink); font-weight:700; }
table.sch td.y { background:#fdf6e3; }
</style>''', 1)


def sje(rows):
    out = ['<table class="je"><tr><th>Date &middot; Account</th><th>Debit</th><th>Credit</th></tr>']
    for d, dr, cr, amt in rows:
        out.append(f'<tr><td>{d} &nbsp;{dr}</td><td>{amt}</td><td></td></tr>')
        out.append(f'<tr><td class="cr">{cr}</td><td></td><td>{amt}</td></tr>')
    out.append('</table>')
    return ''.join(out)


def ssched(rows, last_hl=False):
    out = ['<table class="sch"><tr><th>Year</th><th>Beg BV</th><th>DepExp</th><th>AccDep</th><th>Ending BV</th></tr>']
    for y, beg, dep, acc, end in rows:
        hl = ' class="y"' if last_hl and y == 4 else ''
        out.append(f'<tr><td>{y}</td><td>{f(beg)}</td><td{hl}>{f(dep)}</td><td>{f(acc)}</td><td>{f(end)}</td></tr>')
    out.append('<tr class="tot"><td>Total</td><td></td><td>76,000</td><td></td><td></td></tr></table>')
    return ''.join(out)


STL = timeline(EVENTS, W=1400, H=170, x0=110, x1=1290, y=70, fs=(24, 22, 21), r=13, sw=4)
STL = STL.replace('class="tl"', 'style="width:100%;height:auto;display:block;font-family:\'Segoe UI\',system-ui,sans-serif"')

body = f'''
<section class="s title" data-nav="Cover">
<div class="tstack">
<p class="eyebrow">ACC 250 &middot; Ch9 Worksheet</p>
<h1>Depreciation Step by Step</h1>
<p class="lede">Campus Brew Co. (a made-up company) buys a coffee roaster and depreciates it by the straight-line and the double-declining balance methods.</p>
</div>
<p class="title-date">Cost $80,000 &middot; residual value $4,000 &middot; useful life 4 years</p>
</section>

<section class="s" data-nav="Timeline">
<p class="eyebrow">The roaster</p>
<h2>Bought on Jan 1, 2026; depreciated every Dec 31</h2>
{STL}
<div class="note" style="margin-top:20px">One purchase entry, then one adjusting entry at the end of each of the 4 years.</div>
</section>

<section class="s" data-nav="1&ndash;2 &middot; Cost and purchase">
<p class="eyebrow">Steps 1 and 2</p>
<h2>Acquisition cost and the purchase entry</h2>
<div class="two">
<div><table class="sch" style="width:auto">
<tr><th style="text-align:left">Item</th><th>$</th></tr>
<tr><td style="text-align:left">List price</td><td>76,000</td></tr>
<tr><td style="text-align:left">Less: Discount</td><td>(4,000)</td></tr>
<tr><td style="text-align:left">Sales tax</td><td>5,000</td></tr>
<tr><td style="text-align:left">Delivery</td><td>1,200</td></tr>
<tr><td style="text-align:left">Installation</td><td>1,800</td></tr>
<tr class="tot"><td style="text-align:left">Acquisition cost</td><td><span class="hl">80,000</span></td></tr>
</table></div>
<div>{sje([("Jan 1", "PPE (+A)", "Cash (&minus;A)", "80,000")])}
<div class="key" style="margin-top:22px"><span class="klab">Cost principle</span>Every cost to get the roaster ready to use is capitalized. No expense on Jan 1.</div></div>
</div>
</section>

<section class="s" data-nav="3&ndash;4 &middot; AJE and AccDep">
<p class="eyebrow">Steps 3 and 4</p>
<h2>The year-end adjustment (straight-line)</h2>
<div class="two">
<div><p class="big">(80,000 &minus; 4,000) &divide; 4 = <span class="hl">19,000</span></p>
{sje([("Dec 31, 2026", "Depreciation Exp (+E)", "AccDep (+xA, &minus;A)", "19,000")])}</div>
<div><table class="tacct"><tr><th colspan="4">Accumulated Depreciation</th></tr>
<tr><td class="l"></td><td class="a dr"></td><td class="l cl">Dec 31, 2026</td><td class="a">19,000</td></tr>
<tr><td class="l"></td><td class="a dr"></td><td class="l cl">Dec 31, 2027</td><td class="a">19,000</td></tr>
<tr class="bal"><td class="l"></td><td class="a dr"></td><td class="l cl">End. bal.</td><td class="a">38,000</td></tr></table></div>
</div>
<div class="note" style="margin-top:20px">The AJE does not touch PPE or Cash. PPE stays at cost (80,000); AccDep grows by 19,000 every year.</div>
</section>

<section class="s" data-nav="5 &middot; SLM schedule">
<p class="eyebrow">Step 5</p>
<h2>Straight-line schedule</h2>
{ssched(SLM)}
<div class="key"><span class="klab">Check</span>Ending BV = Cost &minus; AccDep. After 4 years: 80,000 &minus; 76,000 = 4,000, the residual value.</div>
</section>

<section class="s" data-nav="6&ndash;7 &middot; DDM rate">
<p class="eyebrow">Steps 6 and 7</p>
<h2>Double-declining: the rate and Year 1</h2>
<div class="two">
<div><p class="big">Rate = 2 &divide; 4 = <span class="hl">50%</span></p>
<p class="big">Year 1 = 50% &times; (80,000 &minus; 0) = <span class="hl">40,000</span></p></div>
<div>{sje([("Dec 31, 2026", "Depreciation Exp (+E)", "AccDep (+xA, &minus;A)", "40,000")])}</div>
</div>
<div class="note" style="margin-top:20px">Residual value is <b>not</b> subtracted in the DDM formula. It only matters in the last year.</div>
</section>

<section class="s" data-nav="8 &middot; DDM schedule">
<p class="eyebrow">Step 8</p>
<h2>Double-declining schedule</h2>
{ssched(DDM, last_hl=True)}
<div class="key"><span class="klab">Last year</span>50% &times; 10,000 would be 5,000, but the last year brings BV down to the residual value: 10,000 &minus; 4,000 = <b>6,000</b>.</div>
</section>

<section class="s" data-nav="9&ndash;10 &middot; Compare">
<p class="eyebrow">Steps 9 and 10</p>
<h2>Same total, different timing</h2>
<div class="hbars">
<div class="hbar"><span>Year 1 SLM</span><div class="track"><div class="fill" style="width:47.5%;background:#1a7a5e"></div></div><span class="v">19,000</span></div>
<div class="hbar"><span>Year 1 DDM</span><div class="track"><div class="fill" style="width:100%;background:#b3200f"></div></div><span class="v">40,000</span></div>
<div class="hbar"><span>Year 4 SLM</span><div class="track"><div class="fill" style="width:47.5%;background:#1a7a5e"></div></div><span class="v">19,000</span></div>
<div class="hbar"><span>Year 4 DDM</span><div class="track"><div class="fill" style="width:15%;background:#b3200f"></div></div><span class="v">6,000</span></div>
</div>
<div class="note" style="margin-top:22px">DDM: more expense early, so <b>lower net income in 2026</b>. Both total <b>76,000</b> and end at a BV of <b>4,000</b>.</div>
</section>

<section class="s" data-nav="Takeaways">
<p class="eyebrow">Takeaways</p>
<h2>What to remember</h2>
<ol class="steps">
<li><b>Cost</b> = price &minus; discount + tax, delivery, installation: all capitalized.</li>
<li><b>SLM</b>: (Cost &minus; Residual value) &divide; Useful life, the same every year.</li>
<li><b>DDM</b>: 2 &divide; Useful life &times; (Cost &minus; AccDep); the last year ends at the residual value.</li>
<li><b>Dr Depreciation expense, Cr AccDep</b>: an expense with no cash. Book value = Cost &minus; AccDep.</li>
</ol>
</section>
'''
open(os.path.join(OUT, 'Ch9-Practice-Slides.html'), 'w', encoding='utf-8').write(head + '\n' + body + '\n' + tail)
print('wrote Ch9-Practice-Slides')
