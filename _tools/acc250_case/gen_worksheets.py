#!/usr/bin/env python3
"""Generate the Ch8 bad-debt (Crocs) and IPO (Anthropic S-1) worksheets.

Usage: python _tools/acc250_case/gen_worksheets.py assets/ACC250
Uses case.css (same look as the Walmart/Costco cases) plus a few extra rules.
"""
import os, sys

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'case.css')).read() + '''
.box { border:.8pt solid #000; border-radius:3pt; padding:4pt 8pt; margin:6pt 0; font-size:9.6pt; }
.box b.t { display:block; font:700 8.6pt Arial,sans-serif; letter-spacing:.06em; text-transform:uppercase; margin-bottom:2pt; }
ol.qs.full li { grid-template-columns:16pt 1fr 1in; }
.qblock { font-size:9.8pt; margin:9pt 0 0; display:grid; grid-template-columns:16pt 1fr; gap:4pt; }
.qblock p { margin:0 0 3pt; }
.je2 { border-collapse:collapse; margin:3pt 0 2pt; font-size:9.6pt; }
.je2 th { font:700 7.8pt Arial,sans-serif; letter-spacing:.06em; text-transform:uppercase; color:#444; text-align:left; padding:1pt 6pt; }
.je2 td { padding:3pt 6pt 1pt; vertical-align:bottom; }
.je2 .acct { width:2.6in; } .je2 .amt { width:.8in; }
.je2 .cr .bl { margin-left:18pt; }
.pick i { font-style:normal; padding:0 3pt; }
html.key .pick i.r { border:1.2pt solid var(--key); border-radius:7pt; color:var(--key); font-weight:700; }
.lines { border-bottom:.8pt solid #999; height:16pt; }
html.key .lines { display:none; }
.why { display:none; color:var(--key); font-size:9.2pt; margin-top:2pt; }
html.key .why { display:block; }
table.terms { width:100%; border-collapse:collapse; font-size:9.4pt; margin:2pt 0 4pt; }
table.terms th { font:700 8.4pt Arial,sans-serif; text-align:left; padding:2.2pt 6pt; background:#ffe14d; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
table.terms td { padding:2.2pt 6pt; border-bottom:.6pt solid #ccc; vertical-align:top; width:42%; }
table.terms td:first-child { width:16%; font-weight:700; color:#444; font-size:8.8pt; }
.terms2 { font-size:9.4pt; margin:0 0 6pt; }
.terms2 p { margin:1.5pt 0; }
.inl { display:inline-block; min-width:.8in; vertical-align:bottom; }
table.mini { border-collapse:collapse; font-size:9.6pt; margin:3pt 0; }
table.mini th { font:700 7.8pt Arial,sans-serif; letter-spacing:.06em; text-transform:uppercase; color:#444; padding:1pt 8pt; text-align:right; border-bottom:.8pt solid #000; }
table.mini th:first-child, table.mini td:first-child { text-align:left; }
table.mini td { padding:2pt 8pt; text-align:right; }
table.mini tr.tot td { border-top:.8pt solid #000; font-weight:700; }
'''

def stmt(co, title, colhead, rows):
    out = [f'<div class="stmt"><p class="co">{co}</p><p class="ttl">{title}</p><table>',
           f'<tr><th></th><th>{colhead}</th></tr>']
    for lab, amt, fl in rows:
        f = fl.split()
        if 'sec' in f:
            out.append(f'<tr class="sec"><td>{lab}</td><td></td></tr>'); continue
        cls = ' '.join(c for c in ('u', 'uu', 'hd') if c in f)
        lcls = ' class="i1"' if 'i' in f else ''
        d = '<i>$</i>' if '$' in f else ''
        style = ' style="background:#fff7cc"' if 'hl' in f else ''
        out.append(f'<tr class="{cls}"{style}><td{lcls}>{lab}</td><td class="n">{d}{amt}</td></tr>')
    out.append('</table></div>')
    return '\n'.join(out)

def bl(a, cls='amt'):
    return f'<span class="bl {cls}" data-a="{a}"></span>'

def inl(a):
    return f'<span class="bl inl amt" data-a="{a}"></span>'

def qlist(items, start, full=False):
    rows = ''.join(f'<li><span class="no">{n}</span><span class="qt">{q}</span>{bl(a)}</li>'
                   for n, (q, a) in enumerate(items, start))
    return f'<ol class="qs{" full" if full else ""}">{rows}</ol>'

def page(title, s, header, front, back, note):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
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
  <div class="course">{header}<span class="keytag"> &middot; Answer key</span></div>
  <div class="name">Name <span></span></div>
</header>
{front}
{'' if back else f'<p class="src">{note}</p>'}
</div>
{f'<div class="page">{back}<p class="src">{note}</p></div>' if back else ''}
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

def je(rows):
    """rows: list of (debit_account, credit_account, amount) -> blank JE table."""
    out = ['<table class="je2"><tr><th>Account</th><th>Debit</th><th>Credit</th></tr>']
    dr, cr, amt = rows
    out.append(f'<tr><td class="acct">{bl(dr, "nm")}</td><td class="amt">{bl(amt)}</td><td class="amt"></td></tr>')
    out.append(f'<tr class="cr"><td class="acct">{bl(cr, "nm")}</td><td class="amt"></td><td class="amt">{bl(amt)}</td></tr>')
    out.append('</table>')
    return ''.join(out)

def pick(opts, right):
    return '<span class="pick">' + ' / '.join(f'<i{" class=\"r\"" if o == right else ""}>{o}</i>' for o in opts) + '</span>'

# ======================================================================
# Ch8: Crocs bad debts
# ======================================================================
CROX_URL = 'https://www.sec.gov/Archives/edgar/data/1334036/000133403625000009/crox-20241231.htm'
BS = [('Cash and cash equivalents', '180,485', '$'),
      ('Accounts receivable (gross)', '289,236', 'hl'),
      ('Less: Allowance for doubtful accounts (ADA)', '(31,579)', 'u hl'),
      ('Accounts receivable, net', '257,657', 'i hl'),
      ('Inventories', '356,254', ''),
      ('Other current assets', '77,873', 'u'),
      ('Total current assets', '872,269', 'i'),
      ('Property, goodwill, brands and other', '3,939,884', 'u'),
      ('Total assets', '4,812,153', 'i uu $'),
      ('Total current liabilities', '740,208', 'hd $'),
      ('Long-term liabilities', '2,236,213', 'u'),
      ('Total liabilities', '2,976,421', 'i'),
      ('Total stockholders&rsquo; equity', '1,835,732', 'u'),
      ('Total liabilities and equity', '4,812,153', 'i uu $')]
ALLOW = [('Balance, Dec 31, 2023', '27,591', '$'),
         ('Add: Bad debt expense (new estimates)', '?', ''),
         ('Less: Accounts written off', '?', 'u'),
         ('Balance, Dec 31, 2024', '31,579', 'i uu $')]

front = f'''<h1>Crocs: Bad Debts in a Real Balance Sheet</h1>
<p class="filing"><b>Source:</b> Crocs, Inc. Form 10-K, year ended December 31, 2024 (condensed; amounts in thousands) &middot;
<a href="{CROX_URL}" target="_blank">{CROX_URL.replace("https://www.", "")}</a></p>
<div class="cols">
{stmt('Crocs, Inc.', 'Consolidated Balance Sheet', 'Dec 31, 2024', BS)}
<div>
{stmt('Crocs, Inc.', 'Allowance for Doubtful Accounts (ADA)', '2024', ALLOW)}
<div class="box"><b class="t">Background</b>Crocs sells many of its shoes to retailers and distributors (shoe stores, department stores) on credit. They pay weeks later.</div>
<div class="box"><b class="t">More terms</b>
<b>Gross A/R:</b> the total amount customers owe for goods sold on credit.<br>
<b>Net A/R:</b> gross A/R &minus; ADA, the amount the company expects to collect.<br>
<b>Write-off:</b> removing a specific customer&rsquo;s account once it is known to be uncollectible.</div>
</div>
</div>
<h2>Accounts &amp; Terms</h2>
<table class="terms">
<tr><th></th><th>Allowance for Doubtful Accounts (ADA)</th><th>Bad Debt Expense (BDE)</th></tr>
<tr><td>Where it appears</td><td><b>Balance sheet</b></td><td><b>Income statement</b></td></tr>
<tr><td>Type of account</td><td>Contra-asset: subtracted from accounts receivable</td><td>Operating expense</td></tr>
<tr><td>What it measures</td><td>The <b>total</b> amount of receivables still expected to go uncollected</td><td><b>This period&rsquo;s</b> estimate of new uncollectible amounts (how much ADA is increased)</td></tr>
<tr><td>Time</td><td>A balance at <b>one date</b> (Dec 31)</td><td>An amount for a <b>whole period</b> (the year)</td></tr>
<tr><td>Example</td><td>Last estimate: <b>$1,000</b> will not be collected.<br>New estimate: <b>$3,000</b> will not be collected.</td><td>ADA must go up by $3,000 &minus; $1,000, so record <b>BDE of $2,000</b>. BDE is the amount that brings ADA up to the new estimate.</td></tr>
<tr><td>At Crocs</td><td>31,579 on the balance sheet</td><td>Not shown as a separate line: included in SG&amp;A expenses</td></tr>
</table>
<h2>Find it in the statements <small>Write the amount ($ thousands, %, or $).</small></h2>
{qlist([("In total, how much did customers owe Crocs at year-end?", "289,236"),
        ("How much does Crocs estimate it will never collect?", "31,579"),
        ("How much does Crocs actually expect to collect in cash?", "257,657"),
        ("What percentage of what customers owe does Crocs expect never to collect?", "10.9%"),
        ("Out of every $100 customers owe, about how much does Crocs expect to collect?", "$89"),
        ("By how much did the allowance increase during 2024?", "3,988"),
        ("Sneaker Supply Co. (made up) had an ADA of $2,500. At year-end it now expects $4,000 of its receivables will not be collected (no accounts were written off). How much BDE must it record?", "1,500")], 1, full=True)}
'''

back = f'''<h2 style="margin-top:2pt">Hints</h2>
<div class="defs" style="font-size:9.3pt">
<dl>
<dt>Gross and net A/R</dt><dd>Gross A/R: what customers owe for credit sales. Net A/R = Gross A/R &minus; ADA, the amount expected to be collected.</dd>
<dt>Allowance for doubtful accounts (ADA)</dt><dd>The estimated amount of uncollectible A/R. A contra-asset (credit balance).</dd>
<dt>Allowance method (GAAP)</dt><dd>Estimate and record BDE at the end of each period, in the same period as the credit sales (matching principle).</dd>
</dl>
<dl>
<dt>Bad debt expense (BDE)</dt><dd>Adjusting entry: Dr BDE, Cr ADA. % of credit sales method: BDE = credit sales &times; historical % uncollectible.</dd>
<dt>Write-off</dt><dd>Dr ADA, Cr A/R. No expense; net A/R does not change.</dd>
<dt>ADA equation</dt><dd>Ending ADA = Beginning ADA + BDE &minus; Write-offs.</dd>
</dl>
</div>

<h2 style="margin-top:10pt">Practice</h2>
<div class="qblock"><span class="no">7</span><div>
<p><b>Fill in the &ldquo;?&rdquo;.</b> Suppose Crocs wrote off <b>6,000</b> of customer accounts during 2024. How much bad debt expense did it record? {inl("9,988")}</p>
<div class="why">27,591 + Expense &minus; 6,000 = 31,579, so Expense = 9,988.</div></div></div>

<div class="qblock"><span class="no">8</span><div>
<p><b>Journal entries.</b> (a) Record the year-end bad debt estimate from Q7.</p>
{je(("Bad debt expense", "Allowance for doubtful accounts", "9,988"))}
<p>(b) A shoe store that owes Crocs <b>1,500</b> goes bankrupt. Write off its account.</p>
{je(("Allowance for doubtful accounts", "Accounts receivable", "1,500"))}
<p>Effect of entry (b): net income {pick(["decreases", "no change"], "no change")}; &nbsp; accounts receivable, net {pick(["decreases", "no change"], "no change")}</p>
</div></div>

<div class="qblock"><span class="no">9</span><div>
<p><b>% of credit sales method.</b> Shoe Wholesale Co. (a smaller, made-up company) made <b>$400,000</b> of credit sales in December. In the past, <b>2%</b> of credit sales have not been collected.</p>
<p>(a) Bad debt expense for December = {inl("8,000")}</p>
<p>(b) ADA was 3,000 on Dec 1, and 2,500 of accounts were written off during December. ADA on Dec 31 = {inl("8,500")}</p>
<div class="why">(a) 400,000 &times; 2% = 8,000. &nbsp;(b) 3,000 + 8,000 &minus; 2,500 = 8,500.</div>
</div></div>

<div class="qblock"><span class="no">10</span><div>
<p><b>Direct write-off method.</b> Under the direct write-off method, when would Crocs record the expense for the shoe store in Q8(b)? {pick(["when the sale is made", "when the account is written off"], "when the account is written off")}<br>
Why is this method not allowed under GAAP?</p>
<div class="lines"></div>
<div class="why">The expense would be recorded in a later period than the sale, which violates the matching principle (it is used for tax purposes).</div>
</div></div>

<div class="qblock"><span class="no">11</span><div>
<p><b>Compare.</b> Costco says its allowance for receivables is <i>immaterial</i>. Why would Costco have almost no bad debts while Crocs does?</p>
<div class="lines"></div>
<div class="why">Costco&rsquo;s members pay at the register (cash, debit or credit card), so the card company, not Costco, bears the risk of non-payment. Crocs sells to other businesses on credit.</div>
</div></div>
'''
note = ('Crocs&rsquo;s reported &ldquo;allowances&rdquo; ($31,579) also include reserves for customer returns and discounts; this worksheet treats the total as the allowance for doubtful accounts. '
        'Accounts receivable (gross), other current assets, &ldquo;property, goodwill, brands and other&rdquo; and long-term liabilities are derived from reported totals. Q7 and Q9 use made-up numbers.')
note = ('Crocs&rsquo;s reported &ldquo;allowances&rdquo; ($31,579) also include reserves for customer returns and discounts; this worksheet treats the total as the allowance for doubtful accounts. '
        'Accounts receivable (gross), other current assets, &ldquo;property, goodwill, brands and other&rdquo; and long-term liabilities are derived from reported totals. Q7 uses made-up numbers.')
open(os.path.join(OUT, 'Ch8-BadDebt-Worksheet.html'), 'w').write(
    page('Bad Debts Worksheet', 'Crocs', 'ACC 250 &middot; Ch8 Opening Activity', front, '', note))
print('wrote Ch8-BadDebt-Worksheet')

# ======================================================================
# IPO: Anthropic S-1
# ======================================================================
S1_URL = 'https://www.sec.gov/Archives/edgar/data/0002130357/000162828026067168/anthropicpbc-sx1.htm'
IS = [('Revenue', '16.3', '$'),
      ('Cost of revenue and operating expenses', '(17.0)', 'u'),
      ('Operating income (loss)', '(0.7)', 'i'),
      ('Change in fair value of convertible notes and similar', '(72.4)', 'hd'),
      ('All other items, net*', '(7.6)', 'u'),
      ('Net income (loss)', '$ (80.7)', 'i uu')]
OTHER = [('Revenue, six months ended June 30, 2025', '1.2', '$'),
         ('Revenue, full year 2025', '4.6', ''),
         ('&ldquo;Adjusted&rdquo; operating income (company&rsquo;s non-GAAP measure)', '1.6', 'hd'),
         ('Convertible notes held by Amazon: amount lent (principal)', '6.2', 'hd'),
         ('Convertible notes: carried at fair value', '108.6', ''),
         ('Free cash flow, six months (analyst estimates)', '&asymp; 3.4', 'hd'),
         ('Long-term computing purchase commitments (not on balance sheet)', '500+', 'hd')]

front = f'''<h1>Anthropic&rsquo;s IPO Filing: Reading the S-1</h1>
<p class="filing"><b>Source:</b> Anthropic, PBC Form S-1, filed October 26, 2026, as reported in press coverage (six months ended June 30, 2026; $ billions) &middot;
<a href="{S1_URL}" target="_blank">{S1_URL.replace("https://www.", "")}</a></p>
<div class="cols">
{stmt('Anthropic, PBC', 'Condensed Income Statement', 'Six months, 2026', IS)}
{stmt('Anthropic, PBC', 'Other Reported Figures', '$ billions', OTHER)}
</div>
<div class="box"><b class="t">Background</b>An <b>S-1</b> is the document a company files with the SEC before it sells stock to the public for the first time (an IPO). It contains audited financial statements, risk factors, and management&rsquo;s discussion of the numbers. Anthropic makes Claude and earns revenue from API use and subscriptions.</div>
<h2>Find it in the statements <small>Write the amount ($ billions) or ratio. Use parentheses for losses.</small></h2>
{qlist([("How much revenue did Anthropic earn in the first six months of 2026?", "16.3"),
        ("How many times larger is that than revenue in the same six months of 2025?", "&asymp; 13.6 times"),
        ("What was the operating income (loss), from the core business?", "(0.7)"),
        ("What was the net income (loss)?", "(80.7)"),
        ("What percentage of the net loss came from the fair value change on the convertible notes?", "&asymp; 90%"),
        ("How much higher is &ldquo;adjusted&rdquo; operating income than GAAP operating income?", "2.3")], 1, full=True)}
'''

back = f'''<h2 style="margin-top:2pt">Hints</h2>
<div class="defs" style="font-size:9.3pt">
<dl>
<dt>Revenue recognition</dt><dd>Record revenue when it is <i>earned</i>. Cash received before the service is delivered is <b>unearned revenue</b>, a liability.</dd>
<dt>Convertible notes</dt><dd>Loans that the lender can turn into the company&rsquo;s stock. Anthropic reports them at <b>fair value</b>: when the stock becomes worth more, the liability grows and a <b>loss</b> is recorded.</dd>
<dt>Liability</dt><dd>An obligation arising from a <i>past</i> event. A promise to buy services in the future is a commitment, disclosed in the notes.</dd>
</dl>
<dl>
<dt>Stock-based compensation</dt><dd>Paying employees with shares: Dr Compensation expense, Cr Additional paid-in capital. An expense, but no cash leaves.</dd>
<dt>Non-GAAP (&ldquo;adjusted&rdquo;) measures</dt><dd>Management&rsquo;s own profit measures. They usually leave out stock compensation and one-time or non-cash items.</dd>
<dt>Accrual vs. cash</dt><dd>Net income records events when they happen; the cash flow statement shows the cash. Non-cash losses reduce net income but not cash.</dd>
</dl>
</div>

<h2 style="margin-top:10pt">Apply the concepts</h2>
<div class="qblock"><span class="no">7</span><div>
<p><b>Revenue recognition.</b> On Jan 1, a customer pays <b>$240</b> for a 12-month Claude subscription.<br>
Journal entry on Jan 1:</p>
{je(("Cash", "Unearned revenue", "240"))}
<p>Revenue earned by Mar 31: {inl("$60")} &nbsp; Still unearned on Mar 31: {inl("$180")}</p>
</div></div>

<div class="qblock"><span class="no">8</span><div>
<p><b>The fair value loss.</b> Record the 72.4 increase in the fair value of the convertible notes ($ billions).</p>
{je(("Loss on change in fair value", "Convertible notes payable", "72.4"))}
<p>Effect: liabilities {pick(["increase", "decrease", "no change"], "increase")}; &nbsp; equity {pick(["increases", "decreases", "no change"], "decreases")}; &nbsp; cash {pick(["increases", "decreases", "no change"], "no change")}</p>
</div></div>

<div class="qblock"><span class="no">9</span><div>
<p><b>Stock compensation.</b> Anthropic pays engineers partly in stock. The entry is Dr Compensation expense, Cr Additional paid-in capital. Does it reduce GAAP operating income? {pick(["yes", "no"], "yes")} &nbsp; Does it use cash? {pick(["yes", "no"], "no")}</p>
</div></div>

<div class="qblock"><span class="no">10</span><div>
<p><b>Commitments.</b> Anthropic has signed more than $500 billion of long-term deals to buy computing capacity in future years. Is this recorded as a liability on today&rsquo;s balance sheet? {pick(["yes", "no"], "no")} &nbsp; Why?</p>
<div class="lines"></div>
<div class="why">A liability needs a past event. The providers have not delivered the computing yet, so it is a future commitment, disclosed in the notes.</div>
</div></div>

<div class="qblock"><span class="no">11</span><div>
<p><b>Accrual vs. cash.</b> Net loss was (80.7), yet analysts estimate free cash flow of about +3.4. Explain in one sentence.</p>
<div class="lines"></div>
<div class="why">Most of the loss is the non-cash fair value change (72.4): it raised a liability but no cash left the company.</div>
</div></div>
'''
note = ('*All other items, net is derived: 80.7 &minus; 0.7 &minus; 72.4. Figures are from press and analyst coverage of the S-1 and are rounded; check the filing before citing them. '
        'Computing commitments were reported at roughly $518&ndash;537 billion. Q7 uses made-up numbers.')
open(os.path.join(OUT, 'Anthropic-S1-Worksheet.html'), 'w').write(
    page('IPO Filing Worksheet', 'Anthropic', 'ACC 250 &middot; Accounting in the News Worksheet', front, back, note))
print('wrote Anthropic-S1-Worksheet')
