---
layout: page
title: "Test"
---

Materials being tested before they move to a course page.

## 🏢 Real-Company Cases (ACC250)

<style>
.lnotes table { font-size:.85em; }
.lnotes td, .lnotes th { white-space:nowrap; }
</style>

<div class="lnotes" markdown="1">

| Material | Chapters | Slides | Worksheet | Answer key |
|----------|----------|--------|-----------|------------|
| In-Class Case: Walmart | Ch1-7 | <a href="/assets/ACC250/Walmart-Case-Slides.html?v=f46e749f" target="_blank">Slides</a> | [PDF](/assets/ACC250/Walmart-Case.pdf?v=1bdf1c5c) | [PDF](/assets/ACC250/Walmart-Case-Key.pdf?v=bf99d5c3) |
| In-Class Case: Costco | Ch1-7 | <a href="/assets/ACC250/Costco-Case-Slides.html?v=1c3e6c90" target="_blank">Slides</a> | [PDF](/assets/ACC250/Costco-Case.pdf?v=587c1f75) | [PDF](/assets/ACC250/Costco-Case-Key.pdf?v=7dc03514) |
| Bad Debts in Real Life: Crocs and Costco (opening) | Ch8 | <a href="/assets/ACC250/Ch8-BadDebt-RealLife.html?v=4ddeb162" target="_blank">Slides</a> | [PDF](/assets/ACC250/Ch8-BadDebt-Worksheet.pdf?v=461e795e) | [PDF](/assets/ACC250/Ch8-BadDebt-Worksheet-Key.pdf?v=a2dc56e5) |
| Ch8 Practice: % of Credit Sales (Jan-Feb) | Ch8 | <a href="/assets/ACC250/Ch8-Practice-Slides.html?v=5559c747" target="_blank">Slides</a> | [PDF](/assets/ACC250/Ch8-Practice-Worksheet.pdf?v=00d267fa) | [PDF](/assets/ACC250/Ch8-Practice-Worksheet-Key.pdf?v=88b67d27) |
| Accounting in the News: Anthropic's S-1 (IPO filing) | Overview | <a href="/assets/ACC250/Anthropic-S1.html?v=e110deba" target="_blank">Slides</a> | [PDF](/assets/ACC250/Anthropic-S1-Worksheet.pdf?v=8cd70999) | [PDF](/assets/ACC250/Anthropic-S1-Worksheet-Key.pdf?v=97c43015) |
| Accounting in the News: Berkshire Buybacks | Ch11 | <a href="/assets/ACC250/Berkshire-Buyback.html?v=46fc1ef2" target="_blank">Slides</a> | — | — |

</div>

## 🔎 EDGAR Filings

Type a **ticker** (e.g., WMT) or a **CIK** (e.g., 104169), then pick a form. The company's filings open on SEC EDGAR in a new tab.

<div id="edgar">
  <form id="eg-form" autocomplete="off">
    <input id="eg-q" type="text" placeholder="Ticker or CIK" aria-label="Ticker or CIK" spellcheck="false">
  </form>
  <div class="eg-btns">
    <button type="button" data-type="10-K">10-K <span>annual</span></button>
    <button type="button" data-type="10-Q">10-Q <span>quarterly</span></button>
    <button type="button" data-type="8-K">8-K <span>current events</span></button>
    <button type="button" data-type="DEF 14A">DEF 14A <span>proxy</span></button>
    <button type="button" data-type="S-1">S-1 <span>IPO registration</span></button>
    <button type="button" data-type="DRS">DRS <span>draft registration</span></button>
    <button type="button" data-type="" class="all">All filings</button>
  </div>
  <p id="eg-msg" class="eg-msg" role="status"></p>
  <p class="eg-try">Try:
    <a href="#" data-q="WMT">WMT</a> &middot;
    <a href="#" data-q="COST">COST</a> &middot;
    <a href="#" data-q="CROX">CROX</a> &middot;
    <a href="#" data-q="AAPL">AAPL</a> &middot;
    <a href="#" data-q="104169">104169</a> (Walmart&rsquo;s CIK)
  </p>
  <p class="eg-try">IPO S-1s:
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=UBER&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Uber S-1 filings (2019 IPO)">Uber <small>2019</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=ZM&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Zoom S-1 filings (2019 IPO)">Zoom <small>2019</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=PINS&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Pinterest S-1 filings (2019 IPO)">Pinterest <small>2019</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=SNOW&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Snowflake S-1 filings (2020 IPO)">Snowflake <small>2020</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=ABNB&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Airbnb S-1 filings (2020 IPO)">Airbnb <small>2020</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=DASH&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="DoorDash S-1 filings (2020 IPO)">DoorDash <small>2020</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=COIN&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Coinbase S-1 filings (2021 IPO)">Coinbase <small>2021</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=HOOD&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Robinhood S-1 filings (2021 IPO)">Robinhood <small>2021</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=RIVN&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Rivian S-1 filings (2021 IPO)">Rivian <small>2021</small></a> &middot;
    <a href="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&amp;CIK=1713445&amp;type=S-1&amp;dateb=&amp;owner=include&amp;count=40" target="_blank" rel="noopener" title="Reddit S-1 filings (2024 IPO)">Reddit <small>2024</small></a>
  </p>
</div>

<style>
#edgar { margin:1.2em 0 1.6em; }
#eg-q { width:100%; max-width:420px; box-sizing:border-box; font-size:1.3em; padding:10px 14px;
  border:2px solid #1a7a5e; border-radius:8px; text-transform:uppercase; letter-spacing:.04em; }
#eg-q::placeholder { text-transform:none; letter-spacing:0; }
.eg-btns { display:flex; flex-wrap:wrap; gap:10px; margin-top:14px; }
.eg-btns button { font-size:1.05em; font-weight:700; padding:10px 16px; border-radius:8px; cursor:pointer;
  border:0; background:#1a7a5e; color:#fff; line-height:1.15; text-align:left; }
.eg-btns button span { display:block; font-size:.72em; font-weight:400; opacity:.85; }
.eg-btns button.all { background:#16263a; }
.eg-btns button:hover { filter:brightness(1.12); }
.eg-msg { min-height:1.4em; margin:.6em 0 0; color:#b3200f; font-size:.95em; }
.eg-try { font-size:.9em; color:#5c6863; }
</style>

<script>
(function () {
  var input = document.getElementById('eg-q');
  var msg = document.getElementById('eg-msg');

  // Ticker: letters/digits with an optional "." or "-" (BRK.B, BF-B). CIK: up to 10 digits.
  function clean() {
    var q = input.value.trim().toUpperCase();
    if (/^\d{1,10}$/.test(q)) return q.replace(/^0+(?=\d)/, '');
    if (/^[A-Z][A-Z0-9]{0,5}([.\-][A-Z0-9]{1,2})?$/.test(q)) return q.replace('.', '-');   // EDGAR writes BRK.B as BRK-B
    return null;
  }

  function url(q, type) {
    if (!type) return 'https://www.sec.gov/edgar/browse/?CIK=' + encodeURIComponent(q);
    return 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + encodeURIComponent(q) +
           '&type=' + encodeURIComponent(type) + '&dateb=&owner=include&count=40';
  }

  function open(type) {
    var q = clean();
    if (!q) {
      msg.textContent = input.value.trim() ? 'Enter a ticker (e.g., WMT) or a CIK number (e.g., 104169).'
                                           : 'Type a ticker or CIK first.';
      input.focus();
      return;
    }
    msg.textContent = '';
    window.open(url(q, type), '_blank', 'noopener');
  }

  document.querySelectorAll('.eg-btns button').forEach(function (b) {
    b.addEventListener('click', function () { open(b.getAttribute('data-type')); });
  });
  document.getElementById('eg-form').addEventListener('submit', function (e) { e.preventDefault(); open('10-K'); });
  document.querySelectorAll('.eg-try a[data-q]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); input.value = a.getAttribute('data-q'); msg.textContent = ''; input.focus(); });
  });
})();
</script>

### Notes
- **10-K**: annual report with audited financial statements. **10-Q**: quarterly report (unaudited). **8-K**: current report on major events, such as earnings releases, acquisitions, or executive changes. **DEF 14A**: proxy statement for the shareholder meeting, including executive pay and board elections.
- **S-1**: IPO registration statement. **DRS**: draft registration filed confidentially before the IPO; EDGAR shows it only after release.
- Each form list also includes amendments (for example, 10-K/A).
- Pressing **Enter** opens the 10-K list.
- Foreign companies file different forms (20-F annual, 6-K current), so use **All filings** for them.

## 📜 Buffett's Letters

* [Buffett's Letters: Accounting Themes](/buffett-letters/): 17 accounting themes from Berkshire's shareholder letters, with links, difficulty, ACC250/ACC531 fit, and a question sheet with key for each.
