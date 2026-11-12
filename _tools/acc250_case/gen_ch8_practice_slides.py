#!/usr/bin/env python3
"""Review slides for the Ch8 practice worksheet (% of credit sales, Jan-Feb).

Usage: python _tools/acc250_case/gen_ch8_practice_slides.py assets/ACC250 assets/ACC250/Anthropic-S1.html
Uses the Anthropic-S1 deck as the slide shell (styles + navigation script).
"""
import os, sys

OUT, SHELL = sys.argv[1], sys.argv[2]
lines = open(SHELL).read().split('\n')
head = '\n'.join(lines[:535]); tail = '\n'.join(lines[734:])

COLORS = {'start': '#5c6863', 'cash': '#5b7f95', 'credit': '#1a7a5e', 'writeoff': '#b3200f', 'aje': '#8a6d1f'}


def timeline(ndays, events):
    W, x0, x1, y = 1400, 110, 1290, 70
    def X(d): return x0 + (d - 1) / (ndays - 1) * (x1 - x0)
    out = [f'<svg viewBox="0 0 {W} 160" style="width:100%;height:auto;display:block;font-family:\'Segoe UI\',system-ui,sans-serif">',
           f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#16263a" stroke-width="4"/>',
           f'<polygon points="{x1},{y-9} {x1+18},{y} {x1},{y+9}" fill="#16263a"/>']
    for d, lab, l1, l2, k in events:
        c = COLORS[k]; x = X(d)
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="13" fill="{c}" stroke="#fff" stroke-width="3"/>')
        out.append(f'<text x="{x:.1f}" y="{y-28}" text-anchor="middle" font-weight="700" font-size="24" fill="#16263a">{lab}</text>')
        out.append(f'<text x="{x:.1f}" y="{y+46}" text-anchor="middle" font-size="22" font-weight="700" fill="{c}">{l1}</text>')
        if l2:
            out.append(f'<text x="{x:.1f}" y="{y+76}" text-anchor="middle" font-size="21" fill="#333">{l2}</text>')
    out.append('</svg>')
    return ''.join(out)


def je(rows):
    out = ['<table class="je"><tr><th>Date &middot; Account</th><th>Debit</th><th>Credit</th></tr>']
    for d, dr, cr, amt in rows:
        out.append(f'<tr><td>{d} &nbsp;{dr}</td><td>{amt}</td><td></td></tr>')
        out.append(f'<tr><td class="cr">{cr}</td><td></td><td>{amt}</td></tr>')
    out.append('</table>')
    return ''.join(out)


def tacct(title, debits, credits, bal, side):
    n = max(len(debits), len(credits))
    rows = [f'<table class="tacct"><tr><th colspan="4">{title}</th></tr>']
    for i in range(n):
        dl, da = debits[i] if i < len(debits) else ('', '')
        cl, ca = credits[i] if i < len(credits) else ('', '')
        rows.append(f'<tr><td class="l">{dl}</td><td class="a dr">{da}</td><td class="l cl">{cl}</td><td class="a">{ca}</td></tr>')
    if side == 'dr':
        rows.append(f'<tr class="bal"><td class="l">End. bal.</td><td class="a dr">{bal}</td><td class="l cl"></td><td class="a"></td></tr>')
    else:
        rows.append(f'<tr class="bal"><td class="l"></td><td class="a dr"></td><td class="l cl">End. bal.</td><td class="a">{bal}</td></tr>')
    rows.append('</table>')
    return ''.join(rows)


def summary(date, gross, ada, net):
    return f'''<table class="ar3">
<tr><th></th><th>{date}</th><th class="m">What it means</th></tr>
<tr><td>Gross A/R</td><td class="a">{gross}</td><td class="m">Total A/R</td></tr>
<tr><td>Less: ADA</td><td class="a">{ada}</td><td class="m">Noncollectible A/R (estimated)</td></tr>
<tr class="tot"><td>Net A/R</td><td class="a">{net}</td><td class="m">Collectible portion of A/R</td></tr>
</table>'''


JAN_TL = timeline(31, [(1, "Jan 1", "Start", "A/R = ADA = $0", "start"),
                       (5, "Jan 5", "Cash sale", "$4,000", "cash"),
                       (10, "Jan 10", "Credit sale", "$6,000", "credit"),
                       (20, "Jan 20", "Credit sale", "$4,000", "credit"),
                       (31, "Jan 31", "AJE: BDE", "2% of credit sales", "aje")])
FEB_TL = timeline(28, [(1, "Feb 1", "Start", "Jan 31 balances", "start"),
                       (8, "Feb 8", "Cash sale", "$3,000", "cash"),
                       (15, "Feb 15", "Credit sale", "$8,000", "credit"),
                       (20, "Feb 20", "Write-off", "1% of Jan credit sales", "writeoff"),
                       (28, "Feb 28", "AJE: BDE", "2% of credit sales", "aje")])

body = f'''
<section class="s title" data-nav="Cover">
<div class="tstack">
<p class="eyebrow">ACC 250 &middot; Ch8 Worksheet</p>
<h1>Bad Debts Step by Step: % of Credit Sales Method</h1>
<p class="lede">Sneaker Supply Co. (a made-up company) expects 2% of each month&rsquo;s credit sales to be uncollectible and records BDE at the end of each month.</p>
</div>
<p class="title-date">January and February &middot; A/R and ADA start at $0 on January 1</p>
</section>

<section class="s" data-nav="January timeline">
<p class="eyebrow">January</p>
<h2>What happened in January</h2>
{JAN_TL}
<div class="note" style="margin-top:20px">Only <b>credit sales</b> create A/R, so only they carry collection risk. The cash sale is not part of the 2% estimate.</div>
</section>

<section class="s" data-nav="1&ndash;2 · Entries and A/R">
<p class="eyebrow">January &middot; Steps 1 and 2</p>
<h2>Journal entries and the A/R T-account</h2>
<div class="two">
<div>{je([("Jan 5", "Cash (+A)", "Sales Rev (+R)", "4,000"),
            ("Jan 10", "A/R (+A)", "Sales Rev (+R)", "6,000"),
            ("Jan 20", "A/R (+A)", "Sales Rev (+R)", "4,000")])}</div>
<div>{tacct("A/R", [("Jan 10", "6,000"), ("Jan 20", "4,000")], [], "10,000", "dr")}
<div class="key" style="margin-top:22px"><span class="klab">Read it from the T-account</span>January credit sales = 10,000</div></div>
</div>
</section>

<section class="s" data-nav="3&ndash;4 · AJE and ADA">
<p class="eyebrow">January &middot; Steps 3 and 4</p>
<h2>Month-end adjustment</h2>
<div class="two">
<div><p class="big">BDE = 10,000 &times; 2% = <span class="hl">200</span></p>
{je([("Jan 31", "BDE (+E)", "ADA (+xA, &minus;A)", "200")])}</div>
<div>{tacct("ADA", [], [("Jan 31 AJE", "200")], "200", "cr")}</div>
</div>
<div class="note" style="margin-top:20px">The AJE does not touch A/R. It records the expense and builds up ADA.</div>
</section>

<section class="s" data-nav="5 · January summary">
<p class="eyebrow">January &middot; Step 5</p>
<h2>Summary: January 31</h2>
{summary("Jan 31", "10,000", "200", "9,800")}
<div class="key"><span class="klab">Net A/R</span>Sneaker Supply expects to collect 9,800 of the 10,000 customers owe.</div>
</section>

<section class="s" data-nav="February timeline">
<p class="eyebrow">February</p>
<h2>What happened in February</h2>
{FEB_TL}
<div class="note" style="margin-top:20px">Feb 20: Store A went out of business. 1% of January&rsquo;s credit sales (10,000 &times; 1% = <b>100</b>) is written off.</div>
</section>

<section class="s" data-nav="6&ndash;7 · Entries and A/R">
<p class="eyebrow">February &middot; Steps 6 and 7</p>
<h2>Journal entries and the A/R T-account</h2>
<div class="two">
<div>{je([("Feb 8", "Cash (+A)", "Sales Rev (+R)", "3,000"),
            ("Feb 15", "A/R (+A)", "Sales Rev (+R)", "8,000"),
            ("Feb 20", "ADA (&minus;xA, +A)", "A/R (&minus;A)", "100")])}</div>
<div>{tacct("A/R", [("Beg. bal.", "10,000"), ("Feb 15", "8,000")], [("Feb 20", "100")], "17,900", "dr")}
<div class="key" style="margin-top:22px"><span class="klab">Read it from the T-account</span>February credit sales = 8,000</div></div>
</div>
<div class="note">The write-off uses up part of ADA. <b>No expense</b> is recorded: it was already recorded as BDE in January.</div>
</section>

<section class="s" data-nav="8&ndash;9 · AJE and ADA">
<p class="eyebrow">February &middot; Steps 8 and 9</p>
<h2>Month-end adjustment</h2>
<div class="two">
<div><p class="big">BDE = 8,000 &times; 2% = <span class="hl">160</span></p>
{je([("Feb 28", "BDE (+E)", "ADA (+xA, &minus;A)", "160")])}</div>
<div>{tacct("ADA", [("Feb 20", "100")], [("Beg. bal.", "200"), ("Feb 28 AJE", "160")], "260", "cr")}</div>
</div>
<div class="note" style="margin-top:20px">Ending ADA = Beginning ADA + BDE &minus; Write-offs = 200 + 160 &minus; 100 = 260</div>
</section>

<section class="s" data-nav="10 · February summary">
<p class="eyebrow">February &middot; Step 10</p>
<h2>Summary: February 28</h2>
{summary("Feb 28", "17,900", "260", "17,640")}
<div class="key"><span class="klab">Net A/R</span>Sneaker Supply expects to collect 17,640 of the 17,900 customers owe.</div>
</section>

<section class="s" data-nav="Takeaways">
<p class="eyebrow">Takeaways</p>
<h2>What to remember</h2>
<ol class="steps">
<li><b>BDE</b> = this month&rsquo;s <b>credit</b> sales &times; 2%. Cash sales are not included.</li>
<li><b>BDE</b> is an expense for the month. <b>ADA</b> is the balance of A/R expected to go uncollected.</li>
<li>A <b>write-off</b> lowers gross A/R and ADA by the same amount: no expense, and net A/R does not change.</li>
<li>Net A/R = Gross A/R &minus; ADA = the amount expected to be collected.</li>
</ol>
</section>
'''

css = '''
.je { font-size:26px; }
.je td.cr { padding-left:70px; }
table.tacct { border-collapse:collapse; font-size:27px; width:620px; background:var(--card); }
table.tacct th { text-align:center; padding:6px; border-bottom:4px solid var(--ink); font:700 28px Charter,Georgia,serif; }
table.tacct td { padding:12px 14px 6px; }
table.tacct td.l { color:var(--muted); width:150px; white-space:nowrap; }
table.tacct td.a { text-align:right; width:150px; }
table.tacct td.dr { border-right:4px solid var(--ink); }
table.tacct td.cl { padding-left:22px; }
table.tacct tr.bal td { border-top:2px solid var(--ink); font-weight:700; color:var(--ink); }
table.ar3 { border-collapse:collapse; font-size:30px; background:var(--card); }
table.ar3 th { background:#ffe14d; padding:10px 24px; text-align:right; font:700 22px "Segoe UI",sans-serif; }
table.ar3 th:first-child, table.ar3 td:first-child { text-align:left; }
table.ar3 th.m, table.ar3 td.m { text-align:left; padding-left:40px; }
table.ar3 td { padding:16px 24px 8px; }
table.ar3 td.a { text-align:right; width:200px; }
table.ar3 td.m { font-style:italic; color:var(--muted); }
table.ar3 tr.tot td { border-top:2px solid var(--ink); font-weight:700; }
table.ar3 tr.tot td.m { font-weight:400; }
'''

html = head.replace('<title>Anthropic S-1 Accounting</title>', '<title>Ch8 Practice Review</title>')
html = html.replace('</style>', css + '</style>', 1) + '\n' + body + '\n' + tail
open(os.path.join(OUT, 'Ch8-Practice-Slides.html'), 'w').write(html)
print('wrote Ch8-Practice-Slides')
