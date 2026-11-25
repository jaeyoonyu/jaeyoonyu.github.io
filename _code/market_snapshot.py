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
    rows = []
    for symbol, label in SERIES:
        s = stats(symbol)
        cls = "dn" if s["drawdown"] < -0.0005 else "up"
        rows.append(
            f'<tr><th>{symbol}<small>{label}</small></th>'
            f'<td>{s["last"]:,.2f}<small>{day(s["last_day"])}</small></td>'
            f'<td class="{"dn" if s["change"] < 0 else "up"}">{pct(s["change"])}</td>'
            f'<td>{s["high"]:,.2f}<small>{day(s["high_day"], True)}</small></td>'
            f'<td class="{cls}">{pct(s["drawdown"])}<small>{s["days"]} days since the high</small></td>'
            + "".join(f'<td class="{"dn" if (v or 0) < 0 else "up"}{" sep" if k == 0 else ""}">{pct(v)}</td>'
                      for k, v in enumerate([s["ytd"], s["y1"]] + [s["ann"][n] for n in YEARS]))
            + "</tr>"
        )
        print(symbol, f'{s["last"]:.2f}', s["last_day"].date(), "high", f'{s["high"]:.2f}', s["high_day"].date(),
              "drawdown", pct(s["drawdown"]))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = f"""<!-- Written by _code/market_snapshot.py; do not edit by hand. -->
<style>
.mkt {{ border-collapse: collapse; font-size: .88em; margin: .4em 0 .2em; width: auto; }}
.mkt th, .mkt td {{ padding: .3em .8em; text-align: right; white-space: nowrap; vertical-align: top; }}
.mkt thead th {{ font-weight: 600; border-bottom: 1px solid rgba(128,128,128,.4); }}
.mkt tbody th {{ text-align: left; }}
.mkt small {{ display: block; font-size: .8em; opacity: .65; }}
.mkt .dn {{ color: #c0392b; }}
.mkt .up {{ color: #1a7a5e; }}
.mkt .sep {{ border-left: 1px solid rgba(128,128,128,.35); }}
.mkt-wrap {{ overflow-x: auto; }}
.mkt-note {{ font-size: .78em; opacity: .7; margin: 0 0 1.2em; }}
</style>
<div class="mkt-wrap"><table class="mkt">
<thead><tr><th></th><th>Last close</th><th>1 day</th><th>All-time high (close)</th><th>Drawdown</th>
<th class="sep">YTD</th><th>1 year</th>{"".join(f"<th>{n} years<small>per year</small></th>" for n in YEARS)}</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table></div>
<p class="mkt-note">Drawdown = last close ÷ all-time closing high − 1.<br>
Returns are total returns (dividends reinvested); 3-20 years are annualized; — = the fund is younger than that.<br>
TQQQ and SOXL aim for 3× the daily move, so their long-run returns differ a lot from 3× the index.<br>
Closing prices from Yahoo Finance via FinanceDataReader; updated {stamp}, each weekday after the US market close.</p>
"""
    out = ROOT / "_includes" / "market-snapshot.html"
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
