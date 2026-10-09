"""Build fundamentals.md: per-ticker links + the 12 most recent 10-K/10-Q filings.

Run from the repo root:  python _code/fundamentals.py
Data: SEC EDGAR submissions API (filing list) + companyfacts API (fiscal
year/period each company tagged on its own filing, i.e. its own convention).
"""
import json
import time
import urllib.request
from datetime import date, datetime
from pathlib import Path

UA = {"User-Agent": "Jaeyoon Yu yu10j@cmich.edu"}
N_FILINGS = 12

# (group, [tickers]); CAVA and CMCSA are the biggest competitors of SG and CHTR.
GROUPS = [
    ("Tech", ["MU", "NVDA", "GOOGL", "AMZN", "AVGO", "ORCL", "NFLX"]),
    ("Retail", ["WMT", "COST", "KR", "TGT", "TJX"]),
    ("Footwear / apparel", ["NKE", "CROX", "DECK"]),
    ("Restaurants", ["SG", "CAVA"]),
    ("Autos / used cars", ["KMX", "CVNA", "GM", "F"]),
    ("Airlines", ["UAL", "DAL", "AAL", "LUV"]),
    ("Cruise lines", ["RCL", "CCL", "NCLH"]),
    ("Cable / broadband", ["CHTR", "CMCSA"]),
]


def get_json(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)


def month_end(fye):
    """EDGAR's MMDD fiscal year end snapped to the nearest month end (0201 -> 0131)."""
    mm, dd = int(fye[:2]), int(fye[2:])
    if dd <= 15:
        mm = (mm - 2) % 12 + 1
    last = (date(2025 + (mm == 12), mm % 12 + 1, 1) - date.resolution).day
    return f"{mm:02d}{last:02d}"


def filing_fy_fp(cik):
    """accn -> (fy, fp) from the DEI focus the company reported on that filing."""
    facts = get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    out = {}
    for taxo in facts.get("facts", {}).values():
        for concept in taxo.values():
            for unit in concept.get("units", {}).values():
                for f in unit:
                    if f.get("form") in ("10-K", "10-Q") and f.get("fy") and f.get("fp"):
                        out.setdefault(f["accn"], (f["fy"], f["fp"]))
    return out


def company(ticker, cik):
    sub = get_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    recent = sub["filings"]["recent"]
    rows = [dict(zip(recent, vals)) for vals in zip(*recent.values())]
    rows = [r for r in rows if r["form"] in ("10-K", "10-Q") and r["reportDate"]]
    rows.sort(key=lambda r: r["reportDate"], reverse=True)
    rows = rows[:N_FILINGS]
    fye = sub.get("fiscalYearEnd") or "1231"
    # The tagged fy is noisy filing to filing, so it only votes on the company's
    # naming convention (fiscal year named for the year it ends vs. starts);
    # every label is then computed from the period-end date.
    tagged = filing_fy_fp(cik)
    computed = {r["accessionNumber"]: fiscal_end_and_q(r["reportDate"], fye) for r in rows}
    votes = [tagged[a][0] - e.year for a, (e, _) in computed.items() if a in tagged]
    offset = max(set(votes), key=votes.count) if votes else 0
    filings = []
    for r in rows:
        end, q = computed[r["accessionNumber"]]
        fy = end.year + offset
        if r["form"] == "10-K":
            q = 4
        url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/"
               f"{r['accessionNumber'].replace('-', '')}/{r['primaryDocument']}")
        filings.append(dict(form=r["form"], period=r["reportDate"], filed=r["filingDate"],
                            label=f"{fy % 100:02d}Q{q}", col=fy * 4 + q - 1, url=url))
        tag = tagged.get(r["accessionNumber"])
        if tag and (tag[0] != fy or tag[1] not in (f"Q{q}", "FY")):
            print(f"  note {ticker} {r['reportDate']}: tagged {tag}, using {fy}Q{q}")
    return dict(ticker=ticker, cik=cik, name=sub["name"], fye=fye, filings=filings)


def fiscal_end_and_q(period, fye):
    """(end date of the fiscal year containing period, fiscal quarter 1-4)."""
    d = datetime.strptime(period, "%Y-%m-%d").date()
    mm, dd = int(fye[:2]), min(int(fye[2:]), 28)
    # 52/53-week years drift a few days around the nominal FYE, hence the 10-day slack.
    end = min(e for e in (date(y, mm, dd) for y in range(d.year - 1, d.year + 2))
              if (e - d).days >= -10)
    return end, 4 - round((end - d).days / 91.3)


def main():
    root = Path(__file__).resolve().parent.parent
    tickmap = {v["ticker"]: v["cik_str"]
               for v in get_json("https://www.sec.gov/files/company_tickers.json").values()}
    data = []
    for group, tickers in GROUPS:
        for t in tickers:
            c = company(t, tickmap[t])
            c["group"] = group
            data.append(c)
            print(t, c["fye"], [f["label"] for f in c["filings"]])
            time.sleep(0.25)

    # Columns are fiscal quarters: every company's 26Q4 shares one column,
    # whatever calendar date its fiscal 2026 actually ends on.
    hi = max(f["col"] for c in data for f in c["filings"])
    lo = min(f["col"] for c in data for f in c["filings"])
    cols = list(range(hi, lo - 1, -1))

    def colname(k):
        return f"{(k // 4) % 100:02d}Q{k % 4 + 1}"

    th = "".join(f"<th>{colname(k)}</th>" for k in cols)
    body = []
    group = None
    for c in data:
        if c["group"] != group:
            group = c["group"]
            body.append(f'<tr class="grp"><td colspan="{3 + len(cols)}">{group}</td></tr>')
        t = c["ticker"]
        by_col = {f["col"]: f for f in c["filings"]}
        cells = []
        for k in cols:
            f = by_col.get(k)
            if not f:
                cells.append("<td></td>")
                continue
            cls = ' class="k"' if f["form"] == "10-K" else ""
            tip = f'{f["label"]} &middot; period {f["period"]} &middot; filed {f["filed"]}'
            cells.append(f'<td{cls}><a href="{f["url"]}" target="_blank" title="{tip}">{f["form"]}</a></td>')
        body.append(
            f'<tr><td class="tk" title="{c["name"]}">{t}</td><td>{month_end(c["fye"])}</td>'
            f'<td class="lk"><a href="https://stockanalysis.com/stocks/{t.lower()}/" target="_blank">SA</a>'
            f' | <a href="https://finviz.com/quote.ashx?t={t}" target="_blank">FV</a>'
            f' | <a href="https://www.sec.gov/edgar/browse/?CIK={c["cik"]}" target="_blank">SEC</a></td>'
            + "".join(cells) + "</tr>")

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"""---
layout: page
title: "Fundamentals"
---

<style>
.fund-wrap {{ overflow-x: auto; margin: 0 -2em; }}
table.fund {{ border-collapse: collapse; font-size: 12px; white-space: nowrap; margin: 0 auto; }}
table.fund th, table.fund td {{ padding: 2px 5px; border-bottom: 1px solid rgba(128,128,128,.25); text-align: center; }}
table.fund th {{ position: sticky; top: 0; background: var(--background, #fff); font-weight: 600; }}
table.fund td.tk {{ text-align: left; font-weight: 700; padding-left: 14px; }}
table.fund td.lk {{ opacity: .85; }}
table.fund tr.grp td {{ text-align: left; font-weight: 700; padding-top: 8px; opacity: .7; font-size: 11px; text-transform: uppercase; letter-spacing: .05em; }}
table.fund td.k a {{ font-weight: 700; }}
table.fund td.k {{ background: rgba(26,122,94,.12); }}
table.fund th:nth-child(3), table.fund td:nth-child(3) {{ border-right: 1px solid rgba(128,128,128,.4); }}
</style>

<div class="fund-wrap">
<table class="fund">
<thead><tr><th>Ticker</th><th>FYE</th><th>Links</th>{th}</tr></thead>
<tbody>
{chr(10).join(body)}
</tbody>
</table>
</div>

<small>
SA = stockanalysis.com; FV = finviz; SEC = EDGAR filing list.<br>
FYE = fiscal year end (MMDD), shown as the nearest month end.<br>
Columns are fiscal quarters under each company's own naming, so the same column can end on different calendar dates.<br>
E.g., Target's year ending Jan 2026 is its fiscal 2025 ("25Q4"), while NVIDIA's is fiscal 2026 ("26Q4").<br>
10-K cells are shaded.<br>
Hover a cell for fiscal quarter, period end, and filing date.<br>
Updated {stamp} from SEC EDGAR.
</small>
"""
    (root / "fundamentals.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
