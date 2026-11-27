"""Write _includes/market-snapshot.html: SPY, QQQ, SMH, TQQQ, SOXL - last close, all-time high,
drawdown, and returns (YTD, 1 year, annualized 3/5/10/20 years).

Run from the repo root:  python _code/market_snapshot.py
Prices: Yahoo Finance via FinanceDataReader (daily closes, fetched at run time).
Only the summary numbers below are published, not the price series.
Run daily after the US close by .github/workflows/market-snapshot.yml.
"""
from datetime import datetime, timezone
from pathlib import Path

import FinanceDataReader as fdr
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
# (ticker, what it tracks); history is read from 1993 (SPY's launch) or the fund's own start
SERIES = [("SPY", "S&P 500"), ("QQQ", "Nasdaq-100"), ("TQQQ", "Nasdaq-100, 3× daily"),
          ("SMH", "Semiconductors"), ("SOXL", "Semiconductors, 3× daily")]
YEARS = [3, 5, 10, 20]  # annualized return horizons
# Funds whose name in the top table links to a detail page (written by _code/halving_strategy.py)
DETAIL = {"QQQ": "/halving-qqq/", "TQQQ": "/halving-tqqq/"}
# Major sell-offs, the deepest S&P 500 falls since 1993 (daily closes): (name, window). Drawdown =
# largest fall from a high to a low inside the window; "—" when the fund did not exist at its start.
# The header shows when SPY went from high to low in each.
EVENTS = [("Dot-com", "2000-01-01", "2002-12-31"),
          ("GFC", "2007-07-01", "2009-06-30"),
          ("Q4 2018", "2018-09-01", "2018-12-31"),
          ("COVID", "2020-02-01", "2020-04-30"),
          ("Bear 2022", "2021-11-01", "2022-12-31"),
          ("Tariffs", "2025-02-01", "2025-05-31")]


def stats(symbol):
    df = fdr.DataReader(symbol, "1993-01-01")
    close = df["Close"].dropna()
    adj = df["Adj Close"].dropna()  # dividends reinvested: for returns
    # Before the 4 pm Eastern close, today's row is a live price, not a close: drop it.
    now = pd.Timestamp.now(tz="America/New_York")
    if close.index[-1].date() == now.date() and now.hour < 16:
        close, adj = close.iloc[:-1], adj.iloc[:-1]
    last, last_day = float(close.iloc[-1]), close.index[-1]
    high, high_day = float(close.max()), close.idxmax()
    a_last = float(adj.iloc[-1])

    def ret(since, years=1):
        """Total return since a date (annualized over `years`), None if the fund is younger."""
        before = adj[adj.index <= since]
        if not len(before) or adj.index[0] > since:
            return None
        return (a_last / float(before.iloc[-1])) ** (1 / years) - 1

    def event_dd(start, end):
        """(fall, high day, low day) inside the window, or (None, None, None) before the fund's launch."""
        w = close[(close.index >= start) & (close.index <= end)]
        if close.index[0] > pd.Timestamp(start) or not len(w):
            return None, None, None
        dd = w / w.cummax() - 1
        low_day = dd.idxmin()
        return float(dd.min()), w[:low_day].idxmax(), low_day

    recent = close[close.index > last_day - pd.DateOffset(years=15)]

    return dict(
        since=close.index[0],
        events=[event_dd(a, b) for _, a, b in EVENTS],
        last=last, last_day=last_day, change=last / float(close.iloc[-2]) - 1,
        high=high, high_day=high_day, drawdown=last / high - 1, days=(last_day - high_day).days,
        # Maximum drawdown: the largest fall from a running closing high, over the fund's whole history.
        mdd=float((close / close.cummax() - 1).min()),
        mdd_day=(close / close.cummax() - 1).idxmin(),  # the trough: when the largest fall bottomed out
        # The same over the last 15 years only, so funds launched in 2010 compare on one period.
        mdd15=float((recent / recent.cummax() - 1).min()),
        mdd15_day=(recent / recent.cummax() - 1).idxmin(),
        ytd=ret(pd.Timestamp(last_day.year - 1, 12, 31)),
        y1=ret(last_day - pd.DateOffset(years=1)),
        ann={n: ret(last_day - pd.DateOffset(years=n), n) for n in YEARS},
    )


def day(d, year=False):
    return f"{d:%b} {d.day}" + (f", {d.year}" if year else "")  # no %-d: it fails on Windows


def heat(v, first=False):
    """A drawdown cell shaded red by depth (heatmap): 0% clear, -100% darkest."""
    g = " g" if first else ""
    if v is None:
        return f'<td class="ht{g}">—</td>'
    a = min(abs(v), 1) * 0.85
    ink = "#fff" if a > 0.45 else "inherit"
    return f'<td class="ht{g}" style="background:rgba(192,57,43,{a:.2f});color:{ink}">{pct(v)}</td>'


def era(day):
    """Name of the sell-off a date falls in (MDD trough), else the month, e.g. 2009Mar."""
    for name, start, end in EVENTS:
        if pd.Timestamp(start) <= day <= pd.Timestamp(end):
            return name
    return f"{day.year}{day:%b}"


def pct(v):
    """Percent with its sign and a real minus sign."""
    return "—" if v is None else f"{v * 100:+.1f}%".replace("-", "−")


def main():
    rows, ev_rows, as_of = [], [], None
    up = lambda v: "dn" if (v or 0) < 0 else "up"
    for symbol, label in SERIES:
        s = stats(symbol)
        as_of = s["last_day"]
        h = s["high_day"]
        name = f'<th title="{label}">{symbol}</th>'
        detail = (f'<td class="g dt"><a href="{DETAIL[symbol]}" title="What if you bought each time {symbol} halved?">Halvings ↗</a></td>'
                  if symbol in DETAIL else '<td class="g dt"></td>')
        since = f'<td>{s["since"].year}</td>'
        events = "".join(heat(v, first=k == 0) for k, (v, _, _) in enumerate(s["events"]))
        if symbol == "SPY":
            spy_days = [(a, b) for _, a, b in s["events"]]  # SPY's high day and low day in each sell-off
        main_cells = (
            f'<td>{s["last"]:,.2f}</td><td class="{up(s["change"])}">{pct(s["change"])}</td>'
            f'<td class="g">{s["high"]:,.2f}</td><td>{h.month}/{h.day}/{h.year % 100:02d}</td>'
            + "".join(f'<td class="{"g " if k < 2 else ""}{up(v)}">{pct(v)}</td>'
                      for k, v in enumerate([s["ytd"], s["y1"]] + [s["ann"][n] for n in YEARS]))
            + f'<td class="g {up(s["drawdown"] + 0.0005)}">{pct(s["drawdown"])}</td>'
            f'<td class="g dn">{pct(s["mdd"])}</td><td class="wh">{era(s["mdd_day"])}</td>'
            f'<td class="g dn">{pct(s["mdd15"])}</td><td class="wh">{era(s["mdd15_day"])}</td>' + detail)
        rows.append(f"<tr>{name}{main_cells}</tr>")
        ev_rows.append(f"<tr>{name}{since}{events}</tr>")
        print(symbol, f'{s["last"]:.2f}', s["last_day"].date(), "high", f'{s["high"]:.2f}', h.date(),
              "drawdown", pct(s["drawdown"]))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sub_main = ('<th class="g">P</th><th>Day</th>'
                '<th class="g">1Y</th>' + "".join(f"<th>{n}Y</th>" for n in YEARS)
                + '<th class="g" title="Last close vs. the all-time high">Now</th>'
                # each MDD heading spans its two columns: the fall and the sell-off it bottomed in
                '<th colspan="2" class="g" title="Largest fall from a high since the fund began">MDD, all</th>'
                '<th colspan="2" class="g" title="Largest fall from a high in the last 15 years">MDD, 15Y</th>')
    top_main = ('<th colspan="2" class="g">All-time high</th>'
                '<th rowspan="2" class="g">YTD</th>'
                f'<th colspan="{1 + len(YEARS)}" class="g">Annualized return</th>'
                '<th colspan="5" class="g">Drawdown</th>'
                '<th rowspan="2" class="g" title="Detail pages"><small style="display:inline;font-size:.8em;opacity:1">Detail</small></th>')
    sub_events = "".join(f'<th class="ev{" g" if k == 0 else ""}">{n}</th>' for k, (n, _, _) in enumerate(EVENTS))
    # Two small rows above the funds: when SPY's fall in each sell-off began (its high) and ended (its low).
    cells = {"From": [f"{a.year} {a:%b} {a.day}" for a, _ in spy_days],  # e.g. 2000 Oct 9
             "To": [f"~{b.year} {b:%b} {b.day}" for _, b in spy_days],
             "Length": [f"{(b - a).days:,} days" for a, b in spy_days]}
    period_rows = "".join(f'<tr class="per"><th>{label}</th><td></td>'
                          + "".join(f'<td{" class=g" if k == 0 else ""}>{c}</td>' for k, c in enumerate(v)) + "</tr>"
                          for label, v in cells.items())
    # The theme gives every table display:inline-block and a forced scrollbar; undo that here.
    # One <div> around everything, so the page's markdown treats the snapshot as a single HTML block.
    html = f"""<!-- Written by _code/market_snapshot.py; do not edit by hand. Last run {stamp}. -->
<div class="mkt-box" markdown="0">
<h2 id="market-snapshot">📈 Market Snapshot (as of {day(as_of, True)})</h2>
<style>
table.mkt {{ display: table !important; overflow: visible !important; width: auto !important; max-width: 100%;
  border: 0; border-collapse: collapse; font-size: .9em; line-height: 1.25; margin: .3em 0 0;
  box-shadow: none !important; border-radius: 0; }}
.mkt th, .mkt td {{ padding: .25em .3em; text-align: right; white-space: nowrap; vertical-align: top;
  border: 0; box-shadow: none !important; }}
.mkt tr:nth-child(odd) td, .mkt tr:hover td {{ background: none; }}
.mkt thead th {{ font-weight: 600; vertical-align: bottom; }}
.mkt thead tr:last-child th {{ border-bottom: 1px solid rgba(128,128,128,.45); }}
.mkt tbody tr + tr th, .mkt tbody tr + tr td {{ border-top: 1px solid rgba(128,128,128,.15); }}
.mkt thead tr:first-child th, .mkt thead th[colspan] {{ text-align: center; }}
.mkt thead small {{ line-height: 1.15; }}
.mkt th.ev {{ width: 4.9em; text-align: center; }}  /* sell-off and MDD columns: one width */
.mkt tr.per th, .mkt tr.per td {{ font-size: .78em; font-weight: 400; opacity: .7; text-align: center; padding-top: 0; padding-bottom: 0; }}
.mkt tr.per th {{ text-align: left; }}
.mkt tbody tr.per + tr.per th, .mkt tbody tr.per + tr.per td {{ border-top: 0; }}
.mkt .g {{ padding-left: .7em; border-left: 1px solid rgba(128,128,128,.35) !important; }}  /* a line between column groups */
.mkt tbody th {{ text-align: left; }}
.mkt small {{ display: block; font-size: .85em; font-weight: 400; opacity: .7; }}
.mkt td {{ font-size: .88em; }}  /* numbers a step smaller than the labels */
.mkt .dn {{ color: #c0392b; }}
.mkt td.ht {{ text-align: center; border-top: 1px solid var(--bg, #fff) !important; }}  /* heatmap cells */
.mkt .up {{ color: #1a7a5e; }}
@media (max-width: 640px) {{ table.mkt {{ font-size: .53em; }} .mkt th, .mkt td {{ padding: .2em .06em; }}
  .mkt .g {{ padding-left: .25em; }} .mkt th.ev {{ width: 4em; }}
  .mkt tr.per th, .mkt tr.per td {{ font-size: .68em; }}
  .mkt td.wh {{ white-space: normal; }} }}  /* "Bear 2022" on two lines on phones */
.mkt-note {{ font-size: .72em; opacity: .7; margin: 0 0 1.2em; }}
.mkt td.dt {{ text-align: left; font-size: .8em; }}
.mkt td.dt a {{ text-decoration: none; }}
</style>
<table class="mkt">
<thead>
<tr><th rowspan="2"></th><th colspan="2">Close</th>{top_main}</tr>
<tr><th>P</th><th>1D</th>{sub_main}</tr>
</thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<table class="mkt">
<thead>
<tr><th rowspan="2"></th><th rowspan="2" title="First trading year">Since</th><th colspan="{len(EVENTS)}" class="g">Drawdown in major sell-offs</th>
</tr>
<tr>{sub_events}</tr>
</thead>
<tbody>
{period_rows}
{chr(10).join(ev_rows)}
</tbody>
</table>
<p class="mkt-note">Daily closes; returns include dividends; MDD = largest fall since launch (all) or in the last 15 years (15Y); From/To/Length = SPY's high, low, and days between in each sell-off; — = not yet launched. Detail = what if you bought each time the fund halved. Yahoo Finance, updated weekdays after the 4 pm ET close.</p>
</div>
"""
    out = ROOT / "_includes" / "market-snapshot.html"
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
