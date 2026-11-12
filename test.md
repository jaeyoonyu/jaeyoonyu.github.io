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
| In-Class Case: Walmart | Ch1-7 | <a href="/assets/ACC250/Walmart-Case-Slides.html?v=1a712888" target="_blank">Slides</a> | [PDF](/assets/ACC250/Walmart-Case.pdf?v=1bdf1c5c) | [PDF](/assets/ACC250/Walmart-Case-Key.pdf?v=bf99d5c3) |
| In-Class Case: Costco | Ch1-7 | <a href="/assets/ACC250/Costco-Case-Slides.html?v=11b1a4e8" target="_blank">Slides</a> | [PDF](/assets/ACC250/Costco-Case.pdf?v=587c1f75) | [PDF](/assets/ACC250/Costco-Case-Key.pdf?v=7dc03514) |
| Bad Debts in Real Life: Crocs and Costco (opening) | Ch8 | <a href="/assets/ACC250/Ch8-BadDebt-RealLife.html?v=d775de9d" target="_blank">Slides</a> | [PDF](/assets/ACC250/Ch8-BadDebt-Worksheet.pdf?v=461e795e) | [PDF](/assets/ACC250/Ch8-BadDebt-Worksheet-Key.pdf?v=a2dc56e5) |
| Ch8 Practice: % of Credit Sales (Jan-Feb) | Ch8 | — | [PDF](/assets/ACC250/Ch8-Practice-Worksheet.pdf?v=8614de0f) | [PDF](/assets/ACC250/Ch8-Practice-Worksheet-Key.pdf?v=30663c26) |
| Accounting in the News: Anthropic's S-1 (IPO filing) | Overview | <a href="/assets/ACC250/Anthropic-S1.html?v=c0bf6288" target="_blank">Slides</a> | [PDF](/assets/ACC250/Anthropic-S1-Worksheet.pdf?v=8cd70999) | [PDF](/assets/ACC250/Anthropic-S1-Worksheet-Key.pdf?v=97c43015) |

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
    try { localStorage.setItem('edgar-q', q); } catch (e) {}
    history.replaceState(null, '', '?q=' + encodeURIComponent(q));
    window.open(url(q, type), '_blank', 'noopener');
  }

  document.querySelectorAll('.eg-btns button').forEach(function (b) {
    b.addEventListener('click', function () { open(b.getAttribute('data-type')); });
  });
  document.getElementById('eg-form').addEventListener('submit', function (e) { e.preventDefault(); open('10-K'); });
  document.querySelectorAll('.eg-try a').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); input.value = a.getAttribute('data-q'); msg.textContent = ''; input.focus(); });
  });

  var start = new URLSearchParams(location.search).get('q');
  if (!start) { try { start = localStorage.getItem('edgar-q'); } catch (e) {} }
  if (start) input.value = start;
})();
</script>

### Notes
- **10-K**: annual report with audited financial statements. **10-Q**: quarterly report (unaudited). **8-K**: current report on major events, such as earnings releases, acquisitions, or executive changes. **DEF 14A**: proxy statement for the shareholder meeting, including executive pay and board elections.
- Each form list also includes amendments (for example, 10-K/A).
- Pressing **Enter** opens the 10-K list.
- Foreign companies file different forms (20-F annual, 6-K current), so use **All filings** for them.
