"""Step-by-step lecture slides for each shareholder-letter theme (keyed by theme title in gen_letters.py).

Each deck: list of (frame title, body HTML). gen_letter_slides.py adds the title slide, the letter's quote,
the questions and the sources. Notation follows the ACC250 handouts (PPE (+A), Depreciation Expense (+E),
Accumulated Depreciation (+xA, −A), APIC (+SE), Treasury Stock (+xSE, −SE), ...).
"""
import math, re

M = '&minus;'


def EX(s):
    return f'<p><span class="ex">EX.</span> {s}</p>'


def JE(*entries):
    """entries: (date, [(account, debit, credit), ...]); a line with no debit is a credit line (indented)."""
    rows = []
    for date, lines in entries:
        for k, (acct, dr, cr) in enumerate(lines):
            d = f'<td class="jd" rowspan="{len(lines)}">{date}</td>' if k == 0 else ''
            a = acct if dr else f'<span class="ind">{acct}</span>'
            rows.append(f'<tr>{d}<td class="jl">{a}</td><td class="jdr">{dr or ""}</td><td class="jcr">{cr or ""}</td></tr>')
        rows.append('<tr class="gap"><td colspan="4"></td></tr>')
    return '<div class="rbox je"><table>' + ''.join(rows[:-1]) + '</table></div>'


def TB(head, rows, hl=None, small=False):
    """Booktabs table; first column left; other columns right if they hold numbers, else left. hl: {row index: 'yel' | 'pink'}."""
    hl = hl or {}
    num = [k > 0 and all(re.match(r'(\$|\(|\d|&minus;|N/A|&mdash;|Usually|Higher|Lower|reduces)', r[k]) for r in rows) for k in range(len(head))]
    c = lambda k: ' class=r' if num[k] else ''
    h = '<tr>' + ''.join(f'<th{c(k)}>{x}</th>' for k, x in enumerate(head)) + '</tr>'
    b = ''.join(f'<tr{" class=" + hl[i] if i in hl else ""}>' + ''.join(f'<td{c(k)}>{x}</td>' for k, x in enumerate(r)) + '</tr>'
                for i, r in enumerate(rows))
    return f'<table class="bt{" sm" if small else ""}">{h}{b}</table>'


def BOX(s):
    return f'<div class="rbox">{s}</div>'


def UL(*xs):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'


def OL(*xs):
    return '<ol>' + ''.join(f'<li>{x}</li>' for x in xs) + '</ol>'


def pie(items, note):
    """items: (label, value, color). Percent inside, label and value outside."""
    W, H, cx, cy, r = 1000, 440, 500, 210, 170
    tot = sum(v for _, v, _ in items)
    out = [f'<svg viewBox="0 0 {W} {H}" style="width:86%;height:auto;display:block;margin:0 auto" font-family="Helvetica Neue,Arial,sans-serif">']
    a0 = -math.pi / 2
    for name, v, col in items:
        a1 = a0 + v / tot * 2 * math.pi
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        out.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {1 if a1 - a0 > math.pi else 0} 1 {x1:.1f},{y1:.1f} Z" fill="{col}" stroke="#fff" stroke-width="3"/>')
        am = (a0 + a1) / 2
        out.append(f'<text x="{cx + r*.62*math.cos(am):.1f}" y="{cy + r*.62*math.sin(am) + 9:.1f}" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">{v/tot*100:.0f}%</text>')
        lx, ly = cx + (r + 30) * math.cos(am), cy + (r + 30) * math.sin(am)
        an = 'start' if math.cos(am) >= 0 else 'end'
        out.append(f'<line x1="{cx + r*math.cos(am):.1f}" y1="{cy + r*math.sin(am):.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="#888" stroke-width="1.5"/>')
        out.append(f'<text x="{lx:.1f}" y="{ly - 4:.1f}" text-anchor="{an}" font-size="24" font-weight="700" fill="#333">{name}</text>')
        out.append(f'<text x="{lx:.1f}" y="{ly + 24:.1f}" text-anchor="{an}" font-size="22" fill="#333">${v:,.0f}B</text>')
        a0 = a1
    out.append(f'<text x="{cx}" y="{H - 4}" text-anchor="middle" font-size="22" fill="#333">{note}</text></svg>')
    return ''.join(out)


def timeline():
    """Operating cycle: buy inventory (day 0), sell (19), collect (24), pay supplier (50)."""
    X = lambda d: 90 + d * 16
    s = ['<svg viewBox="0 0 1000 300" style="width:96%;height:auto;display:block;margin:6px auto" font-family="Helvetica Neue,Arial,sans-serif">',
         f'<line x1="{X(0)}" y1="150" x2="{X(50)}" y2="150" stroke="#000" stroke-width="2"/>']
    for d, lab, an, y in [(0, 'Buy inventory', 'start', 128), (19, 'Sell', 'end', 128), (24, 'Collect cash', 'start', 128), (50, 'Pay supplier', 'end', 128)]:
        dx = -6 if an == 'start' and d == 0 else (6 if an == 'end' and d == 19 else 0)
        s.append(f'<circle cx="{X(d)}" cy="150" r="8" fill="#3333b3"/>'
                 f'<text x="{X(d) + (-10 if d == 0 else 10 if d == 24 else 8 if d == 19 else 0)}" y="{y}" text-anchor="{an}" font-size="22" font-weight="700">{lab}</text>'
                 f'<text x="{X(d)}" y="180" text-anchor="middle" font-size="20">Day {d}</text>')
    s.append(f'<line x1="{X(0)}" y1="60" x2="{X(24)}" y2="60" stroke="#3333b3" stroke-width="3"/>'
             f'<text x="{X(12)}" y="48" text-anchor="middle" font-size="20" fill="#3333b3">inventory + receivable days = 24</text>'
             f'<rect x="{X(24)}" y="196" width="{X(50) - X(24)}" height="30" fill="#fff26b"/>'
             f'<text x="{(X(24) + X(50)) / 2}" y="218" text-anchor="middle" font-size="20" font-weight="700">cash in hand: 26 days</text>'
             f'<line x1="{X(0)}" y1="262" x2="{X(50)}" y2="262" stroke="#b3200f" stroke-width="3"/>'
             f'<text x="{X(25)}" y="290" text-anchor="middle" font-size="20" fill="#b3200f">payable days = 50</text></svg>')
    return ''.join(s)


D = {}

# ---------------------------------------------------------------- Cash flow
D['GAAP earnings vs. cash flows'] = [
 ('Step 1: Two Ways to Keep Score', UL(
   '<b>Accrual basis</b> (GAAP): record revenue when <b>earned</b> and expenses when <b>incurred</b>.',
   '<b>Cash basis</b>: record only when cash comes in or goes out.',
   'Net income (accrual) and the change in cash are usually <span class="hl">different numbers</span>.')),
 ('Step 2: Revenue Earned, No Cash Yet', EX('Sell $80 of goods on account on Dec 20; the customer pays on Jan 15.')
  + JE(('Dec 20:', [('A/R (+A)', '80', None), ('Sales Rev (+R)', None, '80')])) + TB(['', 'December', 'January'],
   [['Revenue recorded', '$80', '$0'], ['Cash collected', '$0', '$80']])),
 ('Step 3: Cash Paid, Expense Later', EX('Pay $60 cash for equipment with a 3-year life (no salvage value).')
  + JE(('Jan 1:', [('PPE (+A)', '60', None), ('Cash (' + M + 'A)', None, '60')]),
       ('Dec 31:', [('Depreciation Expense (+E)', '20', None), ('Accumulated Depreciation (+xA, ' + M + 'A)', None, '20')]))
  + TB(['Year 1', 'Amount'], [['Cash paid', '$60'], ['Expense recorded', '$20']])),
 ('Step 4: From Net Income to Cash', EX('Net income $25; depreciation $40; paid $60 cash for new equipment.')
  + TB(['', 'Amount'], [['Net income', '$25'], ['+ Depreciation (expense, no cash this year)', '40'],
                       [M + ' Cash paid for equipment (no expense this year)', '(60)'], ['Change in cash', '$5']], hl={3: 'yel'})),
 ('Back to the Letter', UL(
   'Bezos (1997): if a choice makes GAAP earnings <b>look</b> better but lowers future cash flows, Amazon takes the <b>cash flows</b>.',
   'Bezos (2001): a share of stock is a share of the company&rsquo;s <b>future cash flows</b>.',
   'Lesson: read net income <b>and</b> the cash flow statement.')),
]

D['Free cash flow per share'] = [
 ('Step 1: Start with Operating Cash Flow', UL(
   '<b>Net cash from operating activities</b> (CFO): cash from running the business (customers in, suppliers and employees out).',
   'Found in the first section of the statement of cash flows.')
  + EX('Amazon 2002: net cash provided by operating activities = <b>$174 million</b>.')),
 ('Step 2: Subtract Capital Expenditures', UL(
   '<b>Capital expenditures</b> (capex) = purchases of fixed assets (PPE), in the investing section.',
   '<b>Free cash flow</b> = CFO ' + M + ' capex: cash left after keeping and growing the asset base.')
  + TB(['Amazon ($ millions)', '2001', '2002'], [['Net cash from operating activities', '(120)', '174'],
       [M + ' Purchases of fixed assets', '(50)', '(39)'], ['Free cash flow', '(170)', '135']], hl={2: 'yel'})
  + '<p class="note">Amounts from the 2002 letter&rsquo;s footnote.</p>'),
 ('Step 3: Divide by Shares Outstanding', EX('Free cash flow $120 million; 400 million shares outstanding.')
  + TB(['', 'Amount'], [['Free cash flow', '$120M'], ['&divide; Shares outstanding', '400M'], ['Free cash flow per share', '$0.30']], hl={2: 'yel'})
  + UL('More shares (dilution) &rarr; less per share, even if free cash flow is the same.')),
 ('Back to the Letter', UL(
   'Bezos (2004): free cash flow per share is Amazon&rsquo;s &ldquo;ultimate financial measure.&rdquo;',
   'Why not earnings? Earnings do not directly become cash: <b>working capital</b>, <b>capex</b> and <b>dilution</b> also matter.')),
]

D['Owner earnings'] = [
 ('Step 1: Start with Net Income', UL('Net income (GAAP) includes <b>non-cash</b> charges such as depreciation and amortization (D&amp;A).')
  + EX('Net income $100; D&amp;A $40; capital spending needed just to maintain the business $50.')),
 ('Step 2: Add Back Non-cash Charges', TB(['', 'Amount'], [['Net income', '$100'], ['+ Depreciation and amortization', '40'],
                                                    ['Subtotal', '$140']], hl={2: 'pink'})
  + UL('D&amp;A reduced net income, but no cash left the business this year.')),
 ('Step 3: Subtract Maintenance Capex', TB(['', 'Amount'], [['Net income', '$100'], ['+ Depreciation and amortization', '40'],
       [M + ' Maintenance capital spending', '(50)'], ['Owner earnings', '$90']], hl={3: 'yel'})
  + UL('<b>Maintenance</b> capex: what must be spent just to stay competitive (not growth).')),
 ('Back to the Letter', UL(
   'Buffett (1986): owner earnings, not GAAP earnings, are what matter for <b>valuing</b> a business.',
   'Adding back D&amp;A without subtracting capex (like EBITDA) overstates what owners can take out.',
   'Maintenance capex is an estimate: management has to judge it.')),
]

D['EBITDA ignores a real cost'] = [
 ('Step 1: Build EBITDA from Net Income', UL('<b>EBITDA</b> = Earnings Before Interest, Taxes, Depreciation and Amortization.')
  + EX('Net income $50, interest $10, income taxes $20, D&amp;A $30.')
  + TB(['', 'Amount'], [['Net income', '$50'], ['+ Interest expense', '10'], ['+ Income tax expense', '20'],
                       ['+ Depreciation and amortization', '30'], ['EBITDA', '$110']], hl={4: 'yel'})),
 ('Step 2: Where Does Depreciation Come From?', EX('Buy a truck for $300 cash; 10-year life (no salvage value).')
  + JE(('Year 1:', [('PPE (+A)', '300', None), ('Cash (' + M + 'A)', None, '300')]),
       ('Each Dec 31:', [('Depreciation Expense (+E)', '30', None), ('Accumulated Depreciation (+xA, ' + M + 'A)', None, '30')]))
  + UL('The <b>cash</b> was paid up front; depreciation spreads that cost over 10 years.')),
 ('Step 3: What EBITDA Leaves Out', TB(['', 'Year 1'], [['Cash paid for the truck', '$300'], ['Depreciation in EBITDA', '$0']], hl={1: 'pink'})
  + UL('EBITDA treats depreciation as if it were not a cost &rarr; the truck looks free.',
       'Someday the truck must be replaced &rarr; real cash.')),
 ('Back to the Letter', UL(
   'Buffett (2000): &ldquo;does management think the tooth fairy pays for capital expenditures?&rdquo;',
   'Buffett (2002): trumpeting EBITDA implies depreciation is not truly an expense.')),
]

D['Growing earnings, negative free cash flow'] = [
 ('Step 1: Earnings Double Every Year', '<p>Bezos&rsquo;s example: a business buys machines to grow ($ thousands).</p>'
  + TB(['', 'Year 1', 'Year 2', 'Year 3', 'Year 4'], [['Sales', '100,000', '200,000', '400,000', '800,000'],
       ['Depreciation', '(40,000)', '(80,000)', '(160,000)', '(320,000)'], ['Earnings', '10,000', '20,000', '40,000', '80,000']], hl={2: 'yel'}, small=True)
  + UL('Earnings growth: 100% a year. Investors would be delighted.')),
 ('Step 2: Add Back Depreciation', TB(['', 'Year 1', 'Year 2', 'Year 3', 'Year 4'], [['Earnings', '10,000', '20,000', '40,000', '80,000'],
       ['+ Depreciation', '40,000', '80,000', '160,000', '320,000'], ['Operating cash flow', '50,000', '100,000', '200,000', '400,000']], hl={2: 'pink'}, small=True)
  + UL('No change in working capital in the example, so operating cash flow = earnings + depreciation.')),
 ('Step 3: Subtract Capital Expenditures', TB(['', 'Year 1', 'Year 2', 'Year 3', 'Year 4'], [['Operating cash flow', '50,000', '100,000', '200,000', '400,000'],
       [M + ' Capital expenditures', '(160,000)', '(160,000)', '(320,000)', '(640,000)'], ['Free cash flow', '(110,000)', '(60,000)', '(120,000)', '(240,000)']], hl={2: 'yel'}, small=True)
  + UL('New machines are paid for <b>up front</b>; their cost reaches earnings only slowly.')),
 ('Back to the Letter', UL(
   'Bezos (2004): a company can hurt shareholder value <b>by growing earnings</b>.',
   'Same example with EBITDA: $50, $100, $200, $400 million &rarr; &ldquo;EBITDA isn&rsquo;t cash flow.&rdquo;',
   'Over four years the business has negative free cash flow of $530 million.')),
]

D['Capex, useful lives and free cash flow'] = [
 ('Step 1: Capex Is Recorded as an Asset', EX('Pay $30 billion cash for datacenters (30-year useful life).')
  + JE(('Year 1:', [('PPE (+A)', '30B', None), ('Cash (' + M + 'A)', None, '30B')]))
  + UL('No expense when the asset is bought: it is an asset, not an expense.')),
 ('Step 2: Depreciation over the Useful Life', TB(['Asset', 'Cost', 'Useful life', 'Depreciation per year'],
       [['Datacenters', '$30B', '30 years', '$1.0B'], ['Chips and servers', '$12B', '6 years', '$2.0B']])
  + UL('Straight-line, no salvage value: cost &divide; useful life.',
       'Useful lives from the 2025 letter: 30+ years for datacenters; 5&ndash;6 years for chips, servers and networking gear.')),
 ('Step 3: Year 1 Effect: Net Income vs. Free Cash Flow', TB(['Year 1', 'Net income (pre-tax)', 'Free cash flow'],
       [['Datacenters', '(1.0B)', '(30.0B)'], ['Chips and servers', '(2.0B)', '(12.0B)'], ['Total', '(3.0B)', '(42.0B)']], hl={2: 'yel'})
  + UL('When capex grows faster than revenue, free cash flow falls far more than net income.')),
 ('Back to the Letter', UL(
   'Jassy (2025): AWS pays for land, power, buildings and chips 6&ndash;24 months before it bills customers.',
   'Amazon plans about <b>$200 billion</b> of capex in 2026 and accepts short-term free cash flow headwinds.',
   'Useful lives are <b>estimates</b>: a longer life means lower depreciation and higher earnings.')),
]

# ---------------------------------------------------------------- Non-GAAP
D['"Adjusted" earnings'] = [
 ('Step 1: Start with GAAP Net Income', UL('GAAP net income includes <b>every</b> expense GAAP requires.',
   '&ldquo;Adjusted&rdquo; (non-GAAP) earnings: management removes some expenses.') + EX('GAAP net income = $80 million.')),
 ('Step 2: Management&rsquo;s Add-backs', TB(['', '$ millions'], [['GAAP net income', '$80'], ['+ Stock-based compensation', '15'],
       ['+ Amortization of intangibles', '10'], ['&ldquo;Adjusted&rdquo; earnings', '$105']], hl={3: 'pink'})
  + UL('Adjusted earnings are 31% higher than GAAP net income.')),
 ('Step 3: Ask: Is It a Real Cost?', TB(['Add-back', 'Real cost?'], [['Stock-based compensation', 'Yes: employees are paid in stock instead of cash'],
       ['Amortization of intangibles', 'Often: the company paid for those assets'], ['One-time charges every year', 'Then they are not one-time']], small=True)),
 ('Back to the Letter', UL(
   'Buffett (2016): too many managements feature &ldquo;adjusted earnings&rdquo; that are higher than GAAP earnings.',
   'Compensation is compensation, whatever form it takes &rarr; it belongs in earnings.')),
]

D['Pro forma results'] = [
 ('Step 1: GAAP Operating Result', UL('<b>Pro forma</b> (non-GAAP) results: the company&rsquo;s own version of profit.')
  + EX('GAAP operating loss = $(20) million.')),
 ('Step 2: Leave Out Selected Expenses', TB(['', '$ millions'], [['GAAP operating income (loss)', '$(20)'],
       ['+ Stock-based compensation', '35'], ['+ Amortization of goodwill', '15'], ['Pro forma operating profit', '$30']], hl={3: 'pink'})
  + UL('A $20 million loss becomes a $30 million &ldquo;profit.&rdquo;')),
 ('Step 3: Always Reconcile to GAAP', UL(
   'GAAP does not define pro forma results &rarr; the company chooses what to leave out.',
   'Since 2003 (SEC Regulation G), a company that reports a non-GAAP number must also show the GAAP number and reconcile the two.',
   'Compare the two figures every time.')),
 ('Back to the Letter', UL(
   'Bezos (2000 letter, early 2001): goal of a <b>pro forma</b> operating profit in Q4 2001.',
   'Bezos (2001): Q4 2001 pro forma operating profit of $59 million and pro forma net profit of $35 million.',
   'Auditors (ACC531): non-GAAP measures are a <b>fraud risk</b> signal when the gap to GAAP keeps growing.')),
]

D['Earnings management'] = [
 ('Step 1: The Restructuring Charge', UL(
   '<b>Restructuring charge</b>: expense for closing plants, cutting jobs, &hellip; recorded when the plan is made.',
   '<b>Big bath</b>: charge too much in a bad year, so future years look better.')
  + EX('Year 1 is a bad year. Management books a $40 restructuring charge; only $30 will actually be needed.')),
 ('Step 2: The Entries', JE(('Year 1:', [('Restructuring Expense (+E)', '40', None), ('Restructuring Liability (+L)', None, '40')]),
       ('Year 2:', [('Restructuring Liability (' + M + 'L)', '30', None), ('Cash (' + M + 'A)', None, '30')]),
       ('Year 2:', [('Restructuring Liability (' + M + 'L)', '10', None), ('Restructuring Expense (' + M + 'E)', None, '10')]))
  + UL('The extra $10 is reversed in Year 2 &rarr; Year 2 profit goes <b>up</b> by $10.')),
 ('Step 3: Compare the Two Years', EX('Profit before the charge: $80 each year.')
  + TB(['', 'Year 1', 'Year 2'], [['Honest: $30 charge', '$50', '$80'], ['Big bath: $40 charge, $10 reversed', '$40', '$90']], hl={1: 'pink'})
  + UL('Same business, same cash. Only the timing of expenses changed.')),
 ('Back to the Letter', UL(
   'Buffett (1998): the restructuring charge is &ldquo;the distortion du jour,&rdquo; too often a device for manipulating earnings.',
   '&ldquo;We prefer a lumpy 15% return to a smooth 12%.&rdquo;',
   'Auditors (ACC531): test reserve reversals; very smooth earnings are a red flag.')),
]

# ---------------------------------------------------------------- Performance
D['Operating income and segments'] = [
 ('Step 1: Operating Margin', UL('<b>Operating margin</b> = operating income &divide; revenue: cents of operating profit per $1 of sales.')
  + TB(['Amazon ($ billions)', '2022', '2023', '2024'], [['Revenue', '$514', '$575', '$638'], ['Operating income', '$12.2', '$36.9', '$68.6'],
       ['Operating margin', '2.4%', '6.4%', '10.8%']], hl={2: 'yel'})
  + '<p class="note">Amounts from the 2023 and 2024 letters.</p>'),
 ('Step 2: Revenue by Segment (2024)', pie([('North America', 387, '#3333b3'), ('International', 143, '#8a8ae6'), ('AWS', 108, '#ff9900')],
       'Total revenue: $638B, 2024')
  + '<p class="note">Segment revenue from the 2024 letter.</p>'),
 ('Step 3: Operating Income by Segment (2024)', TB(['$ billions', 'Revenue', 'Operating income', 'Margin'],
       [['North America', '$387', '$25.0', '6%'], ['International', '$143', '$3.8', '3%'], ['AWS', '$108', '$39.8', '37%'], ['Total', '$638', '$68.6', '11%']], hl={2: 'yel'})
  + UL('AWS: 17% of revenue but 58% of operating income.')
  + '<p class="note">Segment operating income from Amazon&rsquo;s 2024 Form 10-K (segment information); margins computed.</p>'),
 ('Back to the Letter', UL(
   'Jassy (2023, 2024): operating income rose from $12.2B to $68.6B in two years.',
   'Segment results show <b>where</b> the profit comes from: here, mostly AWS.')),
]

D['Fixed costs and operating leverage'] = [
 ('Step 1: Fixed vs. Variable Costs', UL('<b>Variable costs</b> rise with sales (cost of goods sold, shipping).',
   '<b>Fixed costs</b> stay the same when sales change (software, a website, headquarters).')
  + EX('Variable costs: 60% of sales. Fixed costs: $100.')),
 ('Step 2: Double the Sales', TB(['', 'Before', 'After'], [['Sales', '$500', '$1,000'], [M + ' Variable costs (60%)', '(300)', '(600)'],
       [M + ' Fixed costs', '(100)', '(100)'], ['Operating income', '$100', '$300']], hl={3: 'yel'})
  + UL('Sales &times;2, operating income &times;3: <b>operating leverage</b>.')),
 ('Step 3: Fixed Costs as a Percent of Sales', TB(['', 'Before', 'After'], [['Fixed costs', '$100', '$100'], ['Sales', '$500', '$1,000'],
       ['Fixed costs &divide; sales', '20%', '10%']], hl={2: 'pink'})
  + UL('Works in reverse too: when sales fall, operating income falls faster.')),
 ('Back to the Letter', UL(
   'Bezos (2002): customer-experience costs are largely fixed, &ldquo;more like a publishing model than a retailing model.&rdquo;',
   'Bezos (2001): growth spreads fixed costs across more sales &rarr; lower cost per unit &rarr; lower prices.')),
]

D['Operating cycle and inventory turnover'] = [
 ('Step 1: Days in Inventory', UL('<b>Inventory turnover</b> = CGS &divide; average inventory.', '<b>Days in inventory</b> = 365 &divide; inventory turnover.')
  + EX('Amazon (2002): inventory turns 19 times a year &rarr; 365 &divide; 19 &asymp; <b>19 days</b>.')),
 ('Step 2: Add Receivable Days, Subtract Payable Days', TB(['', 'Days'], [['Days in inventory', '19'], ['+ Days of sales in A/R', '5'],
       [M + ' Accounts payable days', '(50)'], ['Operating cycle (letter&rsquo;s definition)', '(26)']], hl={3: 'yel'})
  + UL('Customers pay by card within days; suppliers are paid later.')),
 ('Step 3: See It on a Timeline', timeline()
  + UL('Negative cycle: Amazon <b>collects before it pays</b>; suppliers finance its inventory.')),
 ('Back to the Letter', UL(
   'Bezos (2004): a &ldquo;cash generative operating cycle&rdquo;: turn inventory quickly and collect before paying suppliers.',
   'Bezos (1999, 2004): low inventory for its sales ($480 million of inventory on nearly $7 billion of sales in 2004).')),
]

# ---------------------------------------------------------------- Assets
D['Economic vs. accounting goodwill'] = [
 ('Step 1: The Purchase', EX('Pay $500 cash for a company. Fair value of its assets: $450; liabilities: $70.')
  + TB(['', 'Amount'], [['Fair value of assets', '$450'], [M + ' Fair value of liabilities', '(70)'], ['Identifiable net assets', '$380']], hl={2: 'pink'})),
 ('Step 2: Goodwill = Price ' + M + ' Net Assets', TB(['', 'Amount'], [['Purchase price', '$500'], [M + ' Identifiable net assets', '(380)'], ['Goodwill', '$120']], hl={2: 'yel'})
  + JE(('Acq. date:', [('Assets (+A)', '450', None), ('Goodwill (+A)', '120', None), ('Liabilities (+L)', None, '70'), ('Cash (' + M + 'A)', None, '500')]))),
 ('Step 3: After the Purchase', UL(
   'Goodwill is <b>not amortized</b> (U.S. GAAP since 2002); it is tested for <b>impairment</b>.',
   'Goodwill a company <b>builds itself</b> (brand, reputation) is <b>never</b> recorded.')),
 ('Back to the Letter', UL(
   'Buffett (1983): <b>economic</b> goodwill = the power to earn high returns on tangible assets.',
   '<b>Accounting</b> goodwill = only what was paid in an acquisition &rarr; the two can differ enormously.',
   'See&rsquo;s Candies: large economic goodwill, small accounting goodwill.')),
]

D['Purchase vs. pooling for acquisitions'] = [
 ('Step 1: Same Deal, Two Methods (before 2001)', EX('Pay $500 for a company; book value of its net assets $300; fair value $380.')
  + TB(['', 'Purchase', 'Pooling'], [['Net assets recorded at', 'Fair value $380', 'Book value $300'], ['Goodwill', '$120', '$0']], hl={1: 'pink'})),
 ('Step 2: The Effect on Later Earnings', UL('Before 2002, goodwill was <b>amortized</b> (up to 40 years).')
  + TB(['Each year', 'Purchase', 'Pooling'], [['Goodwill amortization', '$3', '$0']])
  + UL('Purchase method &rarr; lower reported earnings every year; pooling &rarr; none.')),
 ('Step 3: Today', UL(
   'SFAS 141 (2001) banned pooling: only the <b>acquisition (purchase) method</b> is allowed.',
   'SFAS 142 (2001) ended goodwill amortization; goodwill is tested for impairment instead.')),
 ('Back to the Letter', UL(
   'Buffett (1999): managers &ldquo;detest purchase accounting&rdquo; because it creates goodwill that is written off.',
   'The economics of the deal are the same under both methods; only the accounting differs.')),
]

# ---------------------------------------------------------------- Liabilities
D['Insurance float and loss reserves'] = [
 ('Step 1: Collect Premiums First', EX('An insurer collects $100 of premiums in advance for one year of coverage.')
  + JE(('Jan 1:', [('Cash (+A)', '100', None), ('Unearned Premiums (+L)', None, '100')]))
  + UL('Like deferred revenue (Ch10): cash now, revenue as coverage is provided.')),
 ('Step 2: Earn the Premium, Record Losses', JE(('Dec 31:', [('Unearned Premiums (' + M + 'L)', '100', None), ('Premium Revenue (+R)', None, '100')]),
       ('Dec 31:', [('Loss Expense (+E)', '95', None), ('Loss Reserve (+L)', None, '95')]))
  + UL('Claims of $95 are incurred but <b>not yet paid</b> &rarr; loss reserve (an estimate).')),
 ('Step 3: Underwriting Profit and Float', TB(['', 'Amount'], [['Premium revenue', '$100'], [M + ' Losses and expenses', '(95)'], ['Underwriting profit', '$5']], hl={2: 'yel'})
  + UL('<b>Float</b>: cash held until claims are paid; the insurer invests it meanwhile.',
       'Underwriting profit &rarr; float costs <b>nothing</b> to use.')),
 ('Back to the Letter', UL(
   'Buffett (2007): float &ldquo;funds $59 billion of our investments.&rdquo;',
   'Abel (2025): float stood at <b>$176 billion</b> at year-end.',
   'Loss reserves are estimates &rarr; a key audit area (ACC531).')),
]

D['Pension return assumptions'] = [
 ('Step 1: What Pension Expense Includes', UL('Pension expense = cost of benefits earned this year + interest on the obligation ' + M + ' <b>expected return</b> on plan assets.',
   'The expected return is an <b>assumption</b> chosen by management.')),
 ('Step 2: Change the Assumption', EX('Plan assets $1,000 million.')
  + TB(['Assumed return', 'Expected return', 'Effect on pension expense'], [['5%', '$50M', 'reduces expense by $50M'], ['8%', '$80M', 'reduces expense by $80M']], hl={1: 'pink'})
  + UL('8% instead of 5% &rarr; expense <b>$30 million lower</b>, earnings higher. Nothing real changed.')),
 ('Step 3: Is the Assumption Reasonable?', UL('Compare it with the plan&rsquo;s asset mix: bonds and cash cannot earn 8%.',
   'Auditors (ACC531): an <b>estimate</b> &rarr; test management&rsquo;s assumptions.')),
 ('Back to the Letter', UL(
   'Buffett (2007): the average S&amp;P 500 company assumed about 8% in 2006.',
   'About 28% of pension assets were bonds and cash, which could be expected to return no more than 5%.')),
]

D['Deferred tax liability'] = [
 ('Step 1: An Unrealized Gain', EX('Stocks bought for $500 are now worth $1,500. None sold.')
  + TB(['', 'Amount'], [['Fair value', '$1,500'], [M + ' Cost', '(500)'], ['Unrealized gain', '$1,000']], hl={2: 'pink'})),
 ('Step 2: Record the Tax That Would Be Owed', TB(['', 'Amount'], [['Unrealized gain', '$1,000'], ['&times; Tax rate', '21%'], ['Deferred tax liability', '$210']], hl={2: 'yel'})
  + JE(('Dec 31:', [('Income Tax Expense (+E)', '210', None), ('Deferred Tax Liability (+L)', None, '210')]))),
 ('Step 3: When Is It Paid?', UL('Only when the stocks are <b>sold</b> and the gain is realized.',
   'Until then: like an interest-free loan from the government that stays invested.')),
 ('Back to the Letter', UL(
   'Buffett (1989): the deferred tax liability works like a large transfer tax, payable only if Berkshire moves from one asset to another.',
   'It is a real liability, but its timing is under Berkshire&rsquo;s control.')),
]

# ---------------------------------------------------------------- Equity
D['Stock options are an expense'] = [
 ('Step 1: Grant-date Fair Value', UL('<b>Stock option</b>: the right to buy shares at a fixed price.', 'Its <b>fair value</b> at the grant date is estimated with a model.')
  + EX('Options worth $12 million granted Jan 1; they vest evenly over 4 years.')),
 ('Step 2: Expense over the Vesting Period', '<p>$12 &divide; 4 years = $3 million each year.</p>'
  + JE(('Dec 31:', [('Compensation Expense (+E)', '3', None), ('APIC (+SE)', None, '3')]))
  + UL('Net income &darr; $3; cash: no change.')),
 ('Step 3: Before and After 2006', TB(['', 'Before 2006', 'Since 2006'], [['Expense for options', 'Usually $0', '$3 per year'], ['Net income', 'Higher', 'Lower by $3']], hl={0: 'pink'})
  + UL('U.S. GAAP (SFAS 123R) has required option expensing since 2006.')),
 ('Back to the Letter', UL(
   'Buffett (1992): &ldquo;How many legs does a dog have if you call his tail a leg? Four.&rdquo;',
   'If options are not compensation, what are they? If compensation is not an expense, what is it?',
   'Buffett (2007): &ldquo;Decades of option-accounting nonsense have now been put to rest.&rdquo;')),
]

D['Stock options and share dilution'] = [
 ('Step 1: Options Add Shares', EX('400 million shares outstanding; employees exercise options for 12 million shares (3%).')
  + JE(('Exercise:', [('Cash (+A)', '120', None), ('Common Stock (+SE)', None, '12'), ('APIC (+SE)', None, '108')]))
  + '<p class="note">Exercise price $10 per share, par $1 (made-up numbers; $ millions).</p>'),
 ('Step 2: Same Cash Flow, More Shares', TB(['', 'Before', 'After'], [['Free cash flow', '$120M', '$120M'], ['Shares outstanding', '400M', '412M'],
       ['Free cash flow per share', '$0.300', '$0.291']], hl={2: 'yel'})
  + UL('<b>Dilution</b>: each existing share owns a smaller slice.')),
 ('Step 3: Set a Limit', UL('Bezos (2001): target net dilution from employee options of about <b>3% per year</b> over five years.',
   'Paying in stock saves cash today but costs owners in per-share value.')),
 ('Back to the Letter', UL(
   'Bezos (1997): weight compensation toward stock options rather than cash.',
   'Bezos (2001): &ldquo;Limiting share count means more cash flow per share and more long-term value for owners.&rdquo;')),
]

D['Share repurchases'] = [
 ('Step 1: Record the Buyback', EX('Buy back 50 shares for $20 each.')
  + JE(('Date:', [('Treasury Stock (+xSE, ' + M + 'SE)', '1,000', None), ('Cash (' + M + 'A)', None, '1,000')]))
  + UL('Assets &darr;, SE &darr;; no expense &rarr; net income unchanged.')),
 ('Step 2: Effect on EPS', TB(['', 'Before', 'After'], [['Net income', '$500', '$500'], ['Shares outstanding', '250', '200'], ['EPS', '$2.00', '$2.50']], hl={2: 'yel'})
  + UL('Fewer shares &rarr; higher EPS, even with the same profit.')),
 ('Step 3: Price vs. Value', TB(['Buyback price', 'Shareholders who stay'], [['Below intrinsic value', 'Gain'], ['Above intrinsic value', 'Lose']], hl={1: 'pink'})),
 ('Back to the Letter', UL(
   'Buffett (1999, 2011): buy back only when the stock sells <b>well below</b> intrinsic value, conservatively calculated.',
   'Abel (2025): the same rule: repurchases must enhance per-share value for continuing owners.')),
]

D['Book value vs. intrinsic value'] = [
 ('Step 1: Book Value per Share', TB(['', 'Amount'], [['Total stockholders&rsquo; equity', '$600M'], ['&divide; Shares outstanding', '2M'], ['Book value per share', '$300']], hl={2: 'yel'})
  + UL('Book value = assets ' + M + ' liabilities, as recorded on the balance sheet.')),
 ('Step 2: Why Value Can Differ from Book', UL('Assets are recorded at <b>historical cost</b>.', 'Internally built value (brands, customer loyalty) is <b>not recorded</b>.')
  + EX('Land bought in 1970 for $10 is worth $200 today; the balance sheet still shows $10.')),
 ('Step 3: Intrinsic Value', UL('<b>Intrinsic value</b>: the present value of the cash a business will produce in the future.',
   'An estimate, not a recorded number &rarr; two people can disagree.')),
 ('Back to the Letter', UL(
   'Buffett (1994): book value is &ldquo;a rough, albeit significantly understated, tracking measure&rdquo; of intrinsic value.',
   'Buffett (2018): book value &ldquo;has lost the relevance it once had&rdquo; &rarr; dropped as the headline measure.')),
]

# ---------------------------------------------------------------- Investments
D['Look-through earnings'] = [
 ('Step 1: What GAAP Records', EX('Berkshire owns 10% of a company that earns $500 million and pays $100 million of dividends.')
  + JE(('Dec 31:', [('Cash (+A)', '10', None), ('Dividend Revenue (+R)', None, '10')]))
  + UL('Under 20% ownership: Berkshire records only its <b>dividends</b> ($ millions).')),
 ('Step 2: Berkshire&rsquo;s Share of Retained Earnings', TB(['', '$ millions'], [['Investee net income', '$500'], [M + ' Dividends paid', '(100)'],
       ['Retained earnings', '$400'], ['Berkshire&rsquo;s 10% share', '$40']], hl={3: 'yel'})
  + UL('This $40 belongs to Berkshire but is <b>not</b> in its profit.')),
 ('Step 3: Look-through Earnings', TB(['', '$ millions'], [['Berkshire&rsquo;s reported operating earnings', '$1,000'],
       ['+ Share of investees&rsquo; retained earnings', '40'], [M + ' Tax if it were paid out', '(5)'], ['Look-through earnings', '$1,035']], hl={3: 'yel'})
  + '<p class="note">Operating earnings and tax are made-up numbers.</p>'),
 ('Back to the Letter', UL(
   'Buffett (1990&ndash;1994): GAAP leaves out investees&rsquo; retained earnings, which still work for Berkshire.',
   'Look-through earnings show the economic earnings of <b>everything</b> Berkshire owns.')),
]

D['Unrealized gains in net income'] = [
 ('Step 1: Stock Prices Rise, Nothing Sold', EX('Stocks held rise from $100 billion to $130 billion during the year.')
  + JE(('Dec 31:', [('Investments (+A)', '30B', None), ('Unrealized Gain (+Gain)', None, '30B')]))),
 ('Step 2: The Gain Goes into Net Income', UL('Since 2018 (ASU 2016-01): changes in the fair value of stocks held go into <b>net income</b>, sold or not.')
  + TB(['Quarter', 'Operating earnings', 'Investment gain (loss)', 'Net income'],
       [['Q1', '$10B', '$20B', '$30B'], ['Q2', '$11B', '($25B)', '($14B)']], hl={1: 'pink'})
  + '<p class="note">Made-up numbers.</p>'),
 ('Step 3: Separate the Two', UL('<b>Operating earnings</b>: profit from the businesses, without investment gains and losses.',
   'Net income now swings with the stock market &rarr; look at operating earnings for performance.')),
 ('Back to the Letter', UL(
   'Buffett (2017, 2018): the new rule will produce &ldquo;wild and capricious swings&rdquo; in the bottom line.',
   'Abel (2025): operating earnings of <b>$44.5 billion</b>; &ldquo;operating earnings remains the best measure.&rdquo;')),
]

D['Derivatives and mark-to-market'] = [
 ('Step 1: Fair Value Each Period', UL('<b>Derivative</b>: a contract whose value depends on something else (interest rates, stock prices, &hellip;).',
   'Recorded at <b>fair value</b>; changes go into earnings.')
  + EX('A contract is worth +$20 million at the start of the year and ' + M + '$15 million at year-end.')),
 ('Step 2: The Gain or Loss', TB(['', '$ millions'], [['Fair value, end of year', '(15)'], [M + ' Fair value, start of year', '(20)'], ['Loss for the year', '(35)']], hl={2: 'pink'})),
 ('Step 3: Where Does Fair Value Come From?', TB(['', 'Fair value from'], [['Traded on an exchange', 'Market price (mark-to-market)'], ['No active market', 'Management&rsquo;s model (mark-to-model)']], hl={1: 'pink'})
  + UL('Change one assumption &rarr; a different &ldquo;profit.&rdquo; Hard to audit (ACC531).')),
 ('Back to the Letter', UL(
   'Buffett (2002): mark-to-market &ldquo;turned out to be truly mark-to-myth&rdquo;; derivatives are &ldquo;financial weapons of mass destruction.&rdquo;',
   'Buffett (2008), after the financial crisis: &ldquo;Derivatives are dangerous.&rdquo;')),
]

# ---------------------------------------------------------------- Historical cost
D['Inflation and reported returns'] = [
 ('Step 1: Depreciation at Old Prices', EX('A machine bought 10 years ago for $100 (10-year life). A new one now costs $200.')
  + TB(['', 'Per year'], [['Depreciation recorded (historical cost)', '$10'], ['Cost to replace, spread over 10 years', '$20']], hl={0: 'pink'})),
 ('Step 2: Reported Profit Is Overstated', TB(['', 'Reported', 'At today&rsquo;s prices'], [['Profit before depreciation', '$50', '$50'], [M + ' Depreciation', '(10)', '(20)'], ['Profit', '$40', '$30']], hl={2: 'yel'})
  + UL('Same for inventory: cost of goods sold uses older, lower prices.')),
 ('Step 3: Real Return', TB(['', '%'], [['Return on equity', '12%'], [M + ' Inflation', '(10%)'], ['Real return (roughly)', '2%']], hl={2: 'yel'})),
 ('Back to the Letter', UL(
   'Buffett (1979&ndash;1981): with inflation above 10%, good-looking returns were &ldquo;illusory&rdquo; for owners.',
   'Historical cost: reliable, but it can mislead when prices change fast.')),
]

# ---------------------------------------------------------------- Audit
D['Audit committees and auditors'] = [
 ('Step 1: Who Does What', TB(['Party', 'Role'], [['Management', 'Prepares the financial statements'], ['External auditor', 'Gives an opinion on them'],
       ['Audit committee (board)', 'Appoints and oversees the auditor (SOX 2002)']], small=True)),
 ('Step 2: Buffett&rsquo;s Four Questions (1)', OL(
   'If the auditor were solely responsible for preparing the statements, would they have been prepared differently from management&rsquo;s way?',
   'If the auditor were an investor, would he have received, in plain English, the information essential to understanding the company&rsquo;s performance?')),
 ('Step 3: Buffett&rsquo;s Four Questions (2)', '<ol start="3" style="counter-reset:k 2">'
  + '<li>Is the company following the same internal audit procedure that would be followed if the auditor himself were CEO?</li>'
  + '<li>Is the auditor aware of any actions that moved revenues or expenses from one reporting period to another?</li></ol>'
  + UL('Ask them at least a week before the earnings release.')),
 ('Back to the Letter', UL(
   'Buffett (2002): &ldquo;Audit committees can&rsquo;t audit.&rdquo;',
   'Their key job: get the auditors to <b>divulge what they know</b>.',
   'Buffett (1998): &ldquo;at times I have been amazed by the numbers that big-name auditors have implicitly blessed.&rdquo;')),
]
