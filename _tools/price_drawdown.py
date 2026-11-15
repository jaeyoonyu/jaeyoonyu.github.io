#!/usr/bin/env python3
"""Price (log scale) + drawdown chart for one stock, as a self-contained HTML page.

Usage: python _tools/price_drawdown.py prices.csv NVDA out.html [years]
prices.csv needs a Date column and a Close (or Adj Close) column, e.g. a Yahoo Finance
or Stooq download. Uses split-adjusted closes as given.
Drawdown at each date = Close / highest Close so far - 1.
"""
import csv, math, sys, datetime as dt

src, ticker, out = sys.argv[1], sys.argv[2], sys.argv[3]
years = float(sys.argv[4]) if len(sys.argv) > 4 else 10

rows = []
with open(src, newline='') as f:
    r = csv.DictReader(f)
    col = next(c for c in ('Adj Close', 'Close', 'close', 'Zamkniecie') if c in r.fieldnames)
    dcol = next(c for c in ('Date', 'date', 'Data') if c in r.fieldnames)
    for x in r:
        try:
            rows.append((dt.date.fromisoformat(x[dcol][:10]), float(x[col])))
        except (ValueError, TypeError):
            pass
rows.sort()
end = rows[-1][0]
start = end - dt.timedelta(days=int(365.25 * years))
rows = [x for x in rows if x[0] >= start]

peak, dd = 0, []
for d, p in rows:
    peak = max(peak, p)
    dd.append(p / peak - 1)

# biggest drawdown episodes (peak -> trough), non-overlapping
episodes, i = [], 0
while i < len(rows):
    if dd[i] < 0:
        j = i
        while j < len(rows) and dd[j] < 0:
            j += 1
        k = min(range(i, j), key=lambda t: dd[t])
        pk = max(range(max(0, i - 1), k + 1), key=lambda t: rows[t][1])
        episodes.append((dd[k], rows[pk][0], rows[k][0], j < len(rows) and rows[j][0] or None))
        i = j
    else:
        i += 1
episodes.sort()
top = episodes[:5]

W, PH, DH, L, R, T, G = 1100, 380, 220, 70, 20, 20, 50
t0, t1 = rows[0][0].toordinal(), rows[-1][0].toordinal()
X = lambda d: L + (d.toordinal() - t0) / (t1 - t0) * (W - L - R)
lo, hi = math.log10(min(p for _, p in rows)), math.log10(max(p for _, p in rows))
Yp = lambda p: T + (hi - math.log10(p)) / (hi - lo) * PH
mind = min(dd)
Yd = lambda v: T + PH + G + (v / mind) * DH

svg = [f'<svg viewBox="0 0 {W} {T + PH + G + DH + 40}" style="width:100%;height:auto" font-family="Helvetica Neue,Arial,sans-serif" font-size="13">']
# price gridlines (powers of 10 and 2x/5x)
for e in range(math.floor(lo), math.ceil(hi) + 1):
    for m in (1, 2, 5):
        v = m * 10 ** e
        if lo <= math.log10(v) <= hi:
            y = Yp(v)
            svg.append(f'<line x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e5e5e5"/>')
            svg.append(f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" fill="#555">${v:g}</text>')
for v in (0, -.2, -.4, -.6, -.8):
    if v >= mind - 1e-9:
        y = Yd(v)
        svg.append(f'<line x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e5e5e5"/>')
        svg.append(f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" fill="#555">{v:.0%}</text>')
for yr in range(rows[0][0].year + 1, rows[-1][0].year + 1):
    x = X(dt.date(yr, 1, 1))
    svg.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T}" y2="{T+PH+G+DH}" stroke="#f0f0f0"/>')
    svg.append(f'<text x="{x:.1f}" y="{T+PH+G+DH+20}" text-anchor="middle" fill="#555">{yr}</text>')
pts = ' '.join(f'{X(d):.1f},{Yp(p):.1f}' for d, p in rows)
svg.append(f'<polyline points="{pts}" fill="none" stroke="#3333b3" stroke-width="1.8"/>')
area = f'M{X(rows[0][0]):.1f},{Yd(0):.1f} ' + ' '.join(f'L{X(d):.1f},{Yd(v):.1f}' for (d, _), v in zip(rows, dd)) + f' L{X(rows[-1][0]):.1f},{Yd(0):.1f} Z'
svg.append(f'<path d="{area}" fill="#e57373" fill-opacity=".55" stroke="#c62828" stroke-width="1"/>')
for v, pk, tr, rec in top:
    x, y = X(tr), Yd(v)
    svg.append(f'<text x="{x:.1f}" y="{y+16:.1f}" text-anchor="middle" font-weight="700" fill="#b3200f">{v:.0%}</text>')
svg.append(f'<text x="{L}" y="{T-4}" fill="#3333b3" font-weight="700">{ticker} share price (split-adjusted, log scale)</text>')
svg.append(f'<text x="{L}" y="{T+PH+G-8}" fill="#b3200f" font-weight="700">Drawdown: decline from the highest price so far</text>')
svg.append('</svg>')

trs = ''.join(f'<tr><td>{pk:%b %Y}</td><td>{tr:%b %Y}</td><td class="r">{v:.0%}</td><td>{rec and f"{rec:%b %Y}" or "not yet"}</td></tr>' for v, pk, tr, rec in top)
first, last = rows[0][1], rows[-1][1]
html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ticker} Price and Drawdown</title>
<style>body{{font-family:Helvetica Neue,Arial,sans-serif;max-width:1150px;margin:24px auto;padding:0 16px;color:#000}}
h1{{color:#3333b3;font-weight:400;border-bottom:2px solid #3333b3;padding-bottom:6px}}
table{{border-collapse:collapse;margin:10px 0}}th{{border-top:2px solid #000;border-bottom:1px solid #000;padding:4px 12px;text-align:left;font-weight:400}}
td{{padding:4px 12px}}tr:last-child td{{border-bottom:2px solid #000}}.r{{text-align:right}}</style></head><body>
<h1>{ticker}: price and drawdown, {rows[0][0]:%b %Y} &ndash; {rows[-1][0]:%b %Y}</h1>
<p>Price went from ${first:,.2f} to ${last:,.2f} (&times;{last/first:,.0f}). Largest drawdown: <b>{mind:.0%}</b>.</p>
{"".join(svg)}
<p><b>Largest drawdowns</b></p>
<table><tr><th>Peak</th><th>Trough</th><th class="r">Decline</th><th>Back to the peak</th></tr>{trs}</table>
<p style="font-size:13px">Daily closing prices, adjusted for stock splits. Drawdown = price &divide; highest price so far &minus; 1.</p>
</body></html>'''
open(out, 'w').write(html)
print('wrote', out, len(rows), 'days; max drawdown', f'{mind:.1%}')
