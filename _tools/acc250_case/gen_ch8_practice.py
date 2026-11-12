#!/usr/bin/env python3
"""Ch8 practice worksheet: percent-of-credit-sales method over January and February.

Usage: python _tools/acc250_case/gen_ch8_practice.py assets/ACC250
Writes Ch8-Practice-Worksheet.html (front: January, back: February).
"""
import os, sys

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'case.css')).read() + '''
.intro2 { margin:0 0 6pt; font-size:10pt; }
.given { border:.8pt solid #000; border-radius:3pt; padding:5pt 9pt; margin:4pt 0 8pt; font-size:10pt; }
.given b.t { display:block; font:700 8.6pt Arial,sans-serif; letter-spacing:.01em; margin-bottom:3pt; }
.given ul { margin:0; padding-left:16pt; }
.given li { margin:2pt 0; }
table.je3 { width:100%; border-collapse:collapse; font-size:10pt; margin:2pt 0 4pt; }
table.je3 th { font:700 7.8pt Arial,sans-serif; letter-spacing:.01em; color:#444;
  text-align:left; padding:2pt 6pt; border-bottom:.8pt solid #000; }
table.je3 th.r { text-align:right; }
table.je3 td { padding:7pt 6pt 1pt; vertical-align:bottom; }
table.je3 td.d { width:.6in; font-weight:700; }
table.je3 td.amt { width:.95in; }
table.je3 tr.first td { border-top:.6pt solid #ccc; }
table.je3 .cr .bl { margin-left:22pt; }
table.je3 .bl { border-bottom:0; min-height:14pt; }
table.ar { border-collapse:collapse; font-size:10.5pt; margin:4pt 0; min-width:4.6in; }
table.ar th { font:700 8.4pt Arial,sans-serif; text-align:right; padding:3pt 10pt; background:#ffe14d;
  -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.ar th:first-child, table.ar td:first-child { text-align:left; }
table.ar td { padding:6pt 10pt 2pt; vertical-align:bottom; }
table.ar td.amt { width:1.2in; }
table.ar tr.tot td { border-top:.8pt solid #000; font-weight:700; }
.inl { display:inline-block; min-width:.9in; vertical-align:bottom; }
.pick i { font-style:normal; padding:0 3pt; }
html.key .pick i.r { border:1.2pt solid var(--key); border-radius:7pt; color:var(--key); font-weight:700; }
.why { display:none; color:var(--key); font-size:9.3pt; margin-top:2pt; }
html.key .why { display:block; }
.qblock { font-size:10pt; margin:8pt 0 0; display:grid; grid-template-columns:16pt 1fr; gap:4pt; }
.qblock p { margin:0 0 3pt; }
.fn { margin:8pt 0 0; font-size:8.8pt; color:#333; }
.pgfn { position:absolute; left:.5in; right:.5in; bottom:.32in; font-size:9.2pt; color:#000; border-top:.6pt solid #000; padding-top:3pt; }
.pgfn sup, h2 sup { font-size:.75em; }
.pair { display:grid; grid-template-columns:3.7in 3.4in; gap:.35in; align-items:start; margin-top:6pt; }
.pair h2 { margin-top:2pt; }
.pair table.je3 { width:100%; }
table.je3 td.amt { width:.62in; }
table.je3 td.d { width:.55in; white-space:nowrap; }
table.tacct td.lab { white-space:nowrap; }
.tq .inl { min-width:.75in; }
.pair table.tacct { width:3.3in; }
table.tacct td.lab { width:.75in; } table.tacct td.amt { width:.72in; }
.tq { margin-top:6pt; line-height:2; }
.hint { font-size:9pt; color:#000; margin:2pt 0 0; }
.pair table.net3 { width:3.2in; }
.net3cap { margin-top:8pt !important; }
.tq2 { font-size:10pt; margin:2pt 0 6pt; }
table.ar3 { border-collapse:collapse; font-size:10.5pt; }
table.ar3 th { font:700 8.8pt Arial,sans-serif; text-align:right; padding:3pt 10pt; background:#ffe14d; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.ar3 th:first-child, table.ar3 td:first-child { text-align:left; }
table.ar3 th.mean, table.ar3 td.mean { text-align:left; padding-left:18pt; }
table.ar3 td { padding:6pt 10pt 2pt; vertical-align:bottom; }
table.ar3 td.amt { width:1in; }
table.ar3 td.mean { font-style:italic; color:#000; }
table.ar3 tr.tot td { border-top:.8pt solid #000; font-weight:700; }
table.ar3 tr.tot td.mean { font-weight:400; }
/* spacing: spread the free space through the page */
.pair { margin-top:13pt !important; }
table.je3 td { padding:7pt 6pt 2pt !important; }
table.tacct td { padding:8pt 6pt 2pt !important; }
.tq2 { margin:4pt 0 8pt !important; }
table.ar3 td { padding:7pt 10pt 2pt !important; }
.sumh { margin-top:16pt !important; }
svg.tl { margin-bottom:6pt !important; }
svg.tl { display:block; width:100%; height:auto; margin:0 0 4pt; font-family:Arial,Helvetica,sans-serif; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.sum { border-collapse:collapse; font-size:10.5pt; margin:4pt 0; min-width:5.4in; }
table.sum th { font:700 8.8pt Arial,sans-serif; text-align:right; padding:3pt 10pt; background:#ffe14d; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.sum th:first-child, table.sum td:first-child { text-align:left; }
table.sum td { padding:6pt 10pt 2pt; vertical-align:bottom; }
table.sum td.amt { width:1.2in; }
table.sum tr.tot td { border-top:.8pt solid #000; font-weight:700; }
table.sum tr.sep td { border-bottom:.8pt solid #999; }
.tw { display:grid; grid-template-columns:3.9in 1fr; gap:.3in; align-items:center; margin:4pt 0 2pt; }
table.tacct { border-collapse:collapse; font-size:10pt; width:3.9in; }
table.tacct th { font:700 10pt "Times New Roman",serif; text-align:center; padding:2pt; border-bottom:1.6pt solid #000; }
table.tacct td { padding:5pt 6pt 1pt; vertical-align:bottom; }
table.tacct td.lab { width:.85in; color:#333; }
table.tacct td.amt { width:1in; }
table.tacct td.dr { border-right:1.6pt solid #000; }
table.tacct td.cl { padding-left:10pt; }
table.tacct tr.bal td { border-top:.8pt solid #000; font-weight:700; }
table.net3 { border-collapse:collapse; font-size:10.5pt; width:100%; }
table.net3 th { font:700 8.8pt Arial,sans-serif; text-align:right; padding:3pt 8pt; background:#ffe14d; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.net3 td { padding:8pt 8pt 2pt; text-align:right; }
.net3cap { font:700 9pt Arial,sans-serif; margin:0 0 3pt; }
.tq { font-size:10pt; }
table.je3 td { padding:5pt 6pt 1pt; }
'''


def bl(a, cls='amt'):
    return f'<span class="bl {cls}" data-a="{a}"></span>'


def inl(a):
    return f'<span class="bl inl amt" data-a="{a}"></span>'


def je(entries):
    """entries: list of (date, debit_acct, credit_acct, amount)."""
    rows = ['<table class="je3"><tr><th>Date</th><th>Account</th><th class="r">Debit</th><th class="r">Credit</th></tr>']
    for d, dr, cr, amt in entries:
        rows.append(f'<tr class="first"><td class="d">{d}</td><td>{bl(dr, "nm")}</td><td class="amt">{bl(amt)}</td><td class="amt"></td></tr>')
        rows.append(f'<tr class="cr"><td></td><td>{bl(cr, "nm")}</td><td class="amt"></td><td class="amt">{bl(amt)}</td></tr>')
    rows.append('</table>')
    return ''.join(rows)


def tacct(title, debits, credits, bal_label, bal, side):
    """side: 'dr' or 'cr' for where the ending balance sits."""
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


def net_table(gross, ada, net):
    return f'''<table class="net3">
<tr><th>Gross A/R</th><th>Less: ADA</th><th>Net A/R</th></tr>
<tr><td>{bl(gross)}</td><td>{bl(ada)}</td><td>{bl(net)}</td></tr>
</table>'''


def summary(month, date, sales, bde, gross, ada, net):
    return f'''<div class="sumrow">
<p class="tq2">{month} credit sales = {inl(sales)}</p>
<p class="tq2">BDE = credit sales &times; 2% = {inl(bde)}</p>
<table class="ar3">
<tr><th></th><th>{date}</th><th class="mean">What it means</th></tr>
<tr><td>Gross A/R</td><td class="amt">{bl(gross)}</td><td class="mean">Total A/R</td></tr>
<tr><td>Less: ADA</td><td class="amt">{bl(ada)}</td><td class="mean">Noncollectible A/R (estimated)</td></tr>
<tr class="tot"><td>Net A/R</td><td class="amt">{bl(net)}</td><td class="mean">Collectible portion of A/R</td></tr>
</table>
</div>'''


def taccount(debits, credits, bal):
    """debits/credits: lists of (label, amount). Amounts are blanks for students."""
    n = max(len(debits), len(credits))
    rows = ['<table class="tacct"><tr><th colspan="4">A/R</th></tr>']
    for i in range(n):
        dl, da = debits[i] if i < len(debits) else ('', None)
        cl, ca = credits[i] if i < len(credits) else ('', None)
        rows.append(f'<tr><td class="lab">{dl}</td><td class="amt dr">{bl(da) if da else ""}</td>'
                    f'<td class="lab cl">{cl}</td><td class="amt">{bl(ca) if ca else ""}</td></tr>')
    rows.append(f'<tr class="bal"><td class="lab">End. bal.</td><td class="amt dr">{bl(bal)}</td><td class="lab cl"></td><td class="amt"></td></tr>')
    rows.append('</table>')
    return ''.join(rows)


COLORS = {'start': '#5c6863', 'cash': '#5b7f95', 'credit': '#1a7a5e', 'writeoff': '#b3200f', 'aje': '#8a6d1f'}


def timeline(ndays, events):
    """events: (day, date label, line 1, line 2, kind). Inline SVG, prints in color or gray."""
    W, x0, x1, y = 740, 70, 670, 40
    def X(d): return x0 + (d - 1) / (ndays - 1) * (x1 - x0)
    out = [f'<svg class="tl" viewBox="0 0 {W} 92" role="img" aria-label="Timeline">',
           f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#16263a" stroke-width="2.5"/>',
           f'<polygon points="{x1},{y-5} {x1+10},{y} {x1},{y+5}" fill="#16263a"/>']
    for d, lab, l1, l2, k in events:
        c = COLORS[k]; x = X(d)
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="7" fill="{c}" stroke="#fff" stroke-width="2"/>')
        out.append(f'<text x="{x:.1f}" y="{y-16}" text-anchor="middle" font-weight="700" font-size="13" fill="#16263a">{lab}</text>')
        out.append(f'<text x="{x:.1f}" y="{y+26}" text-anchor="middle" font-size="12" font-weight="700" fill="{c}">{l1}</text>')
        if l2:
            out.append(f'<text x="{x:.1f}" y="{y+42}" text-anchor="middle" font-size="12" fill="#333">{l2}</text>')
    out.append('</svg>')
    return ''.join(out)


def ar_table(date, gross, ada, net):
    return f'''<table class="ar">
<tr><th>Accounts receivable, {date}</th><th>Amount</th></tr>
<tr><td>Gross A/R</td><td class="amt">{bl(gross)}</td></tr>
<tr><td>Less: ADA</td><td class="amt">{bl(ada)}</td></tr>
<tr class="tot"><td>Net A/R</td><td class="amt">{bl(net)}</td></tr>
</table>'''


def pick(opts, right):
    return '<span class="pick">' + ' / '.join(f'<i{" class=\"r\"" if o == right else ""}>{o}</i>' for o in opts) + '</span>'


front = f'''<h1>Bad Debts Step by Step: % of Credit Sales Method</h1>
<p class="intro2"><b>Sneaker Supply Co.</b> (a made-up company) sells shoes to stores. It started business on <b>January 1</b>, so A/R and ADA begin at $0.
Based on experience, it expects <b>2% of each month&rsquo;s credit sales</b> to be uncollectible, and it records BDE at the end of each month.</p>

<div class="given"><b class="t">January transactions</b>
<ul>
<li><b>Jan 5:</b> Sold shoes for <b>$4,000 cash</b>.</li>
<li><b>Jan 10:</b> Sold shoes to Store A <b>on credit, $6,000</b>.</li>
<li><b>Jan 20:</b> Sold shoes to Store B <b>on credit, $4,000</b>.</li>
<li><b>Jan 31:</b> Record bad debt expense: 2% of January&rsquo;s credit sales.</li>
</ul></div>
{timeline(31, [(1, "Jan 1", "Start", "A/R = ADA = $0", "start"),
               (5, "Jan 5", "Cash sale", "$4,000", "cash"),
               (10, "Jan 10", "Credit sale", "$6,000", "credit"),
               (20, "Jan 20", "Credit sale", "$4,000", "credit"),
               (31, "Jan 31", "AJE: BDE", "2% of credit sales", "aje")])}

<div class="pair">
<div>
<h2>1. Journal entries<sup>*</sup></h2>
{je([("Jan 5", "Cash (+A)", "Sales Rev (+R)", "4,000"),
     ("Jan 10", "A/R (+A)", "Sales Rev (+R)", "6,000"),
     ("Jan 20", "A/R (+A)", "Sales Rev (+R)", "4,000")])}
<p class="hint">Use (+A), (&minus;A), (+R), (+E), (+xA), (&minus;xA).</p>
</div>
<div>
<h2>2. T-account for A/R</h2>
{taccount([("Jan 10", "6,000"), ("Jan 20", "4,000")], [], "10,000")}
</div>
</div>

<div class="pair">
<div>
<h2>3. Adjusting journal entry (AJE)</h2>
{je([("Jan 31", "BDE (+E)", "ADA (+xA, &minus;A)", "200")])}
<div class="why">The cash sale has no collection risk, so it is not in A/R and not in the 2% estimate.</div>
</div>
<div>
<h2>4. T-account for ADA</h2>
{tacct("ADA", [], [("Jan 31 AJE", "200")], "End. bal.", "200", "cr")}
</div>
</div>

<h2 class="sumh">5. Summary: January</h2>
{summary("January", "Jan 31", "10,000", "200", "10,000", "200", "9,800")}
<div class="pgfn"><sup>*</sup> Cost of goods sold entries (Dr CGS, Cr Inventory) are omitted for brevity. See Ch6.</div>
'''

back = f'''<h1 style="margin-top:0">February</h1>
<div class="given"><b class="t">February transactions</b>
<ul>
<li><b>Feb 8:</b> Sold shoes for <b>$3,000 cash</b>.</li>
<li><b>Feb 15:</b> Sold shoes to Store C <b>on credit, $8,000</b>.</li>
<li><b>Feb 20:</b> Store A went out of business. An amount equal to <b>1% of January&rsquo;s credit sales</b> is now deemed uncollectible and is written off.</li>
<li><b>Feb 28:</b> Record bad debt expense: 2% of February&rsquo;s credit sales.</li>
</ul></div>
{timeline(28, [(1, "Feb 1", "Start", "Jan 31 balances", "start"),
               (8, "Feb 8", "Cash sale", "$3,000", "cash"),
               (15, "Feb 15", "Credit sale", "$8,000", "credit"),
               (20, "Feb 20", "Write-off", "1% of Jan credit sales", "writeoff"),
               (28, "Feb 28", "AJE: BDE", "2% of credit sales", "aje")])}

<div class="pair">
<div>
<h2>6. Journal entries<sup>*</sup></h2>
{je([("Feb 8", "Cash (+A)", "Sales Rev (+R)", "3,000"),
     ("Feb 15", "A/R (+A)", "Sales Rev (+R)", "8,000"),
     ("Feb 20", "ADA (&minus;xA, +A)", "A/R (&minus;A)", "100")])}
<div class="why">Feb 20: 10,000 &times; 1% = 100 is written off against ADA. No expense is recorded.</div>
</div>
<div>
<h2>7. T-account for A/R</h2>
{taccount([("Beg. bal.", "10,000"), ("Feb 15", "8,000")], [("Feb 20", "100")], "17,900")}
</div>
</div>

<div class="pair">
<div>
<h2>8. Adjusting journal entry (AJE)</h2>
{je([("Feb 28", "BDE (+E)", "ADA (+xA, &minus;A)", "160")])}
</div>
<div>
<h2>9. T-account for ADA</h2>
{tacct("ADA", [("Feb 20", "100")], [("Beg. bal.", "200"), ("Feb 28 AJE", "160")], "End. bal.", "260", "cr")}
</div>
</div>

<h2 class="sumh">10. Summary: February</h2>
{summary("February", "Feb 28", "8,000", "160", "17,900", "260", "17,640")}
<div class="pgfn"><sup>*</sup> Cost of goods sold entries (Dr CGS, Cr Inventory) are omitted for brevity. See Ch6.</div>
'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ch8 Practice Worksheet</title>
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
  <div class="course">ACC 250 &middot; Ch8 Worksheet<span class="keytag"> &middot; Answer key</span></div>
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
open(os.path.join(OUT, 'Ch8-Practice-Worksheet.html'), 'w').write(html)
print('wrote Ch8-Practice-Worksheet')
