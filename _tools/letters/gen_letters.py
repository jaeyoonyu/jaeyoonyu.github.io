#!/usr/bin/env python3
"""Shareholder letters (Berkshire Hathaway, Amazon): accounting themes page, a question sheet + key
and a reading packet (summary + relevant excerpts) per theme, all sorted by topic.

Usage (from the repo root): python _tools/letters/gen_letters.py [BRK_TXT_DIR AMZN_TXT_DIR]
  BRK_TXT_DIR / AMZN_TXT_DIR hold <year>.txt, the plain text of each letter (only needed for the readings).
Writes assets/Letters/Qnn.html, Rnn.html and shareholder-letters.md. Print the HTML to PDF separately,
then run this again so the page's ?v= hashes match the PDFs.
"""
import os, re, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'assets', 'Letters')
os.makedirs(OUT, exist_ok=True)


def brk_url(y):
    y = int(y)
    if y <= 1997: return f'https://www.berkshirehathaway.com/letters/{y}.html'
    special = {1998: '1998pdf.pdf', 1999: 'final1999pdf.pdf', 2000: '2000pdf.pdf', 2001: '2001pdf.pdf', 2002: '2002pdf.pdf'}
    return 'https://www.berkshirehathaway.com/letters/' + special.get(y, f'{y}ltr.pdf')


AQ = 'https://s2.q4cdn.com/299287126/files/doc_financials/'
AMZN_URL = {1997: 'annual/Shareholderletter97.pdf', 1998: 'annual/Shareholderletter98.pdf', 1999: 'annual/Shareholderletter99.pdf',
            2000: 'annual/00ar_letter.pdf', 2001: 'annual/2001_shareholderLetter.pdf', 2002: 'annual/2002_shareholderLetter.pdf',
            2004: 'annual/2004_shareholderLetter.pdf', 2023: '2024/ar/Amazon-com-Inc-2023-Shareholder-Letter.pdf',
            2024: 'https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-2024-letter-to-shareholders',
            2025: '2026/ar/2025-Shareholder-Letter-Final.pdf'}


def amzn_url(y):
    u = AMZN_URL[int(y)]
    return u if u.startswith('http') else AQ + u


CO = {
 'B': dict(name='Berkshire', url=brk_url, site='berkshirehathaway.com/letters', owner='Berkshire Hathaway Inc.',
           who=lambda ys: 'Warren E. Buffett' + ('; 2025 letter by Greg Abel' if 2025 in ys else ''),
           title='Letters to Berkshire Hathaway Shareholders'),
 'A': dict(name='Amazon', url=amzn_url, site='ir.aboutamazon.com', owner='Amazon.com, Inc.',
           who=lambda ys: '; '.join(n for n, ok in (('Jeffrey P. Bezos', min(ys) <= 2020), ('Andrew R. Jassy', max(ys) >= 2021)) if ok),
           title='Letters to Amazon.com Shareholders'),
}

# theme, key letters (main first), difficulty, ACC250, ACC531, quote, questions
# question: ('mc', stem, [options], index of answer) or ('num', stem, answer)
BRK = [
 ('Economic vs. accounting goodwill', [1983, 1999, 2015], 'Intermediate', 'Ch9', '',
  'We own several businesses that possess economic Goodwill ... far larger than the accounting Goodwill that is carried on our balance sheet. (1983)',
  [('num', 'A company pays $500 million for another company whose identifiable net assets have a fair value of $380 million. How much goodwill does it record ($ millions)?', '120'),
   ('mc', 'Why can a business&rsquo;s economic goodwill be far larger than the goodwill on its balance sheet?',
    ['Goodwill is recorded only when a business is purchased; goodwill a company builds internally is never recorded', 'Goodwill is always amortized to zero within one year', 'Auditors require goodwill to be recorded at half its value', 'Goodwill is a liability, not an asset'], 0)]),
 ('Owner earnings', [1986], 'Intermediate', 'Ch9', '',
  'We consider the owner earnings figure, not the GAAP figure, to be the relevant item for valuation purposes. (1986)',
  [('num', 'Net income is $100, depreciation and amortization are $40, and the capital spending needed just to maintain the business is $50. What are owner earnings (net income + D&amp;A &minus; maintenance capital spending)?', '90'),
   ('mc', 'Compared with EBITDA, owner earnings&hellip;',
    ['subtracts the capital spending needed to keep the business running', 'ignores depreciation', 'adds back income taxes', 'is always larger'], 0)]),
 ('Look-through earnings', [1990, 1991, 1992], 'Advanced', '', '',
  'The retained operating earnings of major investees that, under GAAP accounting, are not reflected in our profits. (1991)',
  [('num', 'Berkshire owns 10% of a company that earns $500 million and pays $100 million of dividends. Berkshire records only its dividends as income. Before taxes, how much of the investee&rsquo;s retained earnings belongs to Berkshire but is not in its profit ($ millions)?', '40'),
   ('mc', 'Look-through earnings add which item to Berkshire&rsquo;s reported operating earnings?',
    ['Berkshire&rsquo;s share of investees&rsquo; retained earnings, less the tax that would be paid if distributed', 'The market value of all stocks owned', 'Insurance float', 'Dividends received'], 0)]),
 ('Stock options are an expense', [1992, 1998, 2007], 'Intro', 'Ch11', '',
  'How many legs does a dog have if you call his tail a leg? Four, because calling a tail a leg does not make it a leg. (1992)',
  [('num', 'A company grants employees options with a total fair value of $12 million that vest evenly over 4 years. How much compensation expense does it record each year ($ millions)?', '3'),
   ('mc', 'Recording stock-option compensation expense&hellip;',
    ['lowers net income but uses no cash', 'lowers cash and net income', 'raises net income', 'affects only the cash flow statement'], 0)]),
 ('Earnings management', [1998, 1992, 2000], 'Intermediate', '', 'Fraud risk',
  'The distortion du jour is the &ldquo;restructuring charge,&rdquo; an accounting entry that ... too often is a device for manipulating earnings. (1998)',
  [('mc', 'A company books an unusually large restructuring charge in a bad year (a &ldquo;big bath&rdquo;). What does this most likely do to the following years&rsquo; reported earnings?',
    ['Makes them look better, because future costs were charged early', 'Makes them look worse', 'Has no effect', 'Eliminates all future expenses'], 0),
   ('mc', 'Buffett writes, &ldquo;We prefer a lumpy 15% return to a smooth 12%.&rdquo; Why should an auditor be skeptical of very smooth earnings?',
    ['Smoothness can come from adjusting estimates and reserves rather than from the business', 'Smooth earnings are illegal under GAAP', 'Auditors cannot audit smooth earnings', 'Smooth earnings mean no taxes are paid'], 0)]),
 ('EBITDA ignores a real cost', [2000, 2002], 'Intro', 'Ch9', '',
  'References to EBITDA make us shudder &mdash; does management think the tooth fairy pays for capital expenditures? (2000)',
  [('num', 'Net income $50, interest $10, income taxes $20, depreciation and amortization $30. What is EBITDA?', '110'),
   ('mc', 'Why does Buffett call depreciation a real cost even though it is a &ldquo;non-cash&rdquo; expense?',
    ['The cash was paid up front when the asset was bought', 'Depreciation is paid in cash every year', 'Depreciation increases taxes owed', 'Depreciation is a liability'], 0)]),
 ('Purchase vs. pooling for acquisitions', [1999, 2000], 'Advanced', '', '',
  'Managements usually detest purchase accounting because it almost always requires that a &ldquo;goodwill&rdquo; account be established and subsequently written off. (1999)',
  [('mc', 'Which method must U.S. companies use today to record an acquisition?',
    ['The acquisition (purchase) method: assets and liabilities at fair value, the excess as goodwill', 'Pooling of interests', 'Either method, at management&rsquo;s choice', 'No entry until the target is sold'], 0),
   ('mc', 'Why did many managers prefer pooling?',
    ['No goodwill was created, so there was no later charge against earnings', 'It required more disclosure', 'It raised income taxes', 'It recorded assets at fair value'], 0)]),
 ('Derivatives and mark-to-market', [2002, 2008], 'Advanced', '', 'Fair value',
  '&ldquo;Mark-to-market&rdquo; then turned out to be truly &ldquo;mark-to-myth.&rdquo; ... Derivatives are financial weapons of mass destruction. (2002)',
  [('num', 'A derivative contract had a fair value of +$20 million at the start of the year and &minus;$15 million at year-end. What gain (loss) is reported for the year ($ millions; use a minus sign for a loss)?', '&minus;35'),
   ('mc', 'Why are many derivatives hard to audit?',
    ['With no active market, fair value comes from management&rsquo;s models and assumptions', 'Derivatives are never recorded on the balance sheet', 'They are always worth zero', 'They are recorded at historical cost'], 0)]),
 ('Audit committees and auditors', [2002, 1998], 'Intermediate', '', 'Governance',
  'Audit committees can&rsquo;t audit. ... The key job of the audit committee is simply to get the auditors to divulge what they know. (2002)',
  [('mc', 'Under the Sarbanes-Oxley Act, who appoints and oversees a public company&rsquo;s external auditor?',
    ['The audit committee of the board', 'The CEO', 'The CFO', 'The SEC'], 0),
   ('mc', 'Buffett suggests the audit committee ask the auditor whether the financial statements would differ if the auditor had prepared them alone. What is the main purpose of such questions?',
    ['To make auditors share their concerns about management&rsquo;s accounting choices', 'To lower the audit fee', 'To replace the internal audit function', 'To prepare the tax return'], 0)]),
 ('Pension return assumptions', [2007, 2016], 'Advanced', '', 'Estimates',
  'Other accounting choices remain &ndash; important among these the investment-return assumption a company uses in calculating pension expense. (2007)',
  [('num', 'Pension plan assets are $1,000 million. If the company assumes an 8% expected return instead of 5%, by how much does reported pension expense fall ($ millions)?', '30'),
   ('mc', 'A higher assumed return on pension assets&hellip;',
    ['lowers pension expense and raises reported earnings', 'raises pension expense', 'has no effect on earnings', 'increases the cash paid to retirees'], 0)]),
 ('Insurance float and loss reserves', [2007, 2011, 2014, 2025], 'Intermediate', 'Ch10', 'Estimates',
  'Insurance float &ndash; money we temporarily hold in our insurance operations that does not belong to us &ndash; funds $59 billion of our investments. (2007)',
  [('num', 'An insurer collects $100 million of premiums and incurs $95 million of losses and expenses. What is its underwriting profit ($ millions)?', '5'),
   ('mc', 'On the balance sheet, insurance float appears mainly as&hellip;',
    ['liabilities (loss reserves and unearned premiums)', 'revenue', 'stockholders&rsquo; equity', 'goodwill'], 0)]),
 ('Deferred tax liability', [1989, 1986], 'Intermediate', '', '',
  'In effect, this deferred tax liability is equivalent to a very large transfer tax that is payable only if we elect to move from one asset to another. (1989)',
  [('num', 'Berkshire holds stocks with an unrealized gain of $1,000 million. At a 21% tax rate, what deferred tax liability is recorded ($ millions)?', '210'),
   ('mc', 'When would that deferred tax actually be paid?',
    ['When the stocks are sold and the gain is realized', 'Every year', 'Never', 'When dividends are received'], 0)]),
 ('Book value vs. intrinsic value', [1992, 1994, 2018], 'Intro', 'Ch2, Ch11', '',
  'The annual change in Berkshire&rsquo;s book value ... is a metric that has lost the relevance it once had. (2018)',
  [('num', 'Total stockholders&rsquo; equity is $600 million and 2 million shares are outstanding. What is book value per share ($)?', '300'),
   ('mc', 'Why can intrinsic value be far above book value?',
    ['Assets are mostly recorded at historical cost, and internally built value (brands, goodwill) is not recorded', 'Book value includes market prices of all assets', 'Liabilities are ignored in book value', 'Book value is measured in future dollars'], 0)]),
 ('Unrealized gains in net income', [2017, 2018, 2024, 2025], 'Intermediate', 'Ch3', 'Analytics',
  'The new rule says that the net change in unrealized investment gains and losses in stocks we hold must be included in all net income figures we report to you. (2017)',
  [('num', 'Stocks Berkshire holds rose from $100 billion to $130 billion during the year, and none were sold. Under the current rule, what pre-tax gain is included in net income ($ billions)?', '30'),
   ('mc', 'Which measure does Buffett tell shareholders to focus on instead?',
    ['Operating earnings, which exclude investment gains and losses', 'EBITDA', 'Revenue', 'Total comprehensive income'], 0)]),
 ('"Adjusted" earnings', [2016], 'Intro', 'Ch3', '',
  'Too many managements ... are looking for any means to report, and indeed feature, &ldquo;adjusted earnings&rdquo; that are higher than their company&rsquo;s GAAP earnings. (2016)',
  [('num', 'GAAP net income is $80 million. Management adds back $15 million of stock-based compensation and $10 million of amortization. What &ldquo;adjusted earnings&rdquo; does it report ($ millions)?', '105'),
   ('mc', 'Which add-back does Buffett argue is clearly a real cost?',
    ['Stock-based compensation', 'Income tax refund', 'Gain on sale of land', 'Dividends paid'], 0)]),
 ('Share repurchases', [1999, 2011, 2016, 2025], 'Intro', 'Ch11', '',
  'We will not repurchase shares unless we believe Berkshire stock is selling well below intrinsic value, conservatively calculated. (1999)',
  [('num', 'Net income is $500 and 250 shares are outstanding. The company buys back 50 shares. What is EPS after the buyback ($)?', '2.50'),
   ('mc', 'Which account is debited when a company buys back its own shares?',
    ['Treasury Stock (contra-equity)', 'Cash', 'Retained Earnings', 'Common Stock expense'], 0)]),
 ('Inflation and reported returns', [1979, 1980, 1981], 'Advanced', '', '',
  'In past reports we have explained how inflation has caused our apparently satisfactory long-term corporate performance to be illusory as a measure of true investment results for our owners. (1981)',
  [('num', 'A company earns a 12% return on equity while inflation is 10%. Roughly what is the real (inflation-adjusted) return, in %?', '2'),
   ('mc', 'Why do historical-cost financial statements overstate earnings when prices rise?',
    ['Depreciation and cost of goods sold are based on older, lower prices', 'Revenue is recorded at old prices', 'Assets are marked to market', 'Taxes are ignored'], 0)]),
]

# keyword pattern used to pick passages, and a plain-English summary, per theme (same order as T)
BRK_K = [
 (r'goodwill', 'When one company buys another for more than the fair value of its identifiable net assets, the excess is recorded as goodwill. Buffett separates this <b>accounting goodwill</b> from <b>economic goodwill</b>: the ability of a great business to earn high returns on its tangible assets. Economic goodwill that a company builds itself never appears on its balance sheet, so book value can understate what a business is worth.'),
 (r'owner earnings|capitalized expenditures|non-cash charges', '<b>Owner earnings</b> = reported earnings + depreciation, depletion, amortization and other non-cash charges &minus; the capital spending needed to keep the business competitive. Buffett argues this, not GAAP earnings, is what matters for valuing a business, because some non-cash charges are not real costs while maintenance capital spending is.'),
 (r'look-through', 'Under GAAP, Berkshire reports only the dividends from companies it owns less than 20% of, so its share of their <b>retained earnings</b> never shows up in Berkshire&rsquo;s profit. <b>Look-through earnings</b> add that share back (less the tax that would be due if it were paid out) to show the economic earnings of everything Berkshire owns.'),
 (r'option', 'For years, companies did not record an expense when they paid employees with <b>stock options</b>. Buffett argues options are compensation, compensation is an expense, and an expense belongs in net income, even when its exact amount is hard to estimate. U.S. GAAP has required option expensing since 2006.'),
 (r'restructuring|smooth|manipulat|managed earnings|big bath|cookie', 'Buffett warns against <b>managing earnings</b>: booking oversized &ldquo;restructuring charges&rdquo; (a &ldquo;big bath&rdquo;) so later years look better, or adjusting estimates to make results smooth. He prefers honest, lumpy results. For auditors, unusually smooth earnings and large one-time charges are signals of possible manipulation.'),
 (r'EBITDA|depreciation', '<b>EBITDA</b> (earnings before interest, taxes, depreciation and amortization) leaves out depreciation as if it were not a real cost. Buffett points out that the cash for plant and equipment is paid up front, before the assets produce anything, so depreciation is a very real expense.'),
 (r'pooling|purchase accounting|purchase-accounting', 'Until 2001, U.S. GAAP allowed two methods for acquisitions. <b>Pooling</b> combined the two companies&rsquo; book values and created no goodwill; the <b>purchase</b> method recorded assets at fair value and created goodwill that was then amortized against earnings. Managers favored pooling to avoid those charges. Today only the purchase (acquisition) method is allowed.'),
 (r'derivative|mark-to-market|mark-to-model', 'Many <b>derivatives</b> have no market price, so their fair value is estimated with models. Buffett shows how traders and companies booked large &ldquo;earnings&rdquo; from optimistic estimates (&ldquo;mark-to-myth&rdquo;) that later vanished, and calls derivatives &ldquo;financial weapons of mass destruction.&rdquo;'),
 (r'audit committee|auditor', 'Buffett says <b>audit committees can&rsquo;t audit</b>; their job is to get the external auditors to tell them what they know. He proposes four questions the committee should ask the auditors, starting with whether the statements would differ if the auditor alone had prepared them.'),
 (r'pension', 'Pension expense depends on the <b>assumed return</b> on pension assets. A higher assumption lowers reported expense and raises earnings, with no change in the plan&rsquo;s real economics. Buffett shows that many companies used assumptions (about 8%) that their actual asset mix could not support.'),
 (r'\bfloat\b', 'Insurers collect premiums before they pay claims. The money held in between, <b>float</b>, appears on the balance sheet as liabilities (loss reserves and unearned premiums), but if the insurer earns an underwriting profit, it is money that costs nothing to use. Berkshire invests its float.'),
 (r'deferred tax', 'When stocks rise in value, Berkshire records a <b>deferred tax liability</b> for the tax that would be owed if they were sold. Buffett explains that this liability is real, but it is paid only when a gain is realized, so it works like an interest-free loan from the government.'),
 (r'book value|intrinsic value', '<b>Book value</b> is what the balance sheet says shareholders&rsquo; equity is; <b>intrinsic value</b> is the discounted value of the cash a business will produce. Because assets are recorded at historical cost and internally built value is not recorded, the two can differ widely. In 2018 Buffett stopped using book value as Berkshire&rsquo;s headline measure.'),
 (r'unrealized|new rule|GAAP rule|operating earnings', 'Since 2018, U.S. GAAP requires changes in the market value of stocks a company holds to be reported in <b>net income</b>, even if nothing is sold. For Berkshire this makes net income swing by billions each quarter. Buffett tells shareholders to focus on <b>operating earnings</b>, which leave these gains and losses out.'),
 (r'adjusted|stock-based|compensation|real cost', 'Many companies feature <b>&ldquo;adjusted&rdquo; earnings</b> that leave out costs such as stock-based compensation or restructuring. Buffett argues these are real costs, and that excluding them makes performance look better than it is.'),
 (r'repurchas|buy ?back', 'A <b>share repurchase</b> helps the shareholders who stay only if the price paid is below the company&rsquo;s intrinsic value. Buffett explains Berkshire&rsquo;s rule: buy back shares only when they are clearly cheap, and only with cash not needed for the business.'),
 (r'inflation', 'In the late 1970s and early 1980s, inflation ran above 10%. Financial statements built on <b>historical cost</b> overstated real earnings, because depreciation and inventory costs were based on old, lower prices. Buffett explains why a business earning a respectable return on equity could still give its owners little or no real return.'),
]

AMZN = [
 ('GAAP earnings vs. cash flows', [1997, 2001], 'Intro', 'Ch1, Ch3', '',
  'When forced to choose between optimizing the appearance of our GAAP accounting and maximizing the present value of future cash flows, we&rsquo;ll take the cash flows. (1997)',
  [('num', 'Net income is $25 million. The company recorded $40 million of depreciation and paid $60 million in cash for new equipment. Ignoring everything else, by how much did cash change ($ millions; use a minus sign for a decrease)?', '5'),
   ('mc', 'Why can GAAP net income differ from the cash a company generates?',
    ['Accrual accounting records revenues when earned and expenses when incurred, not when cash is received or paid', 'GAAP ignores revenue earned on account', 'Net income always equals cash flow', 'Cash flows include only income taxes'], 0)]),
 ('Free cash flow per share', [2004, 2002, 2001], 'Intro', 'Ch9', 'Analytics',
  'Our ultimate financial measure, and the one we most want to drive over the long-term, is free cash flow per share. (2004)',
  [('num', 'In 2002 Amazon&rsquo;s net cash provided by operating activities was $174 million and its purchases of fixed assets were $39 million (2002 letter). What was its free cash flow ($ millions)?', '135'),
   ('mc', 'Why does Bezos focus on free cash flow rather than earnings?',
    ['Earnings do not directly turn into cash: capital spending, working capital and new shares also matter', 'Earnings are not audited', 'Free cash flow is required by GAAP to be the headline number', 'Free cash flow ignores capital spending'], 0)]),
 ('Growing earnings, negative free cash flow', [2004], 'Intermediate', 'Ch9', 'Analytics',
  'Though some may find it counterintuitive, a company can actually impair shareholder value in certain circumstances by growing earnings. (2004)',
  [('num', 'In Bezos&rsquo;s example (in thousands), Year 1 earnings are $10,000, depreciation is $40,000 and there is no working capital change. Capital expenditures are $160,000. What is free cash flow (operating cash flow &minus; capital expenditures; use a minus sign if negative)?', '&minus;110,000'),
   ('mc', 'In the example, earnings double every year while free cash flow is negative every year. Why?',
    ['The business pays cash for new machines up front, more than its operating cash flow, while depreciation spreads their cost over many years', 'Revenue is recorded before it is earned', 'Depreciation is paid in cash each year', 'The business pays no income taxes'], 0)]),
 ('Capex, useful lives and free cash flow', [2025], 'Intro', 'Ch9', 'Estimates',
  'However, these capex investments fund assets with many-year useful lives (30+ years for datacenters; 5-6 years for chips, servers, and networking gear). (2025)',
  [('num', 'A company pays $30 billion in cash for datacenters with a 30-year useful life (straight-line, no salvage value). How much depreciation expense does it record in the first full year ($ billions)?', '1'),
   ('mc', 'In the year it pays for those datacenters, by how much does the $30 billion purchase reduce free cash flow?',
    ['$30 billion, the full purchase', '$1 billion, the depreciation', '$0, because it is an asset', '$15 billion, half the cost'], 0)]),
 ('Pro forma results', [2000, 2001], 'Intro', 'Ch3', 'Fraud risk',
  'As I mentioned, we exceeded our goals for the fourth quarter with pro forma operating profit of $59 million and pro forma net profit of $35 million. (2001)',
  [('num', 'A company&rsquo;s GAAP operating loss is $20 million. Its pro forma figure leaves out $50 million of stock-based compensation and goodwill amortization. What pro forma operating profit does it report ($ millions)?', '30'),
   ('mc', 'Which statement about pro forma (non-GAAP) results is true?',
    ['GAAP does not define them, so the company chooses what to leave out', 'They must be audited the same way as GAAP results', 'They always equal GAAP net income', 'They include every expense GAAP requires'], 0)]),
 ('Operating income and segments', [2024, 2023], 'Intro', 'Ch3', 'Analytics',
  'Amazon&rsquo;s operating income in 2024 improved 86% YoY, from $36.9B (an operating margin of 6.4%) to $68.6B (an operating margin of 10.8%). (2024)',
  [('num', 'In 2024 Amazon&rsquo;s revenue was $638 billion and its operating income was $68.6 billion (2024 letter). What was its operating margin (%, one decimal)?', '10.8'),
   ('mc', 'Amazon reports three segments: North America, International and AWS. Why do segment results matter to readers?',
    ['They show which parts of the business produce the revenue and operating income', 'They replace the income statement', 'They are used only for income taxes', 'They report each segment&rsquo;s share price'], 0)]),
 ('Fixed costs and operating leverage', [2002, 2001], 'Intermediate', 'Ch3', 'Analytics',
  'With customer experience costs largely fixed (more like a publishing model than a retailing model), our costs as a percentage of sales can shrink rapidly as we grow our business. (2002)',
  [('num', 'Fixed costs are $100 million. Sales grow from $500 million to $1,000 million and fixed costs stay the same. Fixed costs as a percent of sales fall from 20% to what percent?', '10'),
   ('mc', 'When most of a company&rsquo;s costs are fixed, as sales grow&hellip;',
    ['operating income grows faster than sales', 'operating income grows slower than sales', 'costs grow faster than sales', 'the operating margin falls'], 0)]),
 ('Operating cycle and inventory turnover', [2004, 2002, 1999], 'Intermediate', 'Ch6, Ch8', 'Analytics',
  'We have a cash generative operating cycle because we turn our inventory quickly, collecting payments from our customers before payments are due to suppliers. (2004)',
  [('num', 'Days of sales in inventory are 20, days of sales in accounts receivable are 5 and accounts payable days are 50. Using the letter&rsquo;s definition (inventory days + receivable days &minus; payable days), what is the operating cycle (days; use a minus sign if negative)?', '&minus;25'),
   ('mc', 'What does a negative operating cycle mean for Amazon?',
    ['It collects cash from customers before it pays its suppliers', 'It pays suppliers before it receives the goods', 'Its inventory never sells', 'Its accounts receivable are uncollectible'], 0)]),
 ('Stock options and share dilution', [2001, 1997], 'Intro', 'Ch11', '',
  'Limiting share count means more cash flow per share and more long-term value for owners. (2001)',
  [('num', 'A company has 400 million shares outstanding and targets net dilution from employee stock options of 3% this year. How many new shares does that add (millions)?', '12'),
   ('mc', 'If free cash flow stays the same and the number of shares rises, free cash flow per share&hellip;',
    ['falls', 'rises', 'stays the same', 'doubles'], 0)]),
]

AMZN_K = [
 (r'GAAP|cash flow', 'Accrual (GAAP) accounting records revenues when they are earned and expenses when they are incurred, so net income and cash flow can differ a lot. In his first letter, Bezos told shareholders that when the two conflict, Amazon would choose what maximizes future <b>cash flows</b> over what makes its <b>GAAP earnings</b> look better. In 2001 he explained why: a share of stock is worth the company&rsquo;s future cash flows.'),
 (r'free cash flow|per share|earnings don', '<b>Free cash flow</b> = net cash from operating activities &minus; purchases of fixed assets (capital expenditures). Bezos calls <b>free cash flow per share</b> Amazon&rsquo;s ultimate financial measure because earnings do not turn directly into cash: working capital, capital spending and new shares also matter.'),
 (r'EBITDA|depreciation|capital expenditure|growing earnings|free cash flow', 'Bezos&rsquo;s example business buys machines to grow. Its earnings double every year, but it must pay for more machines than its operating cash flow covers, so its <b>free cash flow</b> is negative every year. Earnings (and <b>EBITDA</b>) look healthy only because depreciation spreads each machine&rsquo;s cost over its life, while the cash is paid up front.'),
 (r'capex|useful li|FCF', '<b>Capital expenditures</b> (capex) are recorded as assets and expensed through depreciation over their <b>useful lives</b> (30+ years for datacenters; 5&ndash;6 years for chips and servers). The cash is paid up front, so when capex grows faster than revenue, free cash flow falls even while net income holds up. Jassy explains why Amazon accepts this to build AI capacity.'),
 (r'pro forma', 'In 2000&ndash;2001 Amazon featured <b>pro forma</b> results, which left out items such as stock-based compensation, goodwill amortization and restructuring charges. Pro forma (non-GAAP) numbers are not defined by GAAP, so the company chooses what to leave out; readers should always compare them with the GAAP figures.'),
 (r'operating income|operating margin|by segment|AWS revenue', '<b>Operating margin</b> = operating income &divide; revenue. Jassy&rsquo;s letters report revenue for Amazon&rsquo;s three <b>segments</b> (North America, International and AWS) and show operating margin rising from 2.4% in 2022 to 6.4% in 2023 and 10.8% in 2024.'),
 (r'fixed (cost|expense)|as a percentage of sales|cost leverage', 'When most costs are <b>fixed</b>, they shrink as a percent of sales as the business grows, so operating income grows faster than sales (<b>operating leverage</b>). Bezos explains that Amazon&rsquo;s software and customer-experience costs are largely fixed, &ldquo;more like a publishing model than a retailing model.&rdquo;'),
 (r'operating cycle|inventor|suppliers|working capital', 'The <b>operating cycle</b> measures how long cash is tied up in operations: days of inventory + days of receivables &minus; days of payables. Amazon sells its inventory quickly and collects from customers before it pays suppliers, so its cycle is negative and its suppliers in effect finance its growth.'),
 (r'dilution|share count|stock option|shares outstanding', 'Paying employees with <b>stock options</b> saves cash but adds shares. <b>Dilution</b> spreads the same cash flow over more shares, so value per share falls. In 2001 Bezos set a target for net dilution from employee options of about 3% per year.'),
]

# display order: (topic, company, index in that company's list)
TOPICS = [
 ('Cash flow', [('A', 0), ('A', 1), ('B', 1), ('B', 5), ('A', 2), ('A', 3)]),
 ('Non-GAAP', [('B', 14), ('A', 4), ('B', 4)]),
 ('Performance', [('A', 5), ('A', 6), ('A', 7)]),
 ('Assets', [('B', 0), ('B', 6)]),
 ('Liabilities', [('B', 10), ('B', 9), ('B', 11)]),
 ('Equity', [('B', 3), ('A', 8), ('B', 15), ('B', 12)]),
 ('Investments', [('B', 2), ('B', 13), ('B', 7)]),
 ('Historical cost', [('B', 16)]),
 ('Audit', [('B', 8)]),
]

CSS = '''*{box-sizing:border-box}html{background:#e9ecea}body{margin:0;font:11pt/1.4 "Times New Roman",Times,serif;color:#000}
.page{width:8.5in;height:11in;margin:18px auto;background:#fff;padding:.6in .7in;position:relative;box-shadow:0 6px 24px rgba(0,0,0,.15)}
header{display:flex;justify-content:space-between;border-bottom:1.2pt solid #000;padding-bottom:3pt;margin-bottom:10pt;font:700 9pt Arial,sans-serif}
header .n span{display:inline-block;width:2.2in;border-bottom:.8pt solid #000}
h1{font-size:16pt;margin:0 0 4pt}.meta{font-size:10pt;margin:0 0 10pt}
.q{border:.8pt solid #e57373;border-radius:8pt;padding:8pt 12pt;font-size:10.5pt;font-style:italic;margin:0 0 14pt}
ol.qs{padding-left:18pt;margin:0}ol.qs>li{margin:0 0 22pt}
ol.op{list-style:upper-alpha;margin:6pt 0 0;padding-left:20pt}ol.op li{margin:3pt 0}
.ans{display:inline-block;min-width:1.4in;border-bottom:.9pt solid #000;text-align:right;margin-left:8pt}
.ans::after{content:"\\00a0"}html.key .ans::after{content:attr(data-a);color:#b3200f;font-weight:700}
html.key li.r{color:#b3200f;font-weight:700}
.keytag{display:none;color:#b3200f}html.key .keytag{display:inline}
.src{position:absolute;left:.7in;right:.7in;bottom:.45in;font-size:9pt;border-top:.6pt solid #000;padding-top:3pt}
.src a{color:#000}
.bar{position:sticky;top:0;display:flex;gap:10px;justify-content:center;padding:10px;background:#16263a}
.bar button{font:600 13px Arial,sans-serif;padding:7px 16px;border-radius:6px;border:0;background:#fff;cursor:pointer}
@media print{@page{size:letter;margin:0}html{background:#fff}.bar{display:none}.page{margin:0;box-shadow:none}}'''

LISTS = {'B': (BRK, BRK_K), 'A': (AMZN, AMZN_K)}
THEMES = []
for topic, refs in TOPICS:
    for co, k in refs:
        t, kk = LISTS[co][0][k], LISTS[co][1][k]
        THEMES.append(dict(topic=topic, co=co, theme=t[0], years=t[1], diff=t[2], a250=t[3], a531=t[4],
                           quote=t[5], qs=t[6], rx=kk[0], summary=kk[1]))
assert sorted((c, k) for _, r in TOPICS for c, k in r) == sorted([('B', i) for i in range(len(BRK))] + [('A', i) for i in range(len(AMZN))])


def source(th, what):
    c = CO[th['co']]
    links = ', '.join(f'<a href="{c["url"](y)}">{y}</a>' for y in th['years'])
    return (f'Source: {c["who"](th["years"])}, {c["title"]}: {links} ({c["site"]}). '
            f'{what} &copy; {c["owner"]}, all rights reserved; reproduced in part for non-commercial teaching.')


for i, th in enumerate(THEMES, 1):
    items = []
    for qn, q in enumerate(th['qs']):
        if q[0] == 'mc':   # rotate options so the correct letter varies across sheets
            r = (i * 2 + qn * 3) % 4
            opts = q[2][r:] + q[2][:r]
            q = ('mc', q[1], opts, (q[3] - r) % 4)
        if q[0] == 'num':
            items.append(f'<li>{q[1]}<span class="ans" data-a="{q[2]}"></span></li>')
        else:
            ops = ''.join(f'<li{" class=\"r\"" if k == q[3] else ""}>{o}</li>' for k, o in enumerate(q[2]))
            items.append(f'<li>{q[1]}<ol class="op">{ops}</ol></li>')
    m = re.match(r'(.*) \((.*)\)$', th['quote'])
    qt = f'&ldquo;{m.group(1)}&rdquo; ({m.group(2)})'
    name = CO[th['co']]['name']
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shareholder Letters Q{i}</title><style>{CSS}</style></head><body>
<div class="bar"><button onclick="document.documentElement.classList.toggle('key')">Show/hide answers</button><button onclick="print()">Print</button></div>
<div class="page">
<header><span>Shareholder Letters &middot; Accounting Theme {i}<span class="keytag"> &middot; Answer key</span></span><span class="n">Name <span></span></span></header>
<h1>{th['theme']}</h1>
<p class="meta">{name} letters: {', '.join(str(y) for y in th['years'])} &middot; Difficulty: {th['diff']}</p>
<div class="q">{qt}</div>
<ol class="qs">{''.join(items)}</ol>
<p class="src">{source(th, 'Quotation')} Numbers in the questions are made up unless stated.</p>
</div><script>if(location.hash==='#key')document.documentElement.classList.add('key')</script></body></html>'''
    open(os.path.join(OUT, f'Q{i:02d}.html'), 'w').write(html)
print('wrote', len(THEMES), 'question sheets')

# ---------- reading packets ----------
RCSS = CSS + '''.page{height:auto;min-height:11in}.sum{border:.8pt solid #e57373;border-radius:8pt;padding:8pt 12pt;margin:0 0 12pt;font-size:11pt}
.sum b.t{display:block;font:700 9pt Arial,sans-serif;margin-bottom:2pt}h2{font:700 11pt Arial,sans-serif;margin:12pt 0 4pt;border-bottom:.8pt solid #000;padding-bottom:2pt}
p.ex{margin:0 0 6pt;font-size:10.5pt;text-align:justify}p.gap{text-align:center;margin:0 0 6pt;color:#555}
.src{position:static;margin-top:14pt}
table.lt{border-collapse:collapse;margin:4pt auto 8pt;font-size:10pt;border-top:1.2pt solid #000;border-bottom:1.2pt solid #000}
table.lt th{border-bottom:.6pt solid #000;padding:2pt 8pt;text-align:right}table.lt td{padding:1pt 8pt;text-align:right;white-space:nowrap}
table.lt th:first-child,table.lt td:first-child{text-align:left}table.lt tr.b td{font-weight:700}
@media print{.page{min-height:0;height:auto}}'''
MAXW = 600   # words of excerpts per letter


def excerpts(path, rx):
    t = open(path).read()
    t = re.sub(r'\s*[]\s*', ' — ', t)      # private-use glyphs used for em dashes in some PDFs
    t = re.sub(r'[-]', '', t)
    t = t.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'(?<=[a-z])- (?=[a-z])', '', t)
    for a, b in (('W e', 'We'), ('A WS', 'AWS'), ('Y oY', 'YoY'), ('A verage', 'Average'), ('T o ', 'To ')):   # PDF spacing
        t = re.sub(r'\b' + a, b, t)
    s = re.split(r'(?<=[.!?])\s+(?=[A-Z"“(])', t)
    hit = [i for i, x in enumerate(s) if re.search(rx, x, re.I)]
    keep = set()
    for i in hit:
        keep.update(range(max(0, i - 1), min(len(s), i + 2)))
    out, words, prev = [], 0, None
    for i in sorted(keep):
        w = len(s[i].split())
        if words + w > MAXW:
            break
        if prev is not None and i != prev + 1:
            out.append(None)
        out.append(s[i]); words += w; prev = i
    paras, cur = [], []
    for x in out:
        if x is None:
            if cur: paras.append(' '.join(cur)); cur = []
            paras.append(None)
        else:
            cur.append(x)
            if len(cur) >= 4: paras.append(' '.join(cur)); cur = []
    if cur: paras.append(' '.join(cur))
    return paras


def esc(x):
    return x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def tbl(rows, bold=()):
    """Small booktabs table: rows of [label, y1..y4]; first row is the header."""
    out = ['<table class="lt"><tr>' + ''.join(f'<th>{c}</th>' for c in rows[0]) + '</tr>']
    for r in rows[1:]:
        b = ' class="b"' if r[0] in bold else ''
        out.append(f'<tr{b}>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>')
    return '</p>' + ''.join(out) + '</table><p class="ex">'


Y = ['(in thousands)', 'Year 1', 'Year 2', 'Year 3', 'Year 4']
# the 2004 letter's two example tables come out of the PDF as one run of text; rebuild them
LETTER_TABLES = [
 (r'Earnings Year 1 Year 2 Year 3 Year 4 \(in thousands\) Sales.*?Growth N/A 100% 100% 100%(?= However)', tbl([
   Y, ['Sales', '$100,000', '$200,000', '$400,000', '$800,000'], ['Units sold', '100', '200', '400', '800'],
   ['Gross profit', '55,000', '110,000', '220,000', '440,000'], ['Depreciation', '40,000', '80,000', '160,000', '320,000'],
   ['Labor &amp; other costs', '5,000', '10,000', '20,000', '40,000'], ['Earnings', '$10,000', '$20,000', '$40,000', '$80,000'],
   ['Growth', 'N/A', '100%', '100%', '100%']], bold=('Earnings',))),
 (r'Cash Flows Year 1 Year 2 Year 3 Year 4 \(in thousands\) Earnings.*?\$\(240,000\)', tbl([
   Y, ['Earnings', '$10,000', '$20,000', '$40,000', '$80,000'], ['Depreciation', '40,000', '80,000', '160,000', '320,000'],
   ['Working capital', '&mdash;', '&mdash;', '&mdash;', '&mdash;'], ['Operating cash flow', '50,000', '100,000', '200,000', '400,000'],
   ['Capital expenditures', '160,000', '160,000', '320,000', '640,000'],
   ['Free cash flow', '$(110,000)', '$(60,000)', '$(120,000)', '$(240,000)']], bold=('Free cash flow',))),
]


def para(p):
    x = f'<p class="ex">{esc(p)}</p>'
    for rx, t in LETTER_TABLES:
        x = re.sub(rx, lambda m: t, x)
    return x.replace('<p class="ex"></p>', '').replace('<p class="ex"> ', '<p class="ex">')


if len(sys.argv) == 3:
    TXT = {'B': sys.argv[1], 'A': sys.argv[2]}
    for i, th in enumerate(THEMES, 1):
        body = []
        for y in th['years']:
            ps = excerpts(os.path.join(TXT[th['co']], f'{y}.txt'), th['rx'])
            if not ps:
                continue
            body.append(f'<h2>{y} letter</h2>')
            for p in ps:
                body.append('<p class="gap">&hellip;</p>' if p is None else para(p))
        name = CO[th['co']]['name']
        html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shareholder Letters Reading {i}</title><style>{RCSS}</style></head><body>
<div class="bar"><button onclick="print()">Print</button></div>
<div class="page">
<header><span>Shareholder Letters &middot; Accounting Theme {i} &middot; Reading</span><span></span></header>
<h1>{th['theme']}</h1>
<p class="meta">{name} letters: {', '.join(str(y) for y in th['years'])} &middot; Difficulty: {th['diff']}</p>
<div class="sum"><b class="t">Summary</b>{th['summary']}</div>
{chr(10).join(body)}
<p class="src">{source(th, 'Excerpts')} &ldquo;&hellip;&rdquo; marks skipped text. The summary is original course material by Jaeyoon Yu; not affiliated with or endorsed by {CO[th['co']]['owner']}</p>
</div></body></html>'''
        open(os.path.join(OUT, f'R{i:02d}.html'), 'w').write(html)
    print('wrote', len(THEMES), 'readings')

# ---------- page ----------


def h(p):
    f = os.path.join(ROOT, p.lstrip('/'))
    return hashlib.md5(open(f, 'rb').read()).hexdigest()[:8] if os.path.exists(f) else '0'


lines = ['| # | Topic | Accounting theme | Company | Key letters | Lecture | Reading | Difficulty | ACC250 | ACC531 | Questions | Key |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|']
prev = None
for i, th in enumerate(THEMES, 1):
    c = CO[th['co']]
    yl = ', '.join(f'[{y}]({c["url"](y)})' for y in th['years'])
    q = f'/assets/Letters/Q{i:02d}.pdf'; k = f'/assets/Letters/Q{i:02d}-Key.pdf'; rd = f'/assets/Letters/R{i:02d}.pdf'; lh = f'/assets/Letters/L{i:02d}.html'; lp = f'/assets/Letters/L{i:02d}.pdf'
    tp = th['topic'] if th['topic'] != prev else ''
    prev = th['topic']
    lines.append(f'| {i} | {tp} | {th["theme"]} | {c["name"]} | {yl} | [Slides]({lh}?v={h(lh)}){{:target="_blank"}} &middot; [PDF]({lp}?v={h(lp)}) | [PDF]({rd}?v={h(rd)}) | {th["diff"]} | {th["a250"] or "—"} | {th["a531"] or "—"} | [PDF]({q}?v={h(q)}) | [PDF]({k}?v={h(k)}) |')

md = f'''---
layout: page
title: "Shareholder Letters: Accounting Themes"
---

Two sets of annual shareholder letters explain many accounting issues in plain English: Warren Buffett&rsquo;s letters to **Berkshire Hathaway** shareholders (1977&ndash;2024; the 2025 letter is by his successor, Greg Abel) and Jeff Bezos&rsquo;s and Andy Jassy&rsquo;s letters to **Amazon** shareholders (1997&ndash;2025). The table groups the themes by topic and shows the letters that discuss each theme most and where it fits in ACC250 (Intro to Financial Accounting) and ACC531 (Auditing). For each theme, the **Lecture** slides walk through the idea step by step with a small example, the **Reading** packet starts with a short summary and collects only the relevant passages from its key letters, and a one-page question sheet and answer key follow.

<style>
.bt {{ overflow-x:auto; }}
.bt table {{ font-size:.8em; }}
.bt th, .bt td {{ white-space:nowrap; }}
</style>

<div class="bt" markdown="1">

{chr(10).join(lines)}

</div>

**Difficulty**: Intro = needs only ACC250 concepts; Intermediate = intermediate accounting or auditing; Advanced = beyond the intro sequence.
Questions use made-up numbers unless stated.

### Source and copyright

**Sources:**
* Warren E. Buffett (1977&ndash;2024) and Greg Abel (2025), *Letters to Berkshire Hathaway Shareholders*, Berkshire Hathaway Inc., [berkshirehathaway.com/letters](https://www.berkshirehathaway.com/letters/letters.html).
* Jeffrey P. Bezos (1997&ndash;2020) and Andrew R. Jassy (2021&ndash;2025), *Letters to Amazon.com Shareholders*, Amazon.com, Inc., [ir.aboutamazon.com](https://ir.aboutamazon.com/annual-reports-proxies-and-shareholder-letters/default.aspx).

**Copyright:** The Berkshire letters are &copy; Berkshire Hathaway Inc. and the Amazon letters are &copy; Amazon.com, Inc.; all rights reserved. The reading packets and question sheets quote short excerpts for non-commercial teaching only; each cites the letters it quotes and links to the full text. The summaries and questions are original course material by Jaeyoon Yu. This page is not affiliated with or endorsed by Berkshire Hathaway Inc. or Amazon.com, Inc.
'''
open(os.path.join(ROOT, 'shareholder-letters.md'), 'w').write(md)
print('wrote shareholder-letters.md')
