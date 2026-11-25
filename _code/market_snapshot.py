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
SERIES = [("SPY", "S&P 500"), ("QQQ", "Nasdaq-100"), ("SMH", "Semiconductors"),
          ("TQQQ", "Nasdaq-100, 3× daily"), ("SOXL", "Semiconductors, 3× daily")]
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
        ytd=ret(pd.Timestamp(last_day.year - 1, 12, 31)),
        y1=ret(last_day - pd.DateOffset(years=1)),
        ann={n: ret(last_day - pd.DateOffset(years=n), n) for n in YEARS},
    )


def day(d, year=False):
    return f"{d:%b} {d.day}" + (f", {d.year}" if year else "")  # no %-d: it fails on Windows


def pct(v, sign=True):
    if v is None:
        return "—"
    s = f"{v * 100:+.1f}%" if sign else f"{v * 100:.1f}%"
    return s.replace("-", "−")


def main():
    rows, price_rows, ret_rows, as_of = [], [], [], None
    for symbol, label in SERIES:
        s = stats(symbol)
        as_of = s["last_day"]
        up = lambda v: "dn" if (v or 0) < 0 else "up"
        name = f'<th>{symbol}<small>{label}</small></th>'
        prices = (f'<td>{s["last"]:,.2f}<small class="{up(s["change"])}">{pct(s["change"])}</small></td>'
                  f'<td>{s["high"]:,.2f}<small>{day(s["high_day"], True)}</small></td>'
                  f'<td class="{up(s["drawdown"] + 0.0005)}">{pct(s["drawdown"])}<small>{s["days"]} days</small></td>')
        rets = "".join(f'<td class="{up(v)}{" sep" if k == 0 else ""}">{pct(v)}</td>'
                       for k, v in enumerate([s["ytd"], s["y1"]] + [s["ann"][n] for n in YEARS]))
        rows.append(f"<tr>{name}{prices}{rets}</tr>")
        price_rows.append(f"<tr>{name}{prices}</tr>")
        ret_rows.append(f"<tr>{name}{rets.replace(' sep', '')}</tr>")
        print(symbol, f'{s["last"]:.2f}', s["last_day"].date(), "high", f'{s["high"]:.2f}', s["high_day"].date(),
              "drawdown", pct(s["drawdown"]))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    price_head = "<th>Close<small>1 day</small></th><th>All-time high<small>date</small></th><th>Drawdown<small>since high</small></th>"
    ret_head = "".join(f"<th>{n}Y</th>" for n in YEARS)
    # The theme gives every table display:inline-block and a forced scrollbar; undo that here.
    html = f"""<!-- Written by _code/market_snapshot.py; do not edit by hand. -->
<h2 id="market-snapshot">📈 Market Snapshot (as of {day(as_of, True)})</h2>
<style>
table.mkt {{ display: table !important; overflow: visible !important; width: 100% !important; max-width: 100%;
  border-collapse: collapse; font-size: .78em; line-height: 1.25; margin: .3em 0 .2em; box-shadow: none; }}
.mkt th, .mkt td {{ padding: .25em .35em; text-align: right; white-space: nowrap; vertical-align: top; box-shadow: none; }}
.mkt tr:nth-child(odd) td, .mkt tr:hover td {{ background: none; }}
.mkt thead th {{ font-weight: 600; border-bottom: 1px solid rgba(128,128,128,.4); vertical-align: bottom; }}
.mkt tbody tr + tr th, .mkt tbody tr + tr td {{ border-top: 1px solid rgba(128,128,128,.15); }}
.mkt tbody th {{ text-align: left; }}
.mkt small {{ display: block; font-size: .82em; font-weight: 400; opacity: .7; }}
.mkt .dn {{ color: #c0392b; }}
.mkt .up {{ color: #1a7a5e; }}
.mkt .sep {{ border-left: 1px solid rgba(128,128,128,.35); }}
table.mkt.mkt-phone {{ display: none !important; }}
@media (max-width: 640px) {{  /* phones: prices and returns as two tables */
  table.mkt.mkt-desk {{ display: none !important; }}
  table.mkt.mkt-phone {{ display: table !important; }}
  table.mkt {{ font-size: .74em; }}
}}
.mkt-note {{ font-size: .72em; opacity: .7; margin: 0 0 1.2em; line-height: 1.4; }}
</style>
<table class="mkt mkt-desk">
<thead><tr><th></th>{price_head}<th class="sep">YTD</th><th>1Y</th>{ret_head}</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<table class="mkt mkt-phone">
<thead><tr><th></th>{price_head}</tr></thead>
<tbody>
{chr(10).join(price_rows)}
</tbody>
</table>
<table class="mkt mkt-phone">
<thead><tr><th></th><th>YTD</th><th>1Y</th>{ret_head}</tr></thead>
<tbody>
{chr(10).join(ret_rows)}
</tbody>
</table>
<p class="mkt-note">Drawdown = close ÷ all-time closing high − 1.<br>
Total returns (dividends reinvested); 3Y-20Y are per year; — = the fund is younger.<br>
TQQQ and SOXL aim for 3× the daily move, not 3× the long-run return.<br>
Yahoo Finance closes via FinanceDataReader; updated each weekday after the 4 pm Eastern close (last run {stamp}).</p>
"""
    out = ROOT / "_includes" / "market-snapshot.html"
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
