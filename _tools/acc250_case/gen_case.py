#!/usr/bin/env python3
"""Generate the one-sheet (front/back) in-class case worksheets for Walmart and Costco."""
import sys, os

OUT = sys.argv[1]

# row = (label, amount_str, flags)   flags: '$' dollar sign, 'u' underline, 'uu' double, 'i' indent (subtotal), 'hd' gap above, 'sec' section header
C = {}

C['Walmart'] = dict(
  file='Walmart-Case', co='Walmart Inc.', short='Walmart', fy='Fiscal 2025', end='Jan 31, 2025',
  begin='Jan 31, 2024', fydesc='fiscal year ended January 31, 2025',
  url='https://www.sec.gov/Archives/edgar/data/104169/000010416925000021/wmt-20250131.htm',
  IS=[('Net sales','674,538','$'),('Membership and other income','6,447','u'),('Total revenues','680,985','i'),
      ('Cost of sales','511,753','hd'),('Operating, selling, general &amp; admin. expenses','139,884','u'),('Operating income','29,348','i'),
      ('Interest, net','2,245','hd'),('Other (gains) and losses','794','u'),('Income before income taxes','26,309','i'),
      ('Provision for income taxes','6,152','u'),('Net income','20,157','i uu $')],
  BS=[('Cash and cash equivalents','9,037','$'),('Receivables, net','9,975',''),('Inventories','56,435',''),
      ('Prepaid expenses and other','4,011','u'),('Total current assets','79,458','i'),
      ('Property and equipment, at cost','231,617',''),('Less: Accumulated depreciation','(111,624)','u'),('Property and equipment, net','119,993','i'),('Leases, goodwill and other assets','61,372','u'),('Total assets','260,823','i uu $'),
      ('Accounts payable','58,666','hd $'),('Accrued and other current liabilities','37,918','u'),('Total current liabilities','96,584','i'),
      ('Long-term debt','33,401',''),('Lease obligations and other long-term liabilities','33,417','u'),('Total liabilities','163,402','i'),
      ('Common stock and paid-in capital','6,305','hd'),('Retained earnings','98,313',''),('Others (AOCI)','(7,197)','u'),
      ('Total equity','97,421','i u'),('Total liabilities and equity','260,823','i uu $')],
  RE=[('Retained earnings, Jan 31, 2024','89,814','$'),('Add: Net income','20,157',''),('Less: Dividends','(6,688)',''),
      ('Less: Others (incl. share repurchases, Ch11)','(4,970)','u'),('Retained earnings, Jan 31, 2025','98,313','i uu $')],
  CF=[('Operating activities','','sec'),('Net income','20,157','$'),('Depreciation and amortization','12,973',''),('All other operating items, net','3,313','u'),
      ('Net cash provided by operating activities','36,443','i'),
      ('Investing activities','','sec'),('Payments for property and equipment','(23,783)',''),('Other investing activities, net','2,404','u'),
      ('Net cash used in investing activities','(21,379)','i'),
      ('Financing activities','','sec'),('Dividends paid','(6,688)',''),('Purchase of company stock','(4,494)',''),('Other financing activities, net','(3,640)','u'),
      ('Net cash used in financing activities','(14,822)','i'),
      ('Effect of exchange rates and other','(1,072)','hd u'),('Net decrease in cash','(830)','i'),
      ('Cash, beginning of year','9,867','u'),('Cash, end of year','9,037','i uu $')],
  A=dict(ar='9,975',cogs='511,753',sga='139,884',inv='56,435',ap='58,666',tax='6,152',ni='20,157',dep='111,624',
         ocf='231,617',capex='33,401',div='6,688',re='98,313',gpm='24.1%',npm='3.0%',cr='0.82'),
  calc=dict(gpm='(674,538 &minus; 511,753) &divide; 674,538',npm='20,157 &divide; 680,985',cr='79,458 &divide; 96,584'),
  why='Walmart keeps about 3 cents of every sales dollar as profit. A current ratio below 1 is normal for Walmart: it sells its inventory before it has to pay its suppliers (accounts payable is larger than inventory).',
  note='Some lines are combined. Receivables are reported net of an allowance for credit losses; Walmart does not disclose the allowance amount separately. In retained earnings, &ldquo;Others&rdquo; also includes the share of net income that belongs to minority owners of subsidiaries.',
)

C['Costco'] = dict(
  file='Costco-Case', co='Costco Wholesale Corporation', short='Costco', fy='Fiscal 2025', end='Aug 31, 2025',
  begin='Sep 1, 2024', fydesc='fiscal year ended August 31, 2025',
  url='https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm',
  IS=[('Net sales','269,912','$'),('Membership fees','5,323','u'),('Total revenue','275,235','i'),
      ('Merchandise costs','239,886','hd'),('Selling, general and administrative','24,966','u'),('Operating income','10,383','i'),
      ('Interest and other income, net','435','hd u'),('Income before income taxes','10,818','i'),
      ('Provision for income taxes','2,719','u'),('Net income','8,099','i uu $')],
  BS=[('Cash and cash equivalents','14,161','$'),('Short-term investments and other','2,900',''),('Receivables, net','3,203',''),
      ('Merchandise inventories','18,116','u'),('Total current assets','38,380','i'),
      ('Property and equipment, at cost','50,840',''),('Less: Accumulated depreciation','(18,931)','u'),('Property and equipment, net','31,909','i'),('Lease right-of-use and other assets','6,810','u'),('Total assets','77,099','i uu $'),
      ('Accounts payable','19,783','hd $'),('Accrued salaries and other current liabilities','14,471',''),('Deferred membership fees','2,854','u'),
      ('Total current liabilities','37,108','i'),
      ('Long-term debt','5,713',''),('Lease and other long-term liabilities','5,114','u'),('Total liabilities','47,935','i'),
      ('Common stock and paid-in capital','8,284','hd'),('Retained earnings','22,650',''),('Others (AOCI)','(1,770)','u'),
      ('Total equity','29,164','i u'),('Total liabilities and equity','77,099','i uu $')],
  RE=[('Retained earnings, Sep 1, 2024','17,619','$'),('Add: Net income','8,099',''),('Less: Dividends','(2,183)',''),
      ('Less: Others (incl. share repurchases, Ch11)','(885)','u'),('Retained earnings, Aug 31, 2025','22,650','i uu $')],
  CF=[('Operating activities','','sec'),('Net income','8,099','$'),('Depreciation and amortization','2,426',''),('All other operating items, net','2,810','u'),
      ('Net cash provided by operating activities','13,335','i'),
      ('Investing activities','','sec'),('Additions to property and equipment','(5,498)',''),('Other investing activities, net','187','u'),
      ('Net cash used in investing activities','(5,311)','i'),
      ('Financing activities','','sec'),('Cash dividends paid','(2,183)',''),('Repurchases of common stock','(903)',''),('Other financing activities, net','(689)','u'),
      ('Net cash used in financing activities','(3,775)','i'),
      ('Effect of exchange rates','6','hd u'),('Net increase in cash','4,255','i'),
      ('Cash, beginning of year','9,906','u'),('Cash, end of year','14,161','i uu $')],
  A=dict(ar='3,203',cogs='239,886',sga='24,966',inv='18,116',ap='19,783',tax='2,719',ni='8,099',dep='18,931',
         ocf='50,840',capex='5,713',div='2,183',re='22,650',gpm='11.1%',npm='2.9%',cr='1.03'),
  calc=dict(gpm='(269,912 &minus; 239,886) &divide; 269,912',npm='8,099 &divide; 275,235',cr='38,380 &divide; 37,108'),
  why='Costco keeps about 3 cents of every sales dollar as profit, and only about 11 cents after paying for the goods: it makes much of its profit from membership fees.',
  note='Some lines are combined. &ldquo;Interest and other income, net&rdquo; = interest income and other minus interest expense. Property and equipment at cost = net + accumulated depreciation. Costco reports its allowance on receivables as immaterial.',
)

def body(rows, colhead):
    out = ['<table>', f'<tr><th></th><th>{colhead}</th></tr>']
    for lab, amt, fl in rows:
        f = fl.split()
        if 'sec' in f:
            out.append(f'<tr class="sec"><td>{lab}</td><td></td></tr>'); continue
        cls = ' '.join(c for c in ('u','uu','hd') if c in f)
        lcls = ' class="i1"' if 'i' in f else ''
        d = '<i>$</i>' if '$' in f else ''
        out.append(f'<tr class="{cls}"><td{lcls}>{lab}</td><td class="n">{d}{amt}</td></tr>')
    out.append('</table>')
    return '\n'.join(out)

def stmt(title, unit, colhead, rows, extra=''):
    return f'<div class="stmt{extra}"><p class="co">{CO}</p><p class="ttl">{title}</p>' + body(rows, colhead) + '</div>'

def stmt_split(title, colhead, rows):
    k = next(i for i,r in enumerate(rows) if r[0]=='Financing activities')
    return (f'<div class="stmt wide"><p class="co">{CO}</p><p class="ttl">{title}</p><div class="cols in">'
            + '<div>' + body(rows[:k], colhead) + '</div><div>' + body(rows[k:], colhead) + '</div></div></div>')

QS = [('ar','How much does {s} expect to collect from its customers?'),
      ('cogs','What did the merchandise {s} sold this year cost it?'),
      ('sga','What expense did it record for wages, rent, utilities and advertising?'),
      ('inv','What is the cost of the goods still on its shelves and in warehouses?'),
      ('ap','How much does it owe suppliers for goods bought on credit?'),
      ('tax',"What is the government&rsquo;s share of this year&rsquo;s profit?"),
      ('ni','What was left of revenue after all expenses this year?'),
      ('dep','How much of its buildings&rsquo; and equipment&rsquo;s cost has been used up so far?'),
      ('ocf','What did its buildings and equipment originally cost?'),
      ('capex','How much does it owe lenders on long-term loans?'),
      ('div','How much did it pay its shareholders as dividends?'),
      ('re','How much profit has it earned over the years and kept in the business?')]

CSS = open(os.path.join(os.path.dirname(__file__), 'case.css')).read()

for key, c in C.items():
    CO = c['co']; s = c['short']; A = c['A']
    half = len(QS) // 2
    def qcol(items, start):
        rows = []
        for n, (k, q) in enumerate(items, start):
            rows.append(f'<li><span class="no">{n}</span><span class="qt">{q.format(s=s)}</span><span class="bl amt" data-a="{A[k]}"></span></li>')
        return '<ol class="qs">' + ''.join(rows) + '</ol>'
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s} In-Class Case</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="bar">
  <button id="kbtn" onclick="toggleKey()">Show answers</button>
  <button onclick="print()">Print</button>
</div>

<!-- =========================== PAGE 1 =========================== -->
<div class="page">
<header>
  <div class="course">ACC 250 &middot; In-Class Case (10 min)<span class="keytag"> &middot; Answer key</span></div>
  <div class="name">Name <span></span></div>
</header>
<h1>{s}: Reading the Real Financial Statements</h1>
<p class="filing"><b>Source:</b> {CO} Form 10-K, {c['fydesc']} (some lines combined; amounts in millions) &middot;
<a href="{c['url']}" target="_blank">{c['url'].replace('https://www.','')}</a></p>

<div class="cols">
<div>
{stmt('Consolidated Statement of Income','',c['fy'],c['IS'])}
{stmt('Statement of Retained Earnings','',c['fy'],c['RE'],' gapt')}
</div>
{stmt('Consolidated Balance Sheet','',c['end'],c['BS'])}
</div>

<h2>Find it in the statements <small>Write the amount ($ millions). Definitions are on the back.</small></h2>
<div class="qcols">
{qcol(QS[:half],1)}
{qcol(QS[half:],half+1)}
</div>
</div>

<!-- =========================== PAGE 2 =========================== -->
<div class="page">
<h2 style="margin-top:2pt">Key concepts (hints)</h2>
<div class="defs">
<div>
<h3>Income statement &middot; a whole year</h3>
<dl>
<dt>Revenue (net sales)</dt><dd>What the company earns from selling goods and services, recorded when <i>earned</i>.</dd>
<dt>Cost of sales (cost of goods sold, merchandise costs)</dt><dd>The cost of the inventory that was <i>sold</i>. It leaves the balance sheet and becomes an expense.</dd>
<dt>Operating expenses (SG&amp;A)</dt><dd>Costs of running the business other than the goods: wages, rent, utilities, advertising.</dd>
<dt>Depreciation</dt><dd>The part of a building&rsquo;s or equipment&rsquo;s cost recorded as an expense each year as it is used up. No cash is paid when it is recorded.</dd>
<dt>Income tax expense (provision)</dt><dd>The government&rsquo;s share of the profit.</dd>
<dt>Net income</dt><dd>Revenue minus <i>all</i> expenses, including interest and taxes.</dd>
</dl>
<h3>Statement of retained earnings</h3>
<dl>
<dt>Retained earnings</dt><dd>Profit earned since the start and kept in the business. Beginning + Net income &minus; Dividends = Ending.</dd>
<dt>Dividends</dt><dd>Profit paid out to shareholders. Not an expense.</dd>
</dl>
</div>
<div>
<h3>Balance sheet &middot; one date</h3>
<dl>
<dt>Assets = Liabilities + Equity</dt><dd>Everything the company owns is financed by creditors or by owners.</dd>
<dt>Current assets / current liabilities</dt><dd>Expected to be used up or paid within one year.</dd>
<dt>Accounts receivable</dt><dd>Amounts customers owe the company, expected to be collected in cash.</dd>
<dt>Inventory</dt><dd>Goods held for sale, recorded at cost until sold.</dd>
<dt>Accumulated depreciation</dt><dd>All depreciation recorded so far on buildings and equipment. Cost &minus; accumulated depreciation = net (book value).</dd>
<dt>Accounts payable</dt><dd>Amounts owed to suppliers for goods or services bought on credit.</dd>
<dt>Long-term debt</dt><dd>Money borrowed (loans, bonds) that is due after more than one year.</dd>
</dl>

</div>
</div>

<h2 style="margin-top:12pt">Finally, calculate (use the numbers on the front)</h2>
<table class="ratios">
<tr><td><span class="no">13</span></td><td><b>Gross profit margin</b><br><span class="f">= (Net sales &minus; Cost of sales) &divide; Net sales</span></td><td class="ans"><span class="bl amt" data-a="{A['gpm']}"></span></td></tr>
<tr><td><span class="no">14</span></td><td><b>Net profit margin</b><br><span class="f">= Net income &divide; Total revenue</span></td><td class="ans"><span class="bl amt" data-a="{A['npm']}"></span></td></tr>
<tr><td><span class="no">15</span></td><td><b>Current ratio</b><br><span class="f">= Total current assets &divide; Total current liabilities</span></td><td class="ans"><span class="bl amt" data-a="{A['cr']}"></span></td></tr>
</table>
<div class="why">13: {c['calc']['gpm']} = {A['gpm']} &nbsp;&middot;&nbsp; 14: {c['calc']['npm']} = {A['npm']} &nbsp;&middot;&nbsp; 15: {c['calc']['cr']} = {A['cr']}.<br>{c['why']}</div>

<p class="src">{c['note']}</p>
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
    open(os.path.join(OUT, c['file'] + '.html'), 'w').write(html)
    print('wrote', c['file'])
