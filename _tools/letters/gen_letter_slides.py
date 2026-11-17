#!/usr/bin/env python3
"""Step-by-step lecture slides (Beamer look, 4:3) for every shareholder-letter theme.

Usage (from the repo root): python _tools/letters/gen_letter_slides.py
Reads the themes from gen_letters.py and the step slides from slide_content.py;
writes assets/Letters/Lnn.html (print to Lnn.pdf separately, one slide per page).
CSS and navigation come from _tools/acc250_case/gen_berkshire_slides.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from slide_content import D, BOX, UL

src = open(os.path.join(HERE, 'gen_letters.py')).read().split('\nfor i, th in enumerate(THEMES, 1):')[0]
ns = {'__file__': os.path.join(HERE, 'gen_letters.py')}
exec(src, ns)
THEMES, CO = ns['THEMES'], ns['CO']

tpl = open(os.path.join(ROOT, '_tools', 'acc250_case', 'gen_berkshire_slides.py')).read()
CSS = tpl.split('<style>\n')[1].split('</style>')[0].replace('{{', '{').replace('}}', '}')
JS = tpl.split('<script>\n')[1].split('</script>')[0].replace('{{', '{').replace('}}', '}')
CSS += '''
.s:not(.title) .body { display:flex; flex-direction:column; justify-content:center; padding-bottom:30px; }
.s:not(.title) .body > * { flex:none; }
.s:not(.title) .body > .rbox.je { align-self:flex-start; }
.tsub { font-size:24px; color:#000; margin:-34px 0 46px; }
table.bt.sm { font-size:24px; }
table.bt th.r { text-align:right; }
.rbox.je tr.gap td { height:12px; }
.quote { font-style:italic; font-size:30px; }
.who { text-align:right; font-size:24px; margin-top:6px; }
.note { font-size:18px; margin-top:10px; }
.mc { font-size:24px; margin:.1em 0 .3em; }
@media print { @page { size:1200px 900px; margin:0; } html, body { height:auto; overflow:visible; background:#fff; }
  #stage { width:1200px; height:auto; } .s { display:block !important; position:relative; width:1200px; height:900px; page-break-after:always; break-after:page; } }
'''

FOOT_L = 'Shareholder Letters: Accounting Themes'


def author(c, y):
    return 'Greg Abel' if c == 'B' and y >= 2025 else CO[c]['who']([y])


def deck(i, th):
    co = CO[th['co']]
    years = ', '.join(str(y) for y in th['years'])
    m = re.match(r'(.*) \((.*)\)$', th['quote'])
    slides = [('title', '', f'''<div class="tblock">
<p class="tsmall">{FOOT_L}</p>
<p class="tbig">{th['theme']}</p>
<p class="tsub">{co['name']} letters: {years}</p>
<p class="tauth">Jaeyoon Yu, Ph.D.<br>Central Michigan University</p>
</div>''')]
    slides.append(('', 'What the Letter Says', BOX(f'<p class="quote">&ldquo;{m.group(1)}&rdquo;</p><p class="who">{author(th['co'], int(m.group(2)))}, {m.group(2)} letter</p>')
                   + UL(f'Key letters: {years}', f'Course fit: ACC250 {th["a250"] or "&mdash;"} &middot; ACC531 {th["a531"] or "&mdash;"} &middot; Difficulty: {th["diff"]}')))
    slides += [('', t, b) for t, b in D[th['theme']]]
    qs = []
    for qn, q in enumerate(th['qs']):
        if q[0] == 'mc':   # same option order as the question sheet
            r = (i * 2 + qn * 3) % 4
            q = ('mc', q[1], q[2][r:] + q[2][:r], (q[3] - r) % 4)
        if q[0] == 'num':
            qs.append(f'<li>{q[1]}</li>')
        else:
            opts = ''.join(f'<li>{o}</li>' for o in q[2])
            qs.append(f'<li>{q[1]}<ol class="mc" type="A">{opts}</ol></li>')
    slides.append(('', 'Questions', f'<ol class="qq">{"".join(qs)}</ol>'))
    links = ''.join(f'<li><a href="{co["url"](y)}" target="_blank">{author(th['co'], y)}, {y} letter</a> ({co["site"]})</li>' for y in th['years'])
    slides.append(('', 'Sources', f'''<ul class="src">{links}
<li><a href="R{i:02d}.pdf">Reading packet</a> and <a href="Q{i:02d}.pdf">question sheet</a> for this theme</li></ul>
<p class="note">Letters &copy; {co['owner']}; quoted for non-commercial teaching. Examples use made-up numbers unless a slide says otherwise. Not affiliated with or endorsed by {co['owner']}</p>'''))
    N = len(slides)
    secs = []
    for k, (kind, title, body) in enumerate(slides, 1):
        head = '' if kind == 'title' else f'<div class="ft">{title}</div>'
        secs.append(f'''<section class="s{' title' if kind else ''}">
{head}<div class="body">{body}</div>
<div class="foot"><span class="f1">{FOOT_L}</span><span class="f2">{th['theme']}</span><span class="f3">{k} / {N}</span></div>
</section>''')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{re.sub('<[^>]+>', '', th['theme'])}</title>
<style>{CSS}
ol.mc {{ counter-reset:m; list-style:upper-alpha; padding-left:1.2em; }} ol.mc > li {{ counter-increment:m; }} ol.mc > li::before {{ display:none; }}
</style>
</head>
<body>
<div id="stage">
{chr(10).join(secs)}
</div>
<script>{JS}</script>
</body>
</html>
'''


for i, th in enumerate(THEMES, 1):
    open(os.path.join(ROOT, 'assets', 'Letters', f'L{i:02d}.html'), 'w').write(deck(i, th))
print('wrote', len(THEMES), 'decks')
