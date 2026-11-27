"""Buying the halvings: QQQ and TQQQ detail pages linked from the market snapshot table.

Rule: when a fund closes 50% below its all-time high, buy $1,000; each time it halves again,
buy twice as much ($2,000 at -75%, $4,000 at -87.5%, $8,000 at -93.75%). Then hold until the
fund closes back at that all-time high. BUYS sets how many halvings each page uses: QQQ never
fell past -83%, so its page stops at two buys; TQQQ's goes to four.

Writes halving-qqq.md, halving-tqqq.md and their figures in assets/images/halving/.
Run from the repo root:  python _code/halving_strategy.py
Prices: Yahoo Finance via FinanceDataReader (adjusted closes, dividends reinvested).
TQQQ only exists since Feb 2010; before that it is rebuilt from QQQ (see SYNTH_NOTE).
"""
from datetime import datetime, timezone
from pathlib import Path

import FinanceDataReader as fdr
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "images" / "halving"
BUYS = {"QQQ": 2, "TQQQ": 4}  # how many halvings the rule buys on, per fund
RESET = "2003-01-01"  # a second investor who starts watching after the dot-com bust
ORDINAL = {2: "again", 3: "a third time", 4: "a fourth time", 5: "a fifth time"}
COUNT = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
FRACTION = {2: "a quarter", 3: "an eighth", 4: "a sixteenth", 5: "a thirty-second"}


def legs_for(n):
    """((fall from the high, dollars), ...): $1k at -50%, then twice the money at each new halving."""
    return tuple((1 - 0.5 ** k, 1000 * 2 ** (k - 1)) for k in range(1, n + 1))


def lvl(f):
    """-50%, -75%, -87.5%, -93.75%"""
    return "−" + f"{f * 100:.2f}".rstrip("0").rstrip(".") + "%"


def variants_for(n):
    """Rule variants compared on a page: the same levels with fewer buys, and all the money at -50%."""
    out = [(f"{k} buy{'s' if k > 1 else ''}" + (" (the rule)" if k == n else ""),
            " · ".join(f"${a // 1000}k at {lvl(f)}" for f, a in legs_for(k)), legs_for(k))
           for k in range(1, n + 1)]
    total = sum(a for _, a in legs_for(n))
    return out + [("Lump sum", f"all ${total // 1000}k at −50%", ((0.5, total),))]


# Approximate yearly average 3-month T-bill rate (%), for the cost of TQQQ's 3x leverage before 2010
TBILL = {1999: 4.6, 2000: 5.8, 2001: 3.4, 2002: 1.6, 2003: 1.0, 2004: 1.4, 2005: 3.2, 2006: 4.7,
         2007: 4.4, 2008: 1.4, 2009: 0.15, 2010: 0.14, 2011: 0.05, 2012: 0.09, 2013: 0.06, 2014: 0.03,
         2015: 0.05, 2016: 0.32, 2017: 0.93, 2018: 1.94, 2019: 2.06, 2020: 0.37, 2021: 0.04, 2022: 2.02,
         2023: 5.07, 2024: 4.97, 2025: 4.2, 2026: 3.8}
FEE = 0.0095  # TQQQ expense ratio
# Sell-off names, as in the market snapshot (by the year of the high it fell from)
NAMES = {1999: "Dot-com", 2000: "Dot-com", 2007: "GFC", 2018: "Q4 2018", 2020: "COVID",
         2021: "Bear 2022", 2024: "Tariffs", 2025: "Tariffs"}
COLORS = ["#b03a2e", "#e08a1e", "#2a78d4", "#1f9e74", "#d6532c", "#8a5cc9", "#6b6b6b", "#3b8ea5"]
LEG_COLORS = ["#e3a23b", "#d6532c", "#8e1f1f", "#4a0d0d"]

plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": .25, "font.size": 11, "text.parse_math": False,
                     "figure.facecolor": "white"})


def load(symbol):
    d = fdr.DataReader(symbol, "1999-01-01")
    now = pd.Timestamp.now(tz="America/New_York")
    if d.index[-1].date() == now.date() and now.hour < 16:  # a live price, not a close
        d = d.iloc[:-1]
    return d["Adj Close"].dropna(), d["Close"].dropna()


def synthetic_tqqq(qqq, tqqq):
    """3x QQQ's daily return minus TQQQ's costs (fee + 2x the T-bill rate + a spread), chained
    into real TQQQ at its launch. The spread is set so the rebuild matches real TQQQ's total
    return over 2010-today. Returns (series, spread, largest tracking gap)."""
    r = qqq.pct_change().dropna()
    rate = pd.Series(r.index.year.map(TBILL), index=r.index).astype(float) / 100
    t_r = tqqq.pct_change().dropna()
    c = t_r.index.intersection(r.index)
    target = float((1 + t_r.loc[c]).prod())

    def grow(s, idx):
        return (1 + 3 * r.loc[idx] - (FEE + 2 * (rate.loc[idx] + s)) / 252).cumprod()

    lo, hi = -0.05, 0.10
    for _ in range(60):  # bisection on the spread
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if grow(mid, c).iloc[-1] > target else (lo, mid)
    spread = (lo + hi) / 2
    gap = float((grow(spread, c) / (1 + t_r.loc[c]).cumprod() - 1).abs().max())
    syn = grow(spread, r.index)
    syn = pd.concat([pd.Series([1.0], index=[qqq.index[0]]), syn])
    start = tqqq.index[0]
    out = pd.concat([syn[syn.index < start], tqqq / tqqq.iloc[0] * syn[syn.index <= start].iloc[-1]])
    return out, spread, gap


def run(px, legs):
    """Every episode: from the first close at or below -50% of the all-time high to the first
    close back at that high (or today). Buys at the close of the first day each level is hit."""
    ath = px.cummax()
    res, k, n = [], 0, len(px)
    while k < n:
        if px.iloc[k] > ath.iloc[k] * (1 - legs[0][0]):
            k += 1
            continue
        peak = float(ath.iloc[k])
        peak_day = px[:px.index[k]][px[:px.index[k]] == peak].index[-1]
        buys, shares, inv, rows, j, leg = [], 0.0, 0.0, [], k, 0
        while j < n:
            p = float(px.iloc[j])
            while leg < len(legs) and p <= peak * (1 - legs[leg][0]):
                shares += legs[leg][1] / p
                inv += legs[leg][1]
                buys.append((px.index[j], p, legs[leg][1], legs[leg][0]))
                leg += 1
            rows.append((px.index[j], shares * p, inv))
            if p >= peak:
                break
            j += 1
        path = pd.DataFrame(rows, columns=["day", "value", "invested"]).set_index("day")
        under = path[path.value < path.invested]
        recovered = j < n
        res.append(dict(
            peak_day=peak_day, peak=peak, buys=buys, invested=inv, shares=shares, path=path,
            first=buys[0][0], end=path.index[-1], recovered=recovered, end_value=float(path.value.iloc[-1]),
            low=float(px[peak_day:path.index[-1]].min() / peak - 1),
            low_day=px[peak_day:path.index[-1]].idxmin(),
            worst=float((path.value / path.invested).min() - 1),
            worst_day=(path.value / path.invested).idxmin(),
            max_loss=float((path.invested - path.value).max()),
            # the last close below cost: after it, the position never showed a loss again
            last_under=under.index[-1] if len(under) else None,
            underwater=float((path.value < path.invested).mean()),
            now_value=shares * float(px.iloc[-1])))
        k = j + 1
    return res


def episodes(px, legs):
    """The dot-com episode for someone watching since 1999, then every episode for someone who
    started in 2003 (a 1999 holder would still be measuring from the March 2000 high)."""
    first = [e for e in run(px, legs) if e["peak_day"] < pd.Timestamp(RESET)]
    later = run(px[RESET:], legs)
    return first + later


def worst_txt(e):
    return "never below cost" if e["worst"] > -0.0005 else f"worst {pct(e['worst'])}"


def name(e):
    y = e["peak_day"].year
    return NAMES.get(y, f"{e['first'].year} sell-off")


def money(v):
    return f"${v:,.0f}"


def pct(v):
    return (f"{v * 100:+.2f}%" if v < -0.99 else f"{v * 100:+.1f}%").replace("-", "−")


def years(a, b):
    return (b - a).days / 365.25


def d(day):
    return f"{day:%b} {day.year}"


# ---------------------------------------------------------------- figures
def fig_history(px, eps, symbol, path, legs, synth_end=None):
    fig, ax = plt.subplots(figsize=(13, 6.2))
    if synth_end is not None:
        ax.semilogy(px[:synth_end].index, px[:synth_end], color="#b03a2e", lw=1,
                    label="Rebuilt 3x QQQ (before TQQQ existed)")
        ax.semilogy(px[synth_end:].index, px[synth_end:], color="#222", lw=1, label="TQQQ")
    else:
        ax.semilogy(px.index, px, color="#222", lw=1, label=symbol)
    for seg, first in ((px[:RESET], True), (px[RESET:], False)):
        a = seg.cummax()
        ax.semilogy(a.index, a, color="#999", ls="--", lw=.8, label="All-time high" if first else None)
        for (f, amt), c in zip(legs, LEG_COLORS):
            ax.semilogy(a.index, a * (1 - f), color=c, ls=":", lw=.9,
                        label=f"{lvl(f)} → buy ${amt:,}" if first else None)
    for i, e in enumerate(eps):
        c = COLORS[i % len(COLORS)]
        for day, p, amt, _ in e["buys"]:
            ax.scatter(day, p, marker="v", s={1000: 60, 2000: 120, 4000: 220, 8000: 340}.get(amt, 120), color=c,
                       edgecolor="k", lw=.6, zorder=6)
        if e["recovered"]:
            ax.scatter(e["end"], e["peak"], marker="*", s=220, color=c, edgecolor="k", lw=.6, zorder=6)
    ax.axvline(pd.Timestamp(RESET), color="#bbb", lw=.8)
    ax.text(pd.Timestamp(RESET) + pd.Timedelta(days=60), ax.get_ylim()[1] / 1.6,
            "high reset for a 2003 starter →", fontsize=9, color="#777")
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_minor_formatter(mt.NullFormatter())
    ax.set_ylabel("Price (log scale)" if synth_end is None else "Value, Mar 1999 = 1 (log scale)")
    ax.legend(frameon=False, fontsize=9.5, loc="lower right", ncol=2)
    sizes = " / ".join(f"${a // 1000}k" for _, a in legs)
    ax.set_title(f"▼ buys (size = {sizes})   ★ back at the all-time high", loc="left",
                 fontsize=12, color="#444")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def fig_episodes(eps, path):
    n = len(eps)
    cols = 2 if n > 1 else 1
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(13, 3.6 * rows), squeeze=False)
    for i, e in enumerate(eps):
        ax = axes[i // cols][i % cols]
        p = e["path"]
        c = COLORS[i % len(COLORS)]
        ax.plot(p.index, p.value, color=c, lw=1.3, marker="o" if len(p) < 30 else None, ms=4)
        ax.step(p.index, p.invested, where="post", color="k", lw=1.1)
        ax.fill_between(p.index, p.value, p.invested, where=p.value < p.invested, color="#d6532c", alpha=.18)
        ax.fill_between(p.index, p.value, p.invested, where=p.value >= p.invested, color="#1f9e74", alpha=.18)
        if p.value.max() / max(p.value.min(), 1e-9) > 60:
            ax.set_yscale("log")
        ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax.yaxis.set_minor_formatter(mt.NullFormatter())
        span = years(p.index[0], p.index[-1])
        if span > 2:
            loc, fmt = mdates.YearLocator(max(1, int(span // 5))), "%Y"
        elif span > .25:
            loc, fmt = mdates.MonthLocator(interval=max(1, int(span * 12 // 5))), "%b %Y"
        else:
            loc, fmt = mdates.DayLocator(interval=max(1, int(span * 365 // 5))), "%b %-d"
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
        status = (f"back at the high {d(e['end'])}: {money(e['end_value'])}" if e["recovered"]
                  else f"not back yet; today {money(e['end_value'])}")
        ax.set_title(f"{name(e)}: {money(e['invested'])} in, {worst_txt(e)}; {status}",
                     loc="left", fontsize=10.5, fontweight="bold")
    for j in range(n, rows * cols):
        axes[j // cols][j % cols].axis("off")
    fig.text(.01, .005, "Black step = money put in.  Line = what it was worth.  Red = below cost, green = above.",
             fontsize=9.5, color="#555")
    fig.tight_layout(rect=(0, .02, 1, 1))
    fig.savefig(path, dpi=110)
    plt.close(fig)


def fig_compare(cmp, variants, path):
    labels = list(cmp)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.6))
    x = np.arange(len(labels))
    w = .8 / len(variants)
    shades = ["#9bb7d9", "#e3a23b", "#d6532c", "#8e1f1f"][:len(variants) - 1] + ["#555"]
    for k, (vname, _, _) in enumerate(variants):
        m = [cmp[l][vname]["multiple"] for l in labels]
        dd = [-cmp[l][vname]["worst"] for l in labels]
        for ax, vals, fmt in ((a1, m, "×{:.2f}"), (a2, dd, "−{:.0%}")):
            xs = x + (k - (len(variants) - 1) / 2) * w
            ax.bar(xs, vals, w, color=shades[k], edgecolor="k", lw=.4, label=vname)
            for xx, v in zip(xs, vals):
                ax.text(xx, v, fmt.format(v), ha="center", va="bottom", fontsize=7.5 if len(variants) > 4 else 8)
    a1.axhline(1, color="k", lw=.8)
    a1.set_title("Value ÷ money put in (at the old high, or today)", loc="left", fontweight="bold")
    a2.set_title("Worst fall of the position below cost", loc="left", fontweight="bold")
    a2.yaxis.set_major_formatter(mt.PercentFormatter(1))
    a2.set_ylim(0, 1.12)
    for ax in (a1, a2):
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
    a1.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- page
CSS = """<style>
.hv table { display: table !important; overflow: visible !important; width: auto !important; max-width: 100%;
  border-collapse: collapse; font-size: .82em; line-height: 1.3; box-shadow: none !important; margin: .4em 0 1em; }
.hv th, .hv td { padding: .3em .45em; text-align: right; white-space: nowrap; border: 0; box-shadow: none !important; }
.hv tr:nth-child(odd) td, .hv tr:hover td { background: none; }
.hv thead th { border-bottom: 1px solid rgba(128,128,128,.45); vertical-align: bottom; }
.hv tbody tr + tr td, .hv tbody tr + tr th { border-top: 1px solid rgba(128,128,128,.15); }
.hv tbody th, .hv thead th:first-child { text-align: left; }
.hv .dn { color: #c0392b; } .hv .up { color: #1a7a5e; }
.hv .scroll { overflow-x: auto; }
.hv .rule { border-left: 4px solid #d6532c; padding: .5em .9em; margin: .8em 0 1.2em; background: rgba(214,83,44,.06); }
.hv .now { border-left: 4px solid #2a78d4; padding: .5em .9em; margin: .8em 0 1.2em; background: rgba(42,120,212,.06); }
.hv img { max-width: 100%; border: 1px solid rgba(128,128,128,.25); border-radius: 4px; }
.hv .note { font-size: .78em; opacity: .75; }
.hv td small, .hv th small { display: block; font-size: .85em; opacity: .75; font-weight: 400; }
.hv tbody th { vertical-align: top; } .hv td { vertical-align: top; }
@media (max-width: 640px) { .hv table { font-size: .66em; } .hv th, .hv td { padding: .25em .2em; } }
</style>"""


def cls(v):
    return "dn" if v < 0 else "up"


def episode_table(eps):
    head = ("<tr><th>Sell-off</th><th>Low</th><th class=wrap>Buys</th><th>Put in</th><th>Worst</th>"
            "<th>Above cost<br>for good</th><th>Back at high<br><small>years after 1st buy</small></th>"
            "<th>Worth then</th><th>Held to<br>today</th></tr>")
    rows = []
    for e in eps:
        buys = "<br>".join(f"${a // 1000}k {b:%b %Y}" for b, _, a, _ in e["buys"])
        if e["recovered"]:
            good = d(e["last_under"] + pd.Timedelta(days=1)) if e["last_under"] is not None else "at once"
            back = f"{d(e['end'])}<br><small>{years(e['first'], e['end']):.1f} yrs</small>"
        else:
            good = "not yet" if e["end_value"] < e["invested"] else "above now"
            back = f"not yet<br><small>{years(e['first'], e['end']):.1f}+ yrs</small>"
        mult = e["end_value"] / e["invested"]
        worst = ("<td>never below cost</td>" if e["worst"] > -0.0005 else
                 f"<td class=dn>{pct(e['worst'])}<br><small>{money(e['invested'] * (1 + e['worst']))} · "
                 f"{e['worst_day']:%b %Y}</small></td>")
        rows.append(
            f"<tr><th>{name(e)}<br><small>high {e['peak_day']:%b %Y}</small></th><td class=dn>{pct(e['low'])}</td>"
            f"<td>{buys}</td><td>{money(e['invested'])}</td>{worst}<td>{good}</td><td>{back}</td>"
            f"<td>{money(e['end_value'])}<br><small class={cls(mult - 1)}>×{mult:.2f}"
            f"{'' if e['recovered'] else ' today'}</small></td><td>{money(e['now_value'])}</td></tr>")
    return f'<div class="scroll"><table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'


def compare_table(cmp, variants):
    head = "<tr><th>Rule</th>" + "".join(f"<th>{l}</th>" for l in cmp) + "</tr>"
    rows = []
    for vname, desc, _ in variants:
        cells = "".join(
            f"<td>{money(c['invested'])} → {money(c['value'])} "
            f"<span class={cls(c['multiple'] - 1)}>(×{c['multiple']:.2f})</span><br>"
            f"<small>worst {pct(c['worst'])}</small></td>" for c in (cmp[l][vname] for l in cmp))
        rows.append(f"<tr><th>{vname}<br><small>{desc}</small></th>{cells}</tr>")
    return f'<div class="scroll"><table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'


def now_box(symbol, raw, legs):
    high, high_day, last = float(raw.max()), raw.idxmax(), float(raw.iloc[-1])
    levels = " · ".join(f"{lvl(f)} = <b>${high * (1 - f):,.2f}</b> (${a:,})" for f, a in legs)
    hit = [lvl(f) for f, _ in legs if raw[high_day:].min() <= high * (1 - f)]
    status = f"Already hit since the high: {', '.join(hit)}." if hit else "No buy level has been hit since this high."
    return (f'<div class="now"><b>Where {symbol} is now</b> ({raw.index[-1]:%b %-d, %Y}): ${last:,.2f}, '
            f"{pct(last / high - 1)} from its closing high of ${high:,.2f} ({high_day:%b %-d, %Y}).<br>"
            f"Buy levels from that high: {levels}. {status}</div>")


def build(symbol, px, raw, synth=None):
    n = BUYS[symbol]
    legs, variants = legs_for(n), variants_for(n)
    total = sum(a for _, a in legs)
    rule, lump = variants[n - 1][0], variants[-1][0]
    eps = episodes(px, legs)
    slug = symbol.lower()
    IMG.mkdir(parents=True, exist_ok=True)
    fig_history(px, eps, symbol, IMG / f"{slug}-history.png", legs, synth_end=None if synth is None else synth["end"])
    fig_episodes(eps, IMG / f"{slug}-episodes.png")

    # rule variants, on the episodes where the rule bought more than once (or the dot-com one)
    keep = [e for e in eps if len(e["buys"]) > 1 or e["peak_day"] < pd.Timestamp(RESET)]
    if len(keep) < 2:
        keep = eps
    cmp = {}
    for e in keep:
        label = name(e)
        cmp[label] = {}
        src = px if e["peak_day"] < pd.Timestamp(RESET) else px[RESET:]
        for vname, _, vlegs in variants:
            v = [x for x in run(src, vlegs) if x["peak_day"] == e["peak_day"]][0]
            cmp[label][vname] = dict(invested=v["invested"], value=v["end_value"], buys=len(v["buys"]),
                                     multiple=v["end_value"] / v["invested"], worst=v["worst"])
    fig_compare(cmp, variants, IMG / f"{slug}-compare.png")

    done = [e for e in eps if e["recovered"]]
    open_ = [e for e in eps if not e["recovered"]]
    longest = max(eps, key=lambda e: years(e["first"], e["end"]))
    worst = min(eps, key=lambda e: e["worst"])
    nth = {2: "second", 3: "third", 4: "fourth", 5: "fifth"}
    later = [f"the {nth[k]} ({money(a)}, at {lvl(f)}) in **{sum(len(e['buys']) >= k for e in eps)}**"
             for k, (f, a) in enumerate(legs[1:], start=2)]
    bullets = [
        f"The rule fired in **{len(eps)}** sell-offs: the first buy ({money(1000)}) every time, "
        + (", ".join(later[:-1]) + ", and " + later[-1] if len(later) > 1 else "and " + later[0]) + ".",
    ]
    if done:
        mult = [e["end_value"] / e["invested"] for e in done]
        yrs = [years(e["first"], e["end"]) for e in done]
        bullets.append(
            f"In the **{len(done)}** that ended, the money came back as ×{min(mult):.2f} to ×{max(mult):.2f} by the day "
            f"{symbol} regained its old high, which took {min(yrs):.1f} to {max(yrs):.1f} years from the first buy "
            f"(median {np.median(yrs):.1f}).")
    bullets.append(
        f"The worst ride was **{name(worst)}**: {money(worst['invested'])} put in fell to "
        f"{money(worst['invested'] * (1 + worst['worst']))} ({pct(worst['worst'])}) in {worst['worst_day']:%B %Y}.")
    if not longest["recovered"]:
        bullets.append(
            f"**{name(longest)}** has still not reached its old high, {years(longest['first'], longest['end']):.1f} "
            f"years after the first buy: the position is worth {money(longest['end_value'])} on "
            f"{money(longest['invested'])} put in, and it spent {longest['underwater']:.0%} of those days below cost.")
    else:
        bullets.append(f"The longest wait was **{name(longest)}**: {years(longest['first'], longest['end']):.1f} years.")
    multi = [l for l in cmp if cmp[l][rule]["buys"] > 1]
    if multi:
        l = max(multi, key=lambda l: cmp[l][rule]["multiple"] - cmp[l][lump]["multiple"])
        r, ls = cmp[l][rule], cmp[l][lump]
        fr = [FRACTION[k] for k in range(2, r["buys"] + 1)]
        fr = fr[0] if len(fr) == 1 else ", ".join(fr[:-1]) + " and " + fr[-1]
        bullets.append(
            f"Doubling down helps most when the fall keeps going. In {l}, the {COUNT[n]}-step rule turned "
            f"{money(r['invested'])} into ×{r['multiple']:.2f}, against ×{ls['multiple']:.2f} for putting "
            f"all {money(total)} in at −50%: the later, larger buys come in at {fr} of the high.")
    if open_ and open_[-1]["first"].year >= datetime.now().year - 1 and open_[-1] is not longest:
        e = open_[-1]
        bullets.append(f"An episode is open now: the first buy was on {e['first']:%b %-d, %Y}; see the box above for the next levels.")

    synth_txt = ""
    if synth is not None:
        synth_txt = (
            f"\n**Before February 2010, TQQQ is rebuilt.** Each day's QQQ return × 3, minus TQQQ's {FEE:.2%} fee and the "
            f"cost of borrowing twice the money (the year's 3-month T-bill rate + {synth['spread']:.2%}, the spread that "
            f"makes the rebuild match real TQQQ's total return since 2010; the two paths never drift more than "
            f"{synth['gap']:.0%} apart). Borrowing cost about {FEE + 2 * (TBILL[2000] / 100 + synth['spread']):.0%} a year "
            f"in 2000 and {FEE + 2 * (TBILL[2007] / 100 + synth['spread']):.0%} in 2007, so the rebuild is not kind to "
            f"those years. It is an estimate, not a fund you could have bought.\n")

    other = "tqqq" if slug == "qqq" else "qqq"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    page = f"""---
layout: page
title: "{symbol}: Buying the Halvings"
permalink: /halving-{slug}/
---
<!-- Written by _code/halving_strategy.py; do not edit by hand. Last run {stamp}. -->
<div class="hv" markdown="1">
{CSS}

What happens if you buy {symbol} only after it has been cut in half, and buy more each time it halves again?

<div class="rule"><b>The rule.</b> When {symbol} closes 50% below its all-time high, buy <b>$1,000</b>.
{" ".join(f"If it halves {ORDINAL[k]} ({lvl(f)} from the high), buy <b>{money(a)}</b>." for k, (f, a) in enumerate(legs[1:], start=2))}
Hold until {symbol} closes back at that high. At most {money(total)} goes in per sell-off.</div>

{now_box(symbol, raw, legs)}

## Key findings

{chr(10).join("- " + b for b in bullets)}

## Every sell-off that triggered the rule

{episode_table(eps)}
<p class="note">Worst = lowest value of the position against the money in at that point. Above cost for good = the day after the last close below cost.
Back at high = first close at or above the all-time high the fall started from. Worth then = the position on that day (or today, if not back yet).
If held to today = the same shares valued at the last close. The dot-com row is for someone watching since 1999; every later row is for someone who
started in 2003, after the bust (a 1999 holder still measures from the March 2000 high, so for them the later sell-offs are not new signals).</p>

## The whole history

![{symbol} with the buy levels](/assets/images/halving/{slug}-history.png)

## Each sell-off, dollar by dollar

![The position in each sell-off](/assets/images/halving/{slug}-episodes.png)

## Is doubling down better than the alternatives?

Same trigger levels, different amounts: {", ".join(("only the first buy" if k == 1 else f"the first {COUNT[k]}") for k in range(1, n))}, {"both" if n == 2 else "all " + COUNT[n]}, or all {money(total)} at once at −50%.

![Rule variants compared](/assets/images/halving/{slug}-compare.png)

{compare_table(cmp, variants)}

## How this was computed
{synth_txt}
- Daily adjusted closes from Yahoo Finance (dividends reinvested), {px.index[0]:%B %Y} to {px.index[-1]:%B %-d, %Y}. Buys happen at the close of the first day a level is reached; a gap down can fill a level below it.
- No taxes, trading costs, or interest on cash waiting to be invested.
- A backward look at a handful of episodes, not advice. The sample is small, and the dot-com bust shows how long "eventually" can be.

See also: [{other.upper()}: Buying the Halvings](/halving-{other}/) · [Market snapshot](/test/#market-snapshot)

</div>
"""
    (ROOT / f"halving-{slug}.md").write_text(page, encoding="utf-8")
    for e in eps:
        print(symbol, name(e), e["peak_day"].date(), [(b.date(), a) for b, _, a, _ in e["buys"]],
              money(e["invested"]), pct(e["worst"]), "recovered" if e["recovered"] else "open",
              e["end"].date(), money(e["end_value"]))


def main():
    qqq, qqq_raw = load("QQQ")
    tqqq, tqqq_raw = load("TQQQ")
    syn, spread, gap = synthetic_tqqq(qqq, tqqq)
    build("QQQ", qqq, qqq_raw)
    build("TQQQ", syn, tqqq_raw, synth=dict(end=tqqq.index[0], spread=spread, gap=gap))


if __name__ == "__main__":
    main()
