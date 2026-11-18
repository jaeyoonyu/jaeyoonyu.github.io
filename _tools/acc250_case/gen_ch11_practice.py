#!/usr/bin/env python3
"""Ch11 practice: retained earnings over several years (the deck's three "B/S example" slides).

Usage: python _tools/acc250_case/gen_ch11_practice.py assets/ACC250
Writes Ch11-Practice-Worksheet.html (front: growing RE, then dividends; back: losses)
and Ch11-Practice-Slides.html. Styles and helpers come from gen_ch9_practice.py.
"""
import os, sys

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_ch9_practice.py'), encoding='utf-8').read()
ns = {'__file__': os.path.join(HERE, 'gen_ch9_practice.py'), '__name__': 'ch9'}
exec(src.split('# ---------------------------------------------------------------- numbers')[0], ns)
CSS, bl, inl, pick, timeline, COLORS = (ns[k] for k in ('CSS', 'bl', 'inl', 'pick', 'timeline', 'COLORS'))
COLORS.update({'ni': '#1a7a5e', 'div': '#8a6d1f', 'loss': '#b3200f'})
CSS += '''
table.re { border-collapse:collapse; font-size:10.5pt; width:100%; margin:3pt 0 2pt; }
table.re th { font:700 8.8pt Arial,sans-serif; text-align:right; padding:3pt 10pt; background:#ffe14d;
  -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.re th:first-child, table.re td:first-child { text-align:left; }
table.re td { padding:6pt 10pt 1pt; text-align:right; vertical-align:bottom; }
table.re td.amt { width:1.15in; }
table.re tr.tot td { border-top:.8pt solid #000; font-weight:700; }
table.re tr.sec td { font-weight:700; font-style:italic; padding-top:7pt; }
'''


def money(v):
    return f'({-v:,})' if v < 0 else f'{v:,}'


def re_table(years, ni, div, start=0):
    """Statement of retained earnings, one column per year: Beg RE and End RE are blanks."""
    beg, rows_b, rows_e = start, [], []
    for n, d in zip(ni, div):
        end = beg + n - d
        rows_b.append(money(beg)); rows_e.append(money(end)); beg = end
    th = ''.join(f'<th>{y}</th>' for y in years)
    out = [f'<table class="re"><tr><th></th>{th}</tr>',
           '<tr><td>Beginning retained earnings</td>' + ''.join(f'<td class="amt">{bl(b)}</td>' for b in rows_b) + '</tr>',
           '<tr><td>Add: Net income (net loss)</td>' + ''.join(f'<td class="amt">{money(n)}</td>' for n in ni) + '</tr>',
           '<tr><td>Less: Dividends</td>' + ''.join(f'<td class="amt">{f"({d:,})" if d else "&ndash;"}</td>' for d in div) + '</tr>',
           '<tr class="tot"><td>Ending retained earnings</td>' + ''.join(f'<td class="amt">{bl(e)}</td>' for e in rows_e) + '</tr></table>']
    return ''.join(out)


def bs_table(years, ni, div, liab=2_000_000, cc=1_000_000):
    re_, ta, se = 0, [], []
    res = []
    for n, d in zip(ni, div):
        re_ += n - d
        res.append(re_); se.append(cc + re_); ta.append(liab + cc + re_)
    th = ''.join(f'<th>End of {y}</th>' for y in years)
    k = len(years)
    out = [f'<table class="re"><tr><th>Balance sheet</th>{th}</tr>',
           '<tr class="tot"><td>Total assets</td>' + ''.join(f'<td class="amt">{bl(money(v))}</td>' for v in ta) + '</tr>',
           '<tr class="sec"><td>Liabilities and stockholders&rsquo; equity</td>' + '<td></td>' * k + '</tr>',
           '<tr><td>Total liabilities</td>' + f'<td class="amt">{liab:,}</td>' * k + '</tr>',
           '<tr><td>Contributed capital</td>' + f'<td class="amt">{cc:,}</td>' * k + '</tr>',
           '<tr><td>Retained earnings</td>' + ''.join(f'<td class="amt">{bl(money(v))}</td>' for v in res) + '</tr>',
           '<tr class="tot"><td>Total stockholders&rsquo; equity</td>' + ''.join(f'<td class="amt">{bl(money(v))}</td>' for v in se) + '</tr>',
           '<tr class="tot"><td>Total liabilities and stockholders&rsquo; equity</td>' + ''.join(f'<td class="amt">{bl(money(v))}</td>' for v in ta) + '</tr></table>']
    return ''.join(out)


TL1 = [(0.0, "Start of Year 1", "Stock $1M, loan $2M", "RE = $0", "start"),
       (0.333, "End of Year 1", "Net income", "$200,000", "ni"),
       (0.667, "End of Year 2", "Net income", "$300,000", "ni"),
       (1.0, "End of Year 3", "Net income $400,000", "Dividends $250,000*", "div")]
TL3 = [(0.0, "Start of Year 1", "Stock $1M, loan $2M", "RE = $0", "start"),
       (0.5, "End of Year 1", "Net loss", "$600,000", "loss"),
       (1.0, "End of Year 2", "Net loss", "$800,000", "loss")]

front = f'''<h1>Retained Earnings Step by Step</h1>
<p class="intro2"><b>Lakeview Co.</b> (a made-up company) starts business at the beginning of Year 1. Its only liability is a bank loan, so <b>total liabilities stay at $2,000,000</b>.
Net income comes in as cash, and dividends are paid in cash.</p>

<div class="given"><b class="t">Case 1: Growing retained earnings</b>
<ul>
<li><b>Year 1:</b> Raised <b>$1,000,000</b> by issuing stock (contributed capital) and borrowed <b>$2,000,000</b> from a bank.</li>
<li>Net income: <b>$200,000</b> in Year 1, <b>$300,000</b> in Year 2, <b>$400,000</b> in Year 3. No dividends.</li>
</ul></div>
{timeline(TL1)}
<p class="hint" style="margin-top:-2pt">* The Year 3 dividends are for Case 2 only.</p>

<h2>1. Statement of retained earnings (Case 1)</h2>
{re_table(["Year 1", "Year 2", "Year 3"], [200_000, 300_000, 400_000], [0, 0, 0])}
<p class="hint">Ending RE = Beginning RE + Net income &minus; Dividends. &nbsp; Beginning RE = last year&rsquo;s ending RE.</p>

<h2 class="sumh">2. Balance sheet (Case 1)</h2>
{bs_table(["Year 1", "Year 2", "Year 3"], [200_000, 300_000, 400_000], [0, 0, 0])}
<p class="hint">Total assets = Total liabilities + Total stockholders&rsquo; equity.</p>
'''

back = f'''<h1 style="margin-top:0">Case 2: Dividends &nbsp;&middot;&nbsp; Case 3: Losses</h1>

<div class="given"><b class="t">Case 2: The same company pays dividends</b>
<ul><li>Everything as in Case 1, but in <b>Year 3</b> Lakeview also <b>paid $250,000 of dividends</b> in cash.</li></ul></div>

<div class="pair2">
<div>
<h2>3. Retained earnings, Year 3 (Case 2)</h2>
{re_table(["Year 3"], [400_000], [250_000], start=500_000)}
</div>
<div>
<h2>4. Year 3 effects (Case 2)</h2>
<div class="tq">
<p>Total stockholders&rsquo; equity, end of Year 3 = {inl("1,650,000")}</p>
<p>Total assets, end of Year 3 = {inl("3,650,000")}</p>
<p>Dividends reduce {pick(["net income", "retained earnings"], "retained earnings")}</p>
</div>
</div>
</div>

<div class="given" style="margin-top:12pt"><b class="t">Case 3: Accumulated deficit</b>
<ul>
<li><b>Year 1:</b> A different company raised <b>$1,000,000</b> by issuing stock and borrowed <b>$2,000,000</b>. It reported a <b>net loss of $600,000</b>.</li>
<li><b>Year 2:</b> It reported a <b>net loss of $800,000</b>. No dividends. Total liabilities stay at $2,000,000.</li>
</ul></div>
{timeline(TL3)}

<h2>5. Statement of retained earnings (Case 3)</h2>
{re_table(["Year 1", "Year 2"], [-600_000, -800_000], [0, 0])}

<h2 class="sumh">6. Balance sheet (Case 3)</h2>
{bs_table(["Year 1", "Year 2"], [-600_000, -800_000], [0, 0])}

<h2 class="sumh">7. What it means (Case 3, end of Year 2)</h2>
<div class="tq">
<p>Negative retained earnings is called {pick(["accumulated deficit", "contributed capital", "treasury stock"], "accumulated deficit")}; here it is {inl("1,400,000")}</p>
<p>Total stockholders&rsquo; equity is negative: total assets are {pick(["more", "less"], "less")} than total liabilities.</p>
</div>
'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ch11 Practice Worksheet</title>
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
  <div class="course">ACC 250 &middot; Ch11 Worksheet<span class="keytag"> &middot; Answer key</span></div>
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
open(os.path.join(OUT, 'Ch11-Practice-Worksheet.html'), 'w', encoding='utf-8').write(html)
print('wrote Ch11-Practice-Worksheet')

# ---------------------------------------------------------------- slides
lines = open(os.path.join(OUT, 'Ch9-Practice-Slides.html'), encoding='utf-8').read().split('\n')
cut1 = next(i for i, l in enumerate(lines) if l.startswith('<div id="stage">')) + 1
cut2 = next(i for i, l in enumerate(lines) if l.startswith('<div id="bar">'))
head = '\n'.join(lines[:cut1]).replace('<title>Ch9 Practice Review</title>', '<title>Ch11 Practice Review</title>')
tail = '\n'.join(lines[cut2:])


def big_tl(ev):
    s = timeline(ev, W=1400, H=170, x0=110, x1=1290, y=70, fs=(24, 22, 21), r=13, sw=4)
    return s.replace('class="tl"', 'style="width:100%;height:auto;display:block;font-family:\'Segoe UI\',system-ui,sans-serif"')


def sre(years, beg, ni, div, end, hl_last=False):
    th = ''.join(f'<th>{y}</th>' for y in years)
    def row(lab, vals, cls=''):
        return f'<tr{cls}><td style="text-align:left">{lab}</td>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>'
    return (f'<table class="sch"><tr><th style="text-align:left">Retained earnings</th>{th}</tr>'
            + row('Beginning RE', beg) + row('+ Net income (loss)', ni) + row('&minus; Dividends', div)
            + row('Ending RE', [f'<span class="hl">{e}</span>' for e in end], ' class="tot"') + '</table>')


def sbs(years, ta, re_, se):
    th = ''.join(f'<th>{y}</th>' for y in years)
    k = len(years)
    def row(lab, vals, cls=''):
        return f'<tr{cls}><td style="text-align:left">{lab}</td>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>'
    return (f'<table class="sch"><tr><th style="text-align:left">Balance sheet</th>{th}</tr>'
            + row('Total assets', ta, ' class="tot"') + row('Total liabilities', ['2,000,000'] * k)
            + row('Contributed capital', ['1,000,000'] * k) + row('Retained earnings', [f'<span class="hl">{v}</span>' for v in re_])
            + row('Total stockholders&rsquo; equity', se, ' class="tot"') + '</table>')


body = f'''
<section class="s title" data-nav="Cover">
<div class="tstack">
<p class="eyebrow">ACC 250 &middot; Ch11 Worksheet</p>
<h1>Retained Earnings Step by Step</h1>
<p class="lede">Lakeview Co. (a made-up company) over three years: growing retained earnings, dividends, and an accumulated deficit.</p>
</div>
<p class="title-date">Contributed capital $1,000,000 &middot; bank loan $2,000,000</p>
</section>

<section class="s" data-nav="The equation">
<p class="eyebrow">One equation</p>
<h2>How retained earnings changes</h2>
<p class="big" style="margin-top:30px">Ending RE = Beginning RE + Net income &minus; Dividends</p>
<div class="note" style="margin-top:30px">Net income <b>increases</b> retained earnings; a net loss and dividends <b>decrease</b> it.</div>
<div class="note">This year&rsquo;s beginning RE is last year&rsquo;s ending RE.</div>
</section>

<section class="s" data-nav="Case 1 &middot; Timeline">
<p class="eyebrow">Case 1</p>
<h2>Three years of profits</h2>
{big_tl(TL1[:3] + [(1.0, "End of Year 3", "Net income", "$400,000", "ni")])}
<div class="note" style="margin-top:20px">Total liabilities stay at 2,000,000. Net income comes in as cash.</div>
</section>

<section class="s" data-nav="1 &middot; RE (Case 1)">
<p class="eyebrow">Case 1 &middot; Step 1</p>
<h2>Statement of retained earnings</h2>
{sre(["Year 1", "Year 2", "Year 3"], ["0", "200,000", "500,000"], ["200,000", "300,000", "400,000"], ["&ndash;"] * 3, ["200,000", "500,000", "900,000"])}
<div class="key"><span class="klab">Carry it forward</span>Each year starts where the last one ended.</div>
</section>

<section class="s" data-nav="2 &middot; B/S (Case 1)">
<p class="eyebrow">Case 1 &middot; Step 2</p>
<h2>Balance sheet</h2>
{sbs(["End of Year 1", "End of Year 2", "End of Year 3"], ["3,200,000", "3,500,000", "3,900,000"], ["200,000", "500,000", "900,000"], ["1,200,000", "1,500,000", "1,900,000"])}
<div class="key"><span class="klab">Check</span>Total assets = 2,000,000 + Total stockholders&rsquo; equity.</div>
</section>

<section class="s" data-nav="3&ndash;4 &middot; Dividends (Case 2)">
<p class="eyebrow">Case 2 &middot; Steps 3 and 4</p>
<h2>Paying $250,000 of dividends in Year 3</h2>
<div class="two">
<div>{sre(["Year 3"], ["500,000"], ["400,000"], ["(250,000)"], ["650,000"])}</div>
<div>{sbs(["End of Year 3"], ["3,650,000"], ["650,000"], ["1,650,000"])}</div>
</div>
<div class="note" style="margin-top:20px">Dividends reduce <b>retained earnings</b> (and cash), not net income. RE still grows: 400,000 &gt; 250,000.</div>
</section>

<section class="s" data-nav="Case 3 &middot; Timeline">
<p class="eyebrow">Case 3</p>
<h2>Two years of losses</h2>
{big_tl(TL3)}
<div class="note" style="margin-top:20px">A net loss decreases retained earnings, just as net income increases it.</div>
</section>

<section class="s" data-nav="5&ndash;6 &middot; Losses (Case 3)">
<p class="eyebrow">Case 3 &middot; Steps 5 and 6</p>
<h2>Retained earnings below zero</h2>
<div class="two">
<div>{sre(["Year 1", "Year 2"], ["0", "(600,000)"], ["(600,000)", "(800,000)"], ["&ndash;"] * 2, ["(600,000)", "(1,400,000)"])}</div>
<div>{sbs(["Year 1", "Year 2"], ["2,400,000", "1,600,000"], ["(600,000)", "(1,400,000)"], ["400,000", "(400,000)"])}</div>
</div>
</section>

<section class="s" data-nav="7 &middot; Accumulated deficit">
<p class="eyebrow">Case 3 &middot; Step 7</p>
<h2>Accumulated deficit and negative equity</h2>
<div class="two">
<div class="def"><p class="term">Accumulated deficit</p><p>Negative retained earnings: <b>(1,400,000)</b> at the end of Year 2. The losses add up to more than all profits kept.</p></div>
<div class="def" style="border-left-color:#b8901f"><p class="term" style="color:#8a6d1f">Negative stockholders&rsquo; equity</p><p>1,000,000 + (1,400,000) = <b>(400,000)</b>. Total assets (1,600,000) are less than total liabilities (2,000,000).</p></div>
</div>
</section>

<section class="s" data-nav="Takeaways">
<p class="eyebrow">Takeaways</p>
<h2>What to remember</h2>
<ol class="steps">
<li><b>Ending RE</b> = Beginning RE + Net income &minus; Dividends.</li>
<li><b>Dividends</b> reduce retained earnings, not net income.</li>
<li>Negative retained earnings is an <b>accumulated deficit</b>.</li>
<li>Total stockholders&rsquo; equity = Contributed capital + Retained earnings; it can be negative.</li>
</ol>
</section>
'''
open(os.path.join(OUT, 'Ch11-Practice-Slides.html'), 'w', encoding='utf-8').write(head + '\n' + body + '\n' + tail)
print('wrote Ch11-Practice-Slides')
