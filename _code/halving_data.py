"""Write assets/data/halving-lab.json, the data behind assets/tools/halving-lab.html.

Daily total-return index (adjusted closes, dividends reinvested) for the funds in the market
snapshot, each rebased to 100 on its first day and rounded to 5 significant digits. The two 3x
funds also carry a rebuilt history from before they existed (3x their 1x fund each day, minus
fees and the cost of borrowing; see halving_strategy.synthetic), so the lab can reach 2000.
Only the last close and the closing high are kept as prices (the lab shows buy levels in dollars).

Run from the repo root:  python _code/halving_data.py
"""
import json
import sys
from pathlib import Path

import FinanceDataReader as fdr
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from halving_strategy import TBILL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "data" / "halving-lab.json"
# symbol: (what it tracks, 1x fund(s) to rebuild it from before launch, yearly fee)
# SOXL follows the semiconductor index SOXX tracked (PHLX SOX until 2021), so it is rebuilt from
# SOXX; SMH (a different, more concentrated index) only fills the year before SOXX began in Jul 2001.
FUNDS = {"SPY": ("S&P 500", None, None),
         "QQQ": ("Nasdaq-100", None, None),
         "TQQQ": ("Nasdaq-100, 3× daily", ("QQQ",), 0.0095),
         "SMH": ("Semiconductors", None, None),
         "SOXL": ("Semiconductors, 3× daily", ("SOXX", "SMH"), 0.0075)}


def load(symbol):
    d = fdr.DataReader(symbol, "1993-01-01")
    now = pd.Timestamp.now(tz="America/New_York")
    if d.index[-1].date() == now.date() and now.hour < 16:  # a live price, not a close
        d = d.iloc[:-1]
    return d["Adj Close"].dropna(), d["Close"].dropna()


def synthetic(base, real, fee):
    """3x the base fund's daily return minus (fee + 2x (T-bill + spread)) / 252, chained into the real
    fund at its launch. The spread makes the rebuild match the real fund's total return since launch.
    Returns (series, spread, largest gap between rebuild and real fund)."""
    r = base.pct_change().dropna()
    rate = pd.Series(r.index.year.map(TBILL), index=r.index).astype(float) / 100
    rr = real.pct_change().dropna()
    c = rr.index.intersection(r.index)
    target = float((1 + rr.loc[c]).prod())

    def grow(s, idx):
        return (1 + 3 * r.loc[idx] - (fee + 2 * (rate.loc[idx] + s)) / 252).cumprod()

    lo, hi = -0.1, 0.2
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if grow(mid, c).iloc[-1] > target else (lo, mid)
    spread = (lo + hi) / 2
    gap = float((grow(spread, c) / (1 + rr.loc[c]).cumprod() - 1).abs().max())
    syn = pd.concat([pd.Series([1.0], index=[base.index[0]]), grow(spread, r.index)])
    start = real.index[0]
    out = pd.concat([syn[syn.index < start], real / real.iloc[0] * syn[syn.index <= start].iloc[-1]])
    return out, spread, gap


def chain(main, filler):
    """main's daily moves, with filler's moves for the days before main began."""
    early = filler[filler.index <= main.index[0]]
    return pd.concat([early.iloc[:-1] / early.iloc[-1] * main.iloc[0], main])


def sig(v):
    return float(f"{v:.5g}")


def main():
    adj, raw = {}, {}
    for s in list(FUNDS) + ["SOXX"]:
        adj[s], raw[s] = load(s)
    days = sorted(set().union(*[adj[s].index for s in FUNDS]))
    days = pd.DatetimeIndex(days)
    t0 = days[0]
    out = {"asof": f"{days[-1]:%Y-%m-%d}", "start": f"{t0:%Y-%m-%d}",
           "days": [int((d - t0).days) for d in days], "funds": {}}
    for s, (label, base, fee) in FUNDS.items():
        series, info = adj[s], {}
        if base:
            src = adj[base[0]] if len(base) == 1 else chain(adj[base[0]], adj[base[1]])
            series, spread, gap = synthetic(src, adj[s], fee)
            info = {"rebuilt_from": base[0], "fee": fee, "spread": round(spread, 4), "gap": round(gap, 3)}
            if len(base) > 1:
                info["filled_from"] = base[1]
                info["filled_until"] = f"{adj[base[0]].index[0]:%Y-%m-%d}"
        series = series.reindex(days)
        first = int(days.get_loc(series.first_valid_index()))
        vals = series.iloc[first:].ffill()
        vals = vals / vals.iloc[0] * 100
        r = raw[s]
        out["funds"][s] = dict(
            label=label, first=first, real_first=int(days.get_loc(adj[s].index[0])),
            v=[sig(x) for x in vals], last=round(float(r.iloc[-1]), 2),
            high=round(float(r.max()), 2), high_day=f"{r.idxmax():%Y-%m-%d}", **info)
        print(s, label, f"from {days[first]:%Y-%m-%d}", info)
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(OUT, f"{OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
