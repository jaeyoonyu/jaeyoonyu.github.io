"""Write _includes/market-snapshot.html: S&P 500 and QQQ, last close, all-time high, drawdown.

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
# (FinanceDataReader symbol, label, first date to read: 1971 is the earliest Windows can parse)
SERIES = [("US500", "S&P 500", "1971-01-01"), ("QQQ", "QQQ (Nasdaq-100 ETF)", "1999-01-01")]


def stats(symbol, start):
    close = fdr.DataReader(symbol, start)["Close"].dropna()
    # Before the 4 pm Eastern close, today's row is a live price, not a close: drop it.
    now = pd.Timestamp.now(tz="America/New_York")
    if close.index[-1].date() == now.date() and now.hour < 16:
        close = close.iloc[:-1]
    last, last_day = float(close.iloc[-1]), close.index[-1]
    high, high_day = float(close.max()), close.idxmax()
    year_start = close[close.index.year < last_day.year]
    ytd_base = float(year_start.iloc[-1]) if len(year_start) else None
    year = close[close.index > last_day - pd.Timedelta(days=365)]
    return dict(
        last=last, last_day=last_day, change=last / float(close.iloc[-2]) - 1,
        high=high, high_day=high_day, drawdown=last / high - 1, days=(last_day - high_day).days,
        ytd=last / ytd_base - 1 if ytd_base else None,
        high52=float(year.max()), low52=float(year.min()),
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
    for symbol, label, start in SERIES:
        s = stats(symbol, start)
        cls = "dn" if s["drawdown"] < -0.0005 else "up"
        rows.append(
            f'<tr><th>{label}</th>'
            f'<td>{s["last"]:,.2f}<small>{day(s["last_day"])}</small></td>'
            f'<td class="{"dn" if s["change"] < 0 else "up"}">{pct(s["change"])}</td>'
            f'<td>{s["high"]:,.2f}<small>{day(s["high_day"], True)}</small></td>'
            f'<td class="{cls}">{pct(s["drawdown"])}<small>{s["days"]} days since the high</small></td>'
            f'<td class="{"dn" if (s["ytd"] or 0) < 0 else "up"}">{pct(s["ytd"])}</td>'
            f'<td>{s["low52"]:,.2f} – {s["high52"]:,.2f}</td></tr>'
        )
        print(label, f'{s["last"]:.2f}', s["last_day"].date(), "high", f'{s["high"]:.2f}', s["high_day"].date(),
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
.mkt-note {{ font-size: .78em; opacity: .7; margin: 0 0 1.2em; }}
</style>
<table class="mkt">
<thead><tr><th></th><th>Last close</th><th>1 day</th><th>All-time high (close)</th><th>Drawdown</th><th>YTD</th><th>52-week range</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<p class="mkt-note">Drawdown = last close ÷ all-time closing high − 1.<br>
Closing prices from Yahoo Finance via FinanceDataReader; updated {stamp}, each weekday after the US market close.</p>
"""
    out = ROOT / "_includes" / "market-snapshot.html"
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
