"""Build ratios.md: quarterly margins, current ratio, NI vs. OCF, and FCF per ticker.

Run from the repo root:  python _code/ratios.py
Data: SEC EDGAR companyfacts API (the XBRL numbers each company tags in its
10-Qs and 10-Ks). Flows reported only as year-to-date or annual totals are
turned into quarters by differencing: Q = YTD - prior YTD of the same year.
"""
import json
import time
from datetime import datetime
from pathlib import Path

from fundamentals import GROUPS, fye_mmdd, get_json, month_end

FIRST_COL, LAST_COL = (2022, 1), (2026, 2)  # calendar quarters shown, (year, q)
TAGS = {
    "rev": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
            "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax",
            "RevenuesNetOfInterestExpense"],
    "gp": ["GrossProfit"],
    "cost": ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"],
    "ni": ["NetIncomeLoss", "ProfitLoss"],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets",
              "PaymentsForCapitalImprovements"],
    "ca": ["AssetsCurrent"],
    "cl": ["LiabilitiesCurrent"],
    # Delta stopped tagging a capex total in 2026; its two parts add up to it.
    "flight": ["PaymentsForFlightEquipment"],
    "other_pp": ["PaymentsToAcquireOtherProductiveAssets"],
}
INSTANT = {"ca", "cl"}


def days(start, end):
    return (datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days


def facts_for(gaap, tag):
    """[(start or None, end, value)] for one tag in USD, the latest filing winning."""
    out = {}
    facts = gaap.get(tag, {}).get("units", {}).get("USD", [])
    for f in sorted(facts, key=lambda f: f["filed"]):
        if f.get("form", "").startswith(("10-K", "10-Q")):
            out[(f.get("start"), f["end"])] = f["val"]
    return out


def flow_quarters(vals):
    """end -> (value, derived). Direct 12-16 week quarters first; otherwise the
    difference between consecutive year-to-date totals that share a start date."""
    out = {e: (v, False) for (s, e), v in vals.items() if s and 75 <= days(s, e) <= 120}
    by_start = {}
    for (s, e), v in vals.items():
        if s and days(s, e) <= 380:
            by_start.setdefault(s, []).append((e, v))
    for s, ytd in by_start.items():
        ytd.sort()
        for (e0, v0), (e1, v1) in zip(ytd, ytd[1:]):
            if 75 <= days(e0, e1) <= 120 and e1 not in out:
                out[e1] = (v1 - v0, True)
    return out


def instants(vals):
    return {e: (v, False) for (s, e), v in vals.items() if s is None}


def best(gaap, key):
    """Merge a metric's tags, preferring the one whose data runs latest."""
    conv = instants if key in INSTANT else flow_quarters
    series = [s for s in (conv(facts_for(gaap, t)) for t in TAGS[key]) if s]
    series.sort(key=lambda s: (max(s), len(s)), reverse=True)
    merged = {}
    for s in reversed(series):
        merged.update(s)
    return merged


def company(cik):
    facts = get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    gaap = facts["facts"].get("us-gaap", {})
    m = {k: best(gaap, k) for k in TAGS}
    rows = []
    for e in sorted(set(m["rev"]) & set(m["ni"]), reverse=True):
        val = lambda k: m[k][e][0] if e in m[k] else None
        gp = val("gp")
        if gp is None and val("cost") is not None:
            gp = val("rev") - val("cost")
        capex = val("capex")
        if capex is None and val("flight") is not None and val("other_pp") is not None:
            capex = val("flight") + val("other_pp")
        me = month_end(datetime.strptime(e, "%Y-%m-%d").date())
        rows.append(dict(end=e, col=me.year * 4 + (me.month - 1) // 3,
                         derived=m["rev"][e][1] or m["ni"][e][1],
                         rev=val("rev"), gp=gp, ni=val("ni"), ocf=val("ocf"),
                         capex=capex, ca=val("ca"), cl=val("cl")))
    # Same column rule as the Fundamentals page: a long first quarter that lands
    # in the next filing's quarter moves back one column.
    for newer, r in zip(rows, rows[1:]):
        if r["col"] >= newer["col"]:
            r["col"] = newer["col"] - 1
    lo = FIRST_COL[0] * 4 + FIRST_COL[1] - 1
    hi = LAST_COL[0] * 4 + LAST_COL[1] - 1
    rows = [r for r in reversed(rows) if lo <= r["col"] <= hi]
    for r in rows:
        r["q"] = f"{(r['col'] // 4) % 100:02d}Q{r['col'] % 4 + 1}"
        del r["col"]
    return facts["entityName"], rows


def main():
    root = Path(__file__).resolve().parent.parent
    tickmap = {v["ticker"]: v["cik_str"]
               for v in get_json("https://www.sec.gov/files/company_tickers.json").values()}
    data = []
    for group, tickers in GROUPS:
        for t in tickers:
            sub = get_json(f"https://data.sec.gov/submissions/CIK{tickmap[t]:010d}.json")
            name, rows = company(tickmap[t])
            fye = fye_mmdd(sub.get("fiscalYearEnd") or "1231")
            data.append(dict(ticker=t, name=name, group=group, fye=fye, quarters=rows))
            r = rows[-1]
            miss = [k for k in ("gp", "ocf", "capex", "ca", "cl")
                    if sum(q[k] is None for q in rows) > 0]
            gpm = f"{r['gp'] / r['rev']:.1%}" if r["gp"] is not None else "-"
            cr = f"{r['ca'] / r['cl']:.2f}" if r["ca"] and r["cl"] else "-"
            print(f"{t:6} n={len(rows)} {r['q']} GPM {gpm} NPM {r['ni'] / r['rev']:.1%} CR {cr}"
                  f" OCF {r['ocf']} capex {r['capex']}  missing:{miss}")
            time.sleep(0.25)
    order = [g for g, _ in GROUPS]
    data.sort(key=lambda c: (order.index(c["group"]), c["fye"], c["ticker"]))

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    page = (Path(__file__).with_name("ratios_template.html").read_text(encoding="utf-8")
            .replace("__DATA__", json.dumps(data, separators=(",", ":")))
            .replace("__STAMP__", stamp))
    (root / "ratios.md").write_text(
        '---\nlayout: page\ntitle: "Ratios"\n---\n\n{% raw %}\n' + page + "\n{% endraw %}\n",
        encoding="utf-8")


if __name__ == "__main__":
    main()
