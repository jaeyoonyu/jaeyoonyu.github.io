#!/usr/bin/env python3
"""Berkshire buyback slides in the style of the ACC250 Beamer lecture notes (4:3).

Usage: python _tools/acc250_case/gen_berkshire_slides.py assets/ACC250
Optional photos (shown if present): assets/ACC250/img/buffett.jpg, assets/ACC250/img/berkshire.jpg
"""
import os, sys

OUT = sys.argv[1]
FOOT_L = 'ACC250: Intro to Financial Accounting'
FOOT_M = 'Accounting in the News: Berkshire Buybacks'

def photo(name, cap):
    if os.path.exists(os.path.join(OUT, 'img', name)):
        return f'<figure class="ph"><img src="img/{name}" alt=""><figcaption>{cap}</figcaption></figure>'
    return ''


import math
def pie(items, total_label):
    """items: (name, value $B, logo file or None, logo w, logo h, color). Inline SVG pie with logo labels."""
    W, H, cx, cy, r = 1100, 560, 550, 268, 205
    tot = sum(v for _, v, *_ in items)
    out = [f'<svg viewBox="0 0 {W} {H}" style="width:100%;height:auto;display:block" font-family="Helvetica Neue,Arial,sans-serif">']
    a0 = -math.pi / 2
    for name, v, logo, lw, lh, col in items:
        a1 = a0 + v / tot * 2 * math.pi
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        big = 1 if a1 - a0 > math.pi else 0
        out.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 {big} 1 {x1:.1f},{y1:.1f} Z" fill="{col}" stroke="#fff" stroke-width="3"/>')
        am = (a0 + a1) / 2
        pct = v / tot * 100
        # percent inside the slice
        ix, iy = cx + r * .66 * math.cos(am), cy + r * .66 * math.sin(am)
        out.append(f'<text x="{ix:.1f}" y="{iy+9:.1f}" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">{pct:.0f}%</text>')
        # label outside: logo + value
        lx, ly = cx + (r + 34) * math.cos(am), cy + (r + 34) * math.sin(am)
        right = math.cos(am) >= 0
        anchor = 'start' if right else 'end'
        bx = lx if right else lx - max(lw, 150)
        out.append(f'<line x1="{cx + r*math.cos(am):.1f}" y1="{cy + r*math.sin(am):.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="#888" stroke-width="1.5"/>')
        if logo:
            ix0 = lx if right else lx - lw
            out.append(f'<image href="img/logos/{logo}" x="{ix0:.1f}" y="{ly - lh - 2:.1f}" width="{lw}" height="{lh}" preserveAspectRatio="xMidYMid meet"/>')
        else:
            out.append(f'<text x="{lx:.1f}" y="{ly - 6:.1f}" text-anchor="{anchor}" font-size="24" font-weight="700" fill="#333">{name}</text>')
        out.append(f'<text x="{lx:.1f}" y="{ly + 24:.1f}" text-anchor="{anchor}" font-size="22" fill="#333">${v:.1f}B</text>')
        a0 = a1
    out.append(f'<text x="{cx}" y="{H - 4}" text-anchor="middle" font-size="22" fill="#333">{total_label}</text>')
    out.append('</svg>')
    return ''.join(out)

PORTFOLIO = pie([("Apple", 66.0, "apple.svg", 34, 42, "#6e6e6e"),
                 ("American Express", 51.3, "amex.svg", 62, 62, "#2e77bb"),
                 ("Alphabet", 37.8, "alphabet.svg", 130, 32, "#34a853"),
                 ("Coca-Cola", 32.5, "cocacola.svg", 120, 38, "#e41e2b"),
                 ("Bank of America", 27.5, "bofa.svg", 200, 20, "#012169"),
                 ("All others", 84.2, None, 0, 0, "#b9b9b9")],
                "Total: $299.3B, June 30, 2026")

slides = []

slides.append(('title', '', '''
<div class="tblock">
<p class="tsmall">ACC250: Intro to Financial Accounting</p>
<p class="tbig">Accounting in the News: Berkshire Buybacks</p>
<p class="tauth">Jaeyoon Yu, Ph.D.<br>Central Michigan University</p>
</div>'''))

slides.append(('', 'Berkshire Hathaway, Warren Buffett and Greg Abel', f'''
<ul>
<li><b>Berkshire Hathaway</b> (Omaha, Nebraska): owns whole businesses such as <b>GEICO</b>, <b>BNSF</b> railroad and Berkshire Hathaway Energy, and large stakes in Apple, Coca-Cola, American Express, &hellip;</li>
<li><b>Warren Buffett</b> ran Berkshire for six decades; stepped down as CEO at the end of 2025 and is still chairman.</li>
<li><b>Greg Abel</b>: CEO since January 2026.</li>
</ul>
<div class="phrow">{photo("buffett.jpg", "Warren Buffett (U.S. International Trade Administration, public domain)")}{photo("abel.jpg", "Greg Abel (Tankforwin, CC BY-SA 4.0)")}</div>
<p class="credit">Photos via Wikimedia Commons.</p>'''))

slides.append(('', 'Berkshire&rsquo;s Stock Portfolio', f'''
<p>Besides the businesses it owns, Berkshire holds shares of other public companies. Five stocks make up about <b>72%</b>.</p>
{PORTFOLIO}
<p class="note" style="margin-top:4px;font-size:16px">As of June 30, 2026 (Form 13F, U.S.-listed stocks). &ldquo;All others&rdquo; (incl. Chevron) = total minus the five largest. Logos via Wikimedia Commons; trademarks of their owners.</p>'''))

slides.append(('', 'The News: Q3 2026 Results', '''
<p><span class="ex">Q3 2026</span> (reported Nov 7, 2026)</p>
<table class="bt">
<tr><th>Item</th><th class="r">Amount</th><th class="r">Change</th></tr>
<tr><td>Revenue</td><td class="r">$105.6B</td><td class="r">+11%</td></tr>
<tr><td>Operating earnings</td><td class="r">$12.7B</td><td class="r">&minus;6%</td></tr>
<tr><td>Cash on hand</td><td class="r">$377.4B</td><td class="r">+3% vs Q2</td></tr>
<tr class="pink"><td>Stock buybacks</td><td class="r">$9.6B</td><td class="r">Q2: $4.5B</td></tr>
</table>
<ul>
<li>Operating earnings fell, dragged down by weaker <b>insurance</b> underwriting.</li>
<li>Buybacks <b>more than doubled</b> from the previous quarter.</li>
</ul>'''))

slides.append(('', 'What Can a Company Do with Extra Cash?', '''
<ol>
<li><b>Invest outside</b>: buy another company, build new plants.</li>
<li><b>Pay dividends</b>: cash to all shareholders. (Berkshire pays none.)</li>
<li><b>Buy back its own shares</b>: cash to the shareholders who choose to sell.</li>
</ol>
<div class="rbox">With $377B of cash and few large deals at good prices, option 1 is hard. &rarr; Option 3.</div>'''))

slides.append(('', 'When Does a Buyback Make Sense?', '''
<ol>
<li><b>No better investment outside</b><br>Idle cash earns little.</li>
<li><b>Own stock looks cheap</b><br>Management believes the shares are worth <span class="hl">more than their price</span> and will rise.</li>
</ol>
<div class="rbox"><b>Berkshire&rsquo;s rule</b>: buy back only when the price is below a conservative estimate of intrinsic value, and keep at least $30B of cash.</div>'''))

slides.append(('', 'Effect: Fewer Shares Outstanding', '''
<p><span class="ex">EX.</span> Net income $100; the company buys back 10 of its 100 shares.</p>
<table class="bt">
<tr><th></th><th class="r">Before</th><th class="r">After</th></tr>
<tr><td>Net income</td><td class="r">$100</td><td class="r">$100</td></tr>
<tr><td>Shares outstanding</td><td class="r">100</td><td class="r">90</td></tr>
<tr class="yel"><td><b>EPS</b> = NI &divide; shares outstanding</td><td class="r"><b>$1.00</b></td><td class="r"><b>$1.11</b></td></tr>
</table>
<ul>
<li>Same profit, fewer owners &rarr; each remaining share owns a <b>bigger slice</b>.</li>
</ul>'''))

slides.append(('', 'Accounting for a Buyback: Treasury Stock (Ch11)', '''
<p><span class="ex">EX.</span> Berkshire buys back $9.6B of its own stock.</p>
<div class="rbox je"><span class="jd">Q3:</span><span class="jl">Treasury Stock (+xSE, &minus;SE)<br><span class="ind">Cash (&minus;A)</span></span><span class="ja">9.6B<br><span class="ind2">9.6B</span></span></div>
<ul>
<li><b>Treasury stock</b>: a contra-equity account (xSE) &rarr; reduces stockholders&rsquo; equity.</li>
<li>Assets &darr; and SE &darr; by the same amount. No expense &rarr; net income unchanged.</li>
<li>Shares <b>issued</b>: unchanged. Shares <b>outstanding</b>: &darr;.</li>
</ul>'''))

slides.append(('', 'The Catch: Price Matters', '''
<table class="bt">
<tr><th>Buyback price</th><th>Remaining shareholders</th></tr>
<tr><td>Below value</td><td>Gain: $1 of value bought for less than $1</td></tr>
<tr class="pink"><td>Above value</td><td>Lose: the company overpaid for its own shares</td></tr>
</table>
<ul>
<li>Berkshire&rsquo;s shares hit record highs this fall &rarr; analysts question whether the pace can continue.</li>
</ul>'''))

slides.append(('', 'Questions', '''
<ol>
<li>A company earns $500 with 250 shares outstanding, then buys back 50 shares. EPS before and after?</li>
<li>After a $9.6B buyback, what happens to total assets, total SE, and net income?</li>
<li>Berkshire has $377B of cash. Why buy back shares instead of paying a dividend?</li>
</ol>'''))

slides.append(('', 'Sources', '''
<ul class="src">
<li><a href="https://www.cnbc.com/2026/11/07/berkshire-hathaway-q3-2026-earnings-buybacks.html" target="_blank">CNBC, Nov 7, 2026</a>: Berkshire more than doubles buybacks in Q3 as earnings decline</li>
<li><a href="https://www.insurancejournal.com/news/national/2026/11/09/891933.htm" target="_blank">Insurance Journal, Nov 9, 2026</a>: Berkshire boosts buybacks as operating income slips</li>
<li><a href="https://www.fool.com/investing/2026/11/13/greg-abel-bought-back-a-record-amount-of-berkshire-hathaway/" target="_blank">Motley Fool, Nov 13, 2026</a>: Abel bought back a record $9.6B of stock</li>
<li><a href="https://www.cnbc.com/2026/08/15/berkshire-adds-17-billion-to-alphabet-stake.html" target="_blank">CNBC, Aug 15, 2026</a>: Berkshire adds $17 billion to Alphabet stake (Q2 13F)</li>
<li><a href="https://www.berkshirehathaway.com/reports.html" target="_blank">Berkshire Hathaway quarterly reports</a></li>
</ul>
<p class="note">Operating earnings: $12.7B, down 5.8% from $13.5B a year earlier. The EPS example uses made-up numbers.</p>'''))

N = len(slides)
secs = []
for i, (kind, title, body) in enumerate(slides, 1):
    head = '' if kind == 'title' else f'<div class="ft">{title}</div>'
    secs.append(f'''<section class="s{' title' if kind else ''}" data-nav="{title or 'Title'}">
{head}<div class="body">{body}</div>
<div class="foot"><span class="f1">{FOOT_L}</span><span class="f2">{FOOT_M}</span><span class="f3">{i} / {N}</span></div>
</section>''')

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Berkshire Buybacks</title>
<style>
:root {{ --blue:#3333b3; --b1:#2c2c8a; --b2:#5a5ad0; --b3:#a6a6e8; }}
* {{ box-sizing:border-box; }}
html, body {{ margin:0; height:100%; background:#555; }}
body {{ display:flex; align-items:center; justify-content:center; overflow:hidden;
  font-family:"Latin Modern Sans","CMU Sans Serif","Helvetica Neue",Arial,sans-serif; color:#000; }}
#stage {{ position:relative; width:1200px; height:900px; background:#fff; transform-origin:center; box-shadow:0 10px 40px rgba(0,0,0,.4); }}
.s {{ position:absolute; inset:0; display:none; }}
.s.on {{ display:block; }}
.ft {{ position:absolute; left:0; right:0; top:0; padding:22px 40px 12px; font-size:40px; color:var(--blue);
  border-bottom:2px solid var(--blue); }}
.body {{ position:absolute; left:40px; right:40px; top:110px; bottom:60px; font-size:30px; line-height:1.38; }}
.title .body {{ top:0; display:flex; align-items:center; justify-content:center; text-align:center; }}
.tsmall {{ color:var(--blue); font-size:30px; margin:0 0 8px; }}
.tbig {{ color:var(--blue); font-size:42px; margin:0 0 50px; }}
.tauth {{ font-size:26px; margin:0; }}
.foot {{ position:absolute; left:0; right:0; bottom:0; height:30px; display:flex; font-size:15px; color:#fff; }}
.foot span {{ display:flex; align-items:center; padding:0 18px; }}
.f1 {{ background:var(--b1); width:36%; justify-content:center; }}
.f2 {{ background:var(--b2); width:40%; justify-content:center; }}
.f3 {{ background:var(--b3); flex:1; justify-content:flex-end; }}
ul, ol {{ margin:.3em 0 .5em; padding-left:1.5em; }}
li {{ margin:.25em 0; }}
ul {{ list-style:none; }}
ul > li {{ position:relative; }}
ul > li::before {{ content:""; position:absolute; left:-1.05em; top:.48em; width:.42em; height:.42em; border-radius:50%;
  background:radial-gradient(circle at 35% 35%, #8a8ae6, var(--blue)); }}
ol {{ counter-reset:k; list-style:none; }}
ol > li {{ counter-increment:k; position:relative; }}
ol > li::before {{ content:counter(k); position:absolute; left:-1.5em; top:.12em; width:1.05em; height:1.05em; border-radius:50%;
  background:var(--blue); color:#fff; font-size:.7em; display:flex; align-items:center; justify-content:center; }}
p {{ margin:.3em 0; }}
.h {{ font-weight:700; margin:.4em 0 .1em; }}
.ex {{ background:#ffeb3b; font-weight:700; text-decoration:underline; padding:0 4px; }}
.hl {{ color:#1a8a1a; font-weight:700; text-decoration:underline; }}
table.bt {{ border-collapse:collapse; margin:16px auto 18px; font-size:28px; min-width:70%; }}
table.bt th {{ border-top:2px solid #000; border-bottom:1px solid #000; padding:6px 16px; text-align:left; font-weight:400; }}
table.bt td {{ padding:6px 16px; }}
table.bt tr:last-child td {{ border-bottom:2px solid #000; }}
table.bt .r {{ text-align:right; }}
table.bt tr.pink td {{ background:#f6c6c6; }}
table.bt tr.yel td {{ background:#fff26b; }}
.rbox {{ border:2px solid #e57373; border-radius:16px; padding:14px 22px; margin:22px 0; }}
.rbox.je {{ display:grid; grid-template-columns:80px 1fr 140px; align-items:center; max-width:760px; }}
.jd {{ font-weight:700; }}
.jl {{ border-left:2px solid #000; padding-left:16px; }}
.ind {{ padding-left:40px; }} .ind2 {{ padding-left:60px; }}
.ja {{ text-align:right; }}
.ph {{ margin:0 0 14px; text-align:center; }}
.ph {{ margin-top:10px; }}
.phrow {{ display:flex; justify-content:center; gap:40px; }}
.credit {{ font-size:14px; color:#444; text-align:center; margin:0; }}
.ph img {{ height:330px; border:1px solid #ccc; }}
.ph figcaption {{ font-size:15px; color:#444; margin-top:4px; }}
.src {{ font-size:24px; }}
.src a {{ color:var(--blue); }}
.note {{ font-size:20px; margin-top:24px; }}
@media print {{ body {{ background:#fff; display:block; }} #stage {{ transform:none !important; box-shadow:none; }} }}
</style>
</head>
<body>
<div id="stage">
{chr(10).join(secs)}
</div>
<script>
const S=[...document.querySelectorAll('.s')]; let i=0;
function go(n){{ if(n<0||n>=S.length) return; i=n; S.forEach((s,k)=>s.classList.toggle('on',k===i)); location.hash=i+1; }}
function fit(){{ const k=Math.min(innerWidth/1200, innerHeight/900); document.getElementById('stage').style.transform=`scale(${{k}})`; }}
addEventListener('resize',fit);
addEventListener('keydown',e=>{{ const k=e.key;
  if(['ArrowRight','ArrowDown',' ','PageDown','Enter'].includes(k)){{go(i+1);e.preventDefault();}}
  else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(k)){{go(i-1);e.preventDefault();}}
  else if(k==='Home') go(0); else if(k==='End') go(S.length-1);
  else if(k==='f'||k==='F') document.documentElement.requestFullscreen?.(); }});
document.getElementById('stage').addEventListener('click',e=>{{ if(e.target.closest('a')) return; e.clientX<innerWidth*.3?go(i-1):go(i+1); }});
let tx=0; addEventListener('touchstart',e=>tx=e.touches[0].clientX,{{passive:true}});
addEventListener('touchend',e=>{{const d=e.changedTouches[0].clientX-tx; if(Math.abs(d)>50) go(d<0?i+1:i-1);}},{{passive:true}});
fit(); go(Math.max(0,(parseInt(location.hash.slice(1))||1)-1));
</script>
</body>
</html>
'''
open(os.path.join(OUT, 'Berkshire-Buyback.html'), 'w').write(html)
print('wrote Berkshire-Buyback', N)
