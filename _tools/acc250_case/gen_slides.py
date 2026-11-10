import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sankey
spec = importlib.util.spec_from_file_location('g', os.path.join(os.path.dirname(__file__), 'gen_case.py'))
OUT = sys.argv[1]; shell = sys.argv[2]
src = open(os.path.join(os.path.dirname(__file__), 'gen_case.py')).read()
ns = {}
exec(src.split("def body(")[0].replace("OUT = sys.argv[1]", "OUT = ''"), ns)
C = ns['C']
lines = open(shell).read().split('\n')
head = '\n'.join(lines[:535]); tail = '\n'.join(lines[734:])
Q = [('ar','Expects to collect from customers','Receivables'),('cogs','Cost of the merchandise sold','Cost of sales / merchandise costs'),
     ('sga','Expense for wages, rent, utilities, advertising','Operating (SG&amp;A) expenses'),('inv','Cost of goods still on the shelves','Inventories'),
     ('ap','Owes suppliers for goods bought on credit','Accounts payable'),('tax','The government&rsquo;s share of the profit','Provision for income taxes'),
     ('ni','Left of revenue after all expenses','Net income'),('dep','Cost of buildings and equipment used up so far','Accumulated depreciation'),
     ('ocf','What buildings and equipment originally cost','Property and equipment, at cost'),('capex','Owed to lenders on long-term loans','Long-term debt'),
     ('div','Paid to shareholders','Dividends'),('re','Profit earned and kept over the years','Retained earnings')]
for key, c in C.items():
    A = c['A']; s = c['short']
    def items(sl, start):
        return '\n'.join(f'<li><span><b>{n}</b> &nbsp;{q} &rarr; <b class="hl">{a}</b></span><span class="chip yes">{A[k]}</span></li>'
                         for n,(k,q,a) in enumerate(sl, start))
    re = c['RE']; cf = {r[0]:r[1] for r in c['CF']}
    ni = A['ni']; dep = A['dep']; ocf = A['ocf']
    body = f'''
<section class="s title" data-nav="Cover">
<div class="tstack">
<p class="eyebrow">ACC 250 &middot; In-Class Case</p>
<h1>{s}: Reading the Real Financial Statements</h1>
<p class="lede">Know what each account means, and you can find it in the statements.</p>
</div>
<p class="title-date">Form 10-K, {c['fydesc']} &middot; $ millions</p>
</section>

<section class="s" data-nav="Where the revenue goes">
<p class="eyebrow">Income statement as a picture</p>
<h2 style="margin-bottom:6px">Where each revenue dollar goes</h2>
{getattr(sankey, key.lower())()}
<p class="fine" style="font-size:16px;margin-top:-4px">*Here gross profit = total revenue &minus; {'cost of sales' if key=='Walmart' else 'merchandise costs'}, so it includes membership income. The worksheet&rsquo;s gross profit margin uses net sales only. Green = profit, red = costs.</p>
</section>

<section class="s" data-nav="Q1–6">
<p class="eyebrow">Find it in the statements</p>
<h2>Know the concept, find the account</h2>
<ul class="items">
{items(Q[:6],1)}
</ul>
</section>

<section class="s" data-nav="Q7–12">
<p class="eyebrow">Find it in the statements</p>
<h2>Know the concept, find the account</h2>
<ul class="items">
{items(Q[6:],7)}
</ul>
</section>

<section class="s" data-nav="Connections">
<p class="eyebrow">How the numbers connect</p>
<h2>Cost, used up, and what is left</h2>
<div class="two">
<div class="stmt">
<table>
<tr><th>Property and equipment</th><th>$M</th></tr>
{''.join(f'<tr{" class=\"total\"" if "net" in r[0] else ""}><td>{r[0]}</td><td>{r[1]}</td></tr>' for r in c['BS'] if 'Property and equipment' in r[0] or 'Accumulated depreciation' in r[0])}
</table>
</div>
<div class="stmt">
<table>
<tr><th>Retained earnings</th><th>$M</th></tr>
{''.join(f'<tr{" class=\"total\"" if i==len(re)-1 else ""}><td>{r[0]}</td><td>{r[1]}</td></tr>' for i,r in enumerate(re))}
</table>
</div>
</div>
<div class="key"><span class="klab">Two connections</span>Net = cost &minus; accumulated depreciation. Net income flows into retained earnings.</div>
</section>

<section class="s" data-nav="13–15 · Ratios">
<p class="eyebrow">Ratios</p>
<h2>Three numbers that describe {s}</h2>
<div class="hbars">
<div class="hbar"><span>Gross profit margin</span><div class="track"><div class="fill" style="width:{A['gpm'].rstrip('%')}%;background:#1a7a5e"></div></div><span class="v">{A['gpm']}</span></div>
<div class="hbar"><span>Net profit margin</span><div class="track"><div class="fill" style="width:{A['npm'].rstrip('%')}%;background:#1a7a5e"></div></div><span class="v">{A['npm']}</span></div>
</div>
<div class="note"><b>13</b> {c['calc']['gpm']} = {A['gpm']} &nbsp;&middot;&nbsp; <b>14</b> {c['calc']['npm']} = {A['npm']}</div>
<div class="note"><b>15</b> Current ratio = {c['calc']['cr']} = <b class="hl">{A['cr']}</b></div>
<div class="key"><span class="klab">Takeaway</span>{c['why']}</div>
</section>
'''
    html = head.replace('<title>Anthropic S-1 Accounting</title>', f'<title>{s} Case Review</title>') + '\n' + body + '\n' + tail
    html = html.replace('.srcs a { color:var(--accent); }', '.srcs a { color:var(--accent); }\n.items li { grid-template-columns:1fr 210px; }\n.chip { font-size:24px; }\n.stmt table { font-size:24px; }\n.stmt td { padding:7px 10px; }\n.note { font-size:23px; }')
    open(os.path.join(OUT, c['file'] + '-Slides.html'), 'w').write(html)
    print('wrote', c['file'] + '-Slides')
