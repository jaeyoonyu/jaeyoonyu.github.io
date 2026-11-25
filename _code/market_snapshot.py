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

    return dict(
        last=last, last_day=last_day, change=last / float(close.iloc[-2]) - 1,
        high=high, high_day=high_day, drawdown=last / high - 1, days=(last_day - high_day).days,
        # Maximum drawdown: the largest fall from a running closing high, over the fund's whole history.
        mdd=float((close / close.cummax() - 1).min()),
        ytd=ret(pd.Timestamp(last_day.year - 1, 12, 31)),
        y1=ret(last_day - pd.DateOffset(years=1)),
        ann={n: ret(last_day - pd.DateOffset(years=n), n) for n in YEARS},
    )


def day(d, year=False):
    return f"{d:%b} {d.day}" + (f", {d.year}" if year else "")  # no %-d: it fails on Windows


def pct(v):
    """Percent without the % sign (the header says %), with a real minus sign."""
    return "—" if v is None else f"{v * 100:+.1f}".replace("-", "−")


def main():
    rows, as_of = [], None
    up = lambda v: "dn" if (v or 0) < 0 else "up"
    for symbol, label in SERIES:
        s = stats(symbol)
        as_of = s["last_day"]
        h = s["high_day"]
        rows.append(
            f'<tr><th title="{label}">{symbol}</th>'
            f'<td>{s["last"]:,.2f}</td><td class="{up(s["change"])}">{pct(s["change"])}</td>'
            f'<td class="g">{s["high"]:,.2f}</td><td>{h.month}/{h.day}/{h.year % 100:02d}</td>'
            f'<td class="g {up(s["drawdown"] + 0.0005)}">{pct(s["drawdown"])}</td><td class="dn">{pct(s["mdd"])}</td>'
            + "".join(f'<td class="{"g " if k < 2 else ""}{up(v)}">{pct(v)}</td>'
                      for k, v in enumerate([s["ytd"], s["y1"]] + [s["ann"][n] for n in YEARS]))
            + "</tr>")
        print(symbol, f'{s["last"]:.2f}', s["last_day"].date(), "high", f'{s["high"]:.2f}', h.date(),
              "drawdown", pct(s["drawdown"]))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # The theme gives every table display:inline-block and a forced scrollbar; undo that here.
    html = f"""<!-- Written by _code/market_snapshot.py; do not edit by hand. Last run {stamp}. -->
<h2 id="market-snapshot">📈 Market Snapshot (as of {day(as_of, True)})</h2>
<style>
table.mkt {{ display: table !important; overflow: visible !important; width: 100% !important; max-width: 100%;
  border: 0; border-collapse: collapse; font-size: .8em; line-height: 1.2; margin: .3em 0 .2em;
  box-shadow: none !important; border-radius: 0; }}
.mkt th, .mkt td {{ padding: .25em .3em; text-align: right; white-space: nowrap; vertical-align: top;
  border: 0; box-shadow: none !important; }}
.mkt tr:nth-child(odd) td, .mkt tr:hover td {{ background: none; }}
.mkt thead th {{ font-weight: 600; vertical-align: bottom; }}
.mkt thead tr:first-child th {{ text-align: center; }}
.mkt .g {{ padding-left: .9em; }}  /* a gap, not a line, between column groups */
.mkt tbody th {{ text-align: left; }}
.mkt small {{ display: block; font-size: .85em; font-weight: 400; opacity: .7; }}
.mkt .dn {{ color: #c0392b; }}
.mkt .up {{ color: #1a7a5e; }}
@media (max-width: 640px) {{ table.mkt {{ font-size: .6em; }} .mkt th, .mkt td {{ padding: .2em .12em; }}
  .mkt .g {{ padding-left: .5em; }} }}
.mkt-note {{ font-size: .72em; opacity: .7; margin: 0 0 1.2em; }}
</style>
<table class="mkt">
<thead>
<tr><th rowspan="2"></th><th colspan="2">Close</th><th colspan="2" class="g">All-time high</th>
<th colspan="2" class="g">Drawdown (%)</th><th rowspan="2" class="g">YTD<br>(%)</th>
<th colspan="{1 + len(YEARS)}" class="g">Annualized return (%)</th></tr>
<tr><th>P</th><th>1D %</th><th class="g">P</th><th>Day</th>
<th class="g" title="From the all-time high">Now</th><th title="Largest fall from a high since the fund began">MDD</th>
<th class="g">1Y</th>{"".join(f"<th>{n}Y</th>" for n in YEARS)}</tr>
</thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<p class="mkt-note">Closing prices; returns include dividends; MDD = largest fall from a high since the fund began; Yahoo Finance, updated weekdays after the 4 pm ET close.</p>
"""
    out = ROOT / "_includes" / "market-snapshot.html"
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
