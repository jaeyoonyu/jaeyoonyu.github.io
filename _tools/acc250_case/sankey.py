"""Inline-SVG Sankey diagram of an income statement (no external libraries).

nodes: list of dicts {id, col, value, kind, label}
    kind: 'rev' (revenue), 'profit', 'cost', 'other' (non-operating income added in)
links: list of (source_id, target_id, value) in drawing order.
Children of a node are placed in link order: the first child keeps the parent's
top edge (the profit line runs straight across); later children (costs) drop
below it with a gap. A node with two parents (e.g. income before taxes, fed by
operating income and interest income) sits level with its first parent; the
second parent is placed just below and is laid out before the merge.
"""
from collections import defaultdict

COL = {'rev': '#5b7f95', 'profit': '#1a7a5e', 'cost': '#b3200f', 'other': '#b8901f'}
LINK = {'rev': '#9fb6c4', 'profit': '#8fcfb6', 'cost': '#efaaa0', 'other': '#e3cf94'}


def fmt(v):
    return f'{v:,.0f}'


def render(nodes, links, total, width=1400, height=550, unit='$ millions',
           top=78, bar_h=330, node_w=16, gap=34, left=200, right=230):
    N = {n['id']: dict(n) for n in nodes}
    k = bar_h / total                       # px per $
    for n in N.values():
        n['h'] = max(n['value'] * k, 2.0)
    outs, ins = defaultdict(list), defaultdict(list)
    for s, t, v in links:
        outs[s].append((t, v)); ins[t].append((s, v))
    cols = sorted({n['col'] for n in N.values()})
    span = (width - left - right - node_w) / (len(cols) - 1)
    for n in N.values():
        n['x'] = left + cols.index(n['col']) * span

    # --- vertical placement -------------------------------------------------
    placed = {}
    roots = [n for n in nodes if not ins[n['id']]]
    y = top
    for r in [r for r in roots if r['col'] == cols[0]]:
        placed[r['id']] = y; y += N[r['id']]['h'] + gap

    def place(nid):
        if nid in placed:
            return placed[nid]
        ps = ins[nid]
        if not ps:
            return None                     # placed later by the node it feeds
        p0 = ps[0][0]
        if p0 not in placed:
            place(p0)
        # offset of this link inside the first parent's outflows
        off, idx = 0.0, 0
        for i, (t, v) in enumerate(outs[p0]):
            if t == nid:
                idx = i; break
            off += v * k
        yy = placed[p0] + off + (gap * idx)
        placed[nid] = yy
        # secondary parents that are roots: put them right under this node's first input
        acc = ps[0][1] * k
        for s, v in ps[1:]:
            if s not in placed:
                placed[s] = yy + acc + gap
            acc += v * k
        return yy

    for n in nodes:
        place(n['id'])
    for n in nodes:                         # roots outside the first column
        if n['id'] not in placed:
            place(outs[n['id']][0][0])
    for nid, yy in placed.items():
        N[nid]['y'] = yy
    for n in N.values():                    # explicit placement under another node
        if n.get('below'):
            b = N[n['below']]
            n['y'] = b['y'] + b['h'] + 92
    # last column: leave room for each three-line label
    lastcol = sorted((n for n in N.values() if n['col'] == cols[-1]), key=lambda n: n['y'])
    for a, b in zip(lastcol, lastcol[1:]):
        b['y'] = max(b['y'], a['y'] + max(a['h'], 0) + 66)

    # --- links --------------------------------------------------------------
    out_off, in_off = defaultdict(float), defaultdict(float)
    paths = []
    for s, t, v in links:
        a, b = N[s], N[t]
        h = v * k
        y0 = a['y'] + out_off[s]; out_off[s] += h
        y1 = b['y'] + in_off[t]; in_off[t] += h
        x0, x1 = a['x'] + node_w, b['x']
        mx = (x0 + x1) / 2
        kind = b['kind'] if b['kind'] in ('cost', 'profit') else a['kind']
        if a['kind'] == 'other':
            kind = 'other'
        d = (f'M{x0:.1f},{y0:.1f} C{mx:.1f},{y0:.1f} {mx:.1f},{y1:.1f} {x1:.1f},{y1:.1f} '
             f'L{x1:.1f},{y1 + h:.1f} C{mx:.1f},{y1 + h:.1f} {mx:.1f},{y0 + h:.1f} {x0:.1f},{y0 + h:.1f} Z')
        paths.append(f'<path d="{d}" fill="{LINK[kind]}" fill-opacity=".75"/>')

    # --- nodes and labels ---------------------------------------------------
    rects, labels = [], []
    last = cols[-1]
    for n in N.values():
        rects.append(f'<rect x="{n["x"]:.1f}" y="{n["y"]:.1f}" width="{node_w}" height="{n["h"]:.1f}" '
                     f'fill="{COL[n["kind"]]}" rx="2"/>')
        pct = n['value'] / total * 100
        val = f'{fmt(n["value"])}'
        sub = f'{pct:.1f}% of revenue' if n['kind'] != 'rev' or n['col'] != cols[0] else ''
        if n['col'] == cols[0]:
            tx, anchor, ty = n['x'] - 10, 'end', n['y'] + min(n['h'], 60) / 2
        elif n['col'] == last:
            tx, anchor, ty = n['x'] + node_w + 10, 'start', n['y'] + max(n['h'], 18) / 2
        elif n['kind'] == 'cost' or n['kind'] == 'other':
            tx, anchor, ty = n['x'] + node_w / 2, 'middle', n['y'] + n['h'] + 24
        else:
            tx, anchor, ty = n['x'] + node_w / 2, 'middle', n['y'] - 44
        c = COL[n['kind']]
        lines = [f'<tspan x="{tx:.1f}" font-weight="700" fill="{c}">{n["label"]}</tspan>',
                 f'<tspan x="{tx:.1f}" dy="22" font-weight="700" fill="#16263a">{val}</tspan>']
        if sub:
            lines.append(f'<tspan x="{tx:.1f}" dy="19" font-size="15" fill="#5c6863">{sub}</tspan>')
        labels.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" font-size="18">{"".join(lines)}</text>')

    return (f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Income statement Sankey diagram" '
            f'style="width:100%;height:auto;display:block;font-family:\'Segoe UI\',system-ui,sans-serif">'
            + ''.join(paths) + ''.join(rects) + ''.join(labels)
            + f'<text x="{width - 4}" y="{height - 6}" text-anchor="end" font-size="14" fill="#5c6863">{unit}</text></svg>')


def walmart():
    nodes = [dict(id='ns', col=0, value=674538, kind='rev', label='Net sales'),
             dict(id='mem', col=0, value=6447, kind='rev', label='Membership income'),
             dict(id='tr', col=1, value=680985, kind='rev', label='Total revenues'),
             dict(id='gp', col=2, value=169232, kind='profit', label='Gross profit*'),
             dict(id='cogs', col=2, value=511753, kind='cost', label='Cost of sales'),
             dict(id='oi', col=3, value=29348, kind='profit', label='Operating income'),
             dict(id='sga', col=3, value=139884, kind='cost', label='Operating expenses (SG&amp;A)'),
             dict(id='ni', col=4, value=20157, kind='profit', label='Net income'),
             dict(id='tax', col=4, value=6152, kind='cost', label='Income taxes'),
             dict(id='int', col=4, value=3039, kind='cost', label='Interest &amp; other, net')]
    links = [('ns', 'tr', 674538), ('mem', 'tr', 6447),
             ('tr', 'gp', 169232), ('tr', 'cogs', 511753),
             ('gp', 'oi', 29348), ('gp', 'sga', 139884),
             ('oi', 'ni', 20157), ('oi', 'tax', 6152), ('oi', 'int', 3039)]
    return render(nodes, links, 680985)


def costco():
    nodes = [dict(id='ns', col=0, value=269912, kind='rev', label='Net sales'),
             dict(id='mem', col=0, value=5323, kind='rev', label='Membership fees'),
             dict(id='tr', col=1, value=275235, kind='rev', label='Total revenue'),
             dict(id='gp', col=2, value=35349, kind='profit', label='Gross profit*'),
             dict(id='cogs', col=2, value=239886, kind='cost', label='Merchandise costs'),
             dict(id='oi', col=3, value=10383, kind='profit', label='Operating income'),
             dict(id='sga', col=3, value=24966, kind='cost', label='SG&amp;A'),
             dict(id='pti', col=4, value=10818, kind='profit', label='Income before taxes'),
             dict(id='ni', col=5, value=8099, kind='profit', label='Net income'),
             dict(id='tax', col=5, value=2719, kind='cost', label='Income taxes')]
    nodes.insert(7, dict(id='int', col=3, value=435, kind='other', label='Interest &amp; other income', below='sga'))
    links = [('ns', 'tr', 269912), ('mem', 'tr', 5323),
             ('tr', 'gp', 35349), ('tr', 'cogs', 239886),
             ('gp', 'oi', 10383), ('gp', 'sga', 24966),
             ('oi', 'pti', 10383), ('int', 'pti', 435),
             ('pti', 'ni', 8099), ('pti', 'tax', 2719)]
    return render(nodes, links, 275235)
