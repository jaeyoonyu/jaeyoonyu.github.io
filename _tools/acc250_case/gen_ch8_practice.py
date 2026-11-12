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

<h2>1. Journal entries for January <small>Use (+A), (&minus;A), (+R), (+E), (+xA), (&minus;xA).</small></h2>
{je([("Jan 5", "Cash (+A)", "Sales Rev (+R)", "4,000"),
     ("Jan 10", "A/R (+A)", "Sales Rev (+R)", "6,000"),
     ("Jan 20", "A/R (+A)", "Sales Rev (+R)", "4,000"),
     ("Jan 31", "BDE (+E)", "ADA (+xA, &minus;A)", "200")])}
<div class="why">Jan 31: January credit sales = 6,000 + 4,000 = 10,000; BDE = 10,000 &times; 2% = 200. The cash sale has no collection risk, so it is not included.</div>

<h2 style="margin-top:10pt">2. Accounts receivable at the end of January</h2>
{ar_table("Jan 31", "10,000", "200", "9,800")}
<p class="fn">Cost of goods sold entries are omitted for brevity (see Ch6).</p>
'''

back = f'''<h1 style="margin-top:0">February</h1>
<div class="given"><b class="t">February transactions</b>
<ul>
<li><b>Feb 8:</b> Sold shoes for <b>$3,000 cash</b>.</li>
<li><b>Feb 15:</b> Sold shoes to Store C <b>on credit, $5,000</b>.</li>
<li><b>Feb 20:</b> Store A went out of business. An amount equal to <b>1% of January&rsquo;s credit sales</b> is now deemed uncollectible and is written off.</li>
<li><b>Feb 28:</b> Record bad debt expense: 2% of February&rsquo;s credit sales.</li>
</ul></div>

<h2>3. Journal entries for February</h2>
{je([("Feb 8", "Cash (+A)", "Sales Rev (+R)", "3,000"),
     ("Feb 15", "A/R (+A)", "Sales Rev (+R)", "5,000"),
     ("Feb 20", "ADA (&minus;xA, +A)", "A/R (&minus;A)", "100"),
     ("Feb 28", "BDE (+E)", "ADA (+xA, &minus;A)", "100")])}
<div class="why">Feb 20: 10,000 &times; 1% = 100 written off against ADA (no expense). Feb 28: 5,000 &times; 2% = 100.</div>

<h2 style="margin-top:10pt">4. Accounts receivable at the end of February</h2>
{ar_table("Feb 28", "14,900", "200", "14,700")}
<div class="why">Gross A/R = 10,000 + 5,000 &minus; 100 = 14,900. ADA = 200 &minus; 100 + 100 = 200. Net A/R = 14,900 &minus; 200 = 14,700.</div>

<h2 style="margin-top:10pt">5. Put it together</h2>
<div class="qblock"><span class="no">a</span><div>
<p>BDE for January = {inl("200")} &nbsp;&nbsp; BDE for February = {inl("100")}</p></div></div>
<div class="qblock"><span class="no">b</span><div>
<p>ADA equation for February: Beginning ADA {inl("200")} + BDE {inl("100")} &minus; Write-off {inl("100")} = Ending ADA {inl("200")}</p></div></div>
<div class="qblock"><span class="no">c</span><div>
<p>Did the Feb 20 write-off change BDE? {pick(["yes", "no"], "no")} &nbsp;&nbsp; Did it change net A/R? {pick(["yes", "no"], "no")}</p>
<div class="why">The loss was already recorded as BDE in January (matching principle). The write-off lowers gross A/R and ADA by the same 100, so net A/R stays the same.</div></div></div>
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
