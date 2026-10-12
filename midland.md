---
layout: page
title: "Midland Community Center"
permalink: /midland/
sitemap: false
---

{% raw %}
<style>
.md { --aq: #2a78d6; --ct: #d9682b; --kd: #1a7a5e; --line: rgba(128,128,128,.22); --muted: rgba(120,128,124,1);
  --today: rgba(26,122,94,.08); --th-bg: #fff; font-size: 14px; line-height: 1.4;
  width: min(1100px, calc(100vw - 32px)); position: relative; left: 50%; transform: translateX(-50%); }
@media (prefers-color-scheme: dark) {
  .md { --aq: #4a95f0; --ct: #f08a52; --kd: #53c79e; --muted: #96a29b; --today: rgba(83,199,158,.1); --th-bg: #1d1f23; }
}
.md * { box-sizing: border-box; }
.md-sub { color: var(--muted); font-size: 12.5px; margin: -6px 0 14px; line-height: 1.7; }
.md-days { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
.md-days button { border: 1px solid var(--line); background: transparent; color: inherit; border-radius: 999px;
  padding: 4px 13px; font-size: 13px; cursor: pointer; line-height: 1.2; }
.md-days button small { display: block; font-size: 10px; color: var(--muted); }
.md-days button.on { background: var(--kd); border-color: var(--kd); color: #fff; }
.md-days button.on small { color: rgba(255,255,255,.85); }
.md-h { font-size: 17px; font-weight: 700; margin: 6px 0 2px; }
.md-bh { font-size: 12.5px; color: var(--muted); margin-bottom: 10px; }

/* timeline */
.md-tl { position: relative; }
.md-row { display: grid; grid-template-columns: 150px 1fr; align-items: center; min-height: 30px; border-bottom: 1px solid var(--line); }
.md-row.grp { min-height: 0; border: 0; padding: 10px 0 2px; font-size: 11px; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase; color: var(--muted); }
.md-lab { font-size: 13px; font-weight: 600; padding-right: 8px; line-height: 1.2; }
.md-lab small { display: block; font-weight: 400; font-size: 10.5px; color: var(--muted); }
.md-now-b { display: inline-block; font-size: 9.5px; font-weight: 700; color: #fff; background: var(--kd); border-radius: 999px;
  padding: 0 6px; margin-left: 4px; vertical-align: 1px; letter-spacing: .04em; }
.md-track { position: relative; height: 24px; }
.md-bar { position: absolute; top: 3px; bottom: 3px; border-radius: 5px; color: #fff; font-size: 10.5px; font-weight: 600;
  padding: 0 5px; display: flex; align-items: center; overflow: hidden; white-space: nowrap; }
.md-bar.aq { background: var(--aq); } .md-bar.ct { background: var(--ct); } .md-bar.kd { background: var(--kd); }
.md-bar.off { background: repeating-linear-gradient(45deg, var(--line), var(--line) 4px, transparent 4px, transparent 8px);
  color: var(--muted); border: 1px dashed var(--muted); }
.md-bar.done { opacity: .4; }
.md-closed { position: absolute; top: 0; bottom: 0; background: rgba(128,128,128,.1); }
.md-axis { display: grid; grid-template-columns: 150px 1fr; font-size: 10.5px; color: var(--muted); }
.md-axis div:last-child { position: relative; height: 16px; }
.md-axis span { position: absolute; transform: translateX(-50%); }
.md-nowline { position: absolute; top: 0; bottom: 0; width: 2px; background: #c0392b; z-index: 2; pointer-events: none; }
.md-nowline::before { content: "now"; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); font-size: 10px;
  color: #c0392b; font-weight: 700; }
@media (max-width: 640px) {
  .md-row, .md-axis { grid-template-columns: 96px 1fr; }
  .md-lab { font-size: 12px; }
  .md-bar { font-size: 0; }  /* too narrow for text; the weekly table below has the exact times */
}

/* weekly table */
.md-tw { overflow-x: auto; margin-top: 22px; border: 1px solid var(--line); border-radius: 10px; }
table.md-t { border-collapse: separate; border-spacing: 0; font-size: 12.5px; width: 100%; min-width: 760px; }
.md-t th, .md-t td { padding: 5px 8px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.md-t thead th { font-size: 12px; background: var(--th-bg); }
.md-t th:first-child, .md-t td:first-child { position: sticky; left: 0; background: var(--th-bg); min-width: 130px; font-weight: 600; z-index: 1; }
.md-t td { white-space: nowrap; font-variant-numeric: tabular-nums; }
.md-t td.na { color: var(--muted); }
.md-t .today { background: var(--today); }
.md-t thead th.today { color: var(--kd); }
.md-t tr.grp td { font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); padding-top: 10px; }
.md-t td small { color: var(--muted); }
.md-dot { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 6px; vertical-align: 0; }
.md-foot { color: var(--muted); font-size: 11.5px; margin-top: 12px; line-height: 1.7; }
</style>

<div class="md" id="md">
  <div class="md-sub">
    Greater Midland Community Center drop-in hours, effective Sep 8 – Dec 19, 2026.<br>
    Day pass $11 adult, $8 child.
  </div>
  <div class="md-days" id="md-days"></div>
  <div class="md-h" id="md-h"></div>
  <div class="md-bh" id="md-bh"></div>
  <div class="md-tl" id="md-tl"></div>
  <div class="md-tw" id="md-tw"></div>
  <div class="md-foot">
    Source: <a href="https://static1.squarespace.com/static/54352636e4b03176bba53234/t/6aa13f751adad704fe9ce89f/1788952437416/Drop-In+9.8+-+12.19+%282%29.pdf" target="_blank" rel="noopener">Drop-In Hours PDF</a> ·
    <a href="https://greatermidland.org/community-center" target="_blank" rel="noopener">greatermidland.org/community-center</a>.<br>
    * Varies with the program schedule — check before going.<br>
    Rec swim: no slide or spray features. Open swim: the slide runs in 30-minute intervals.<br>
    Ctrl+← / Ctrl+→ switch days; ← / → scroll the weekly table.
  </div>
</div>

<script>
(() => {
  // Days: 0 = Mon … 6 = Sun. Times are hours (13.25 = 1:15 PM).
  const MF = [0, 1, 2, 3, 4];
  const BUILDING = { 0: [5, 21], 1: [5, 21], 2: [5, 21], 3: [5, 21], 4: [5, 21], 5: [7, 20], 6: [10, 17.5] };
  const ACTS = [
    { g: "Aquatics", c: "aq", n: "Lap swim", s: [
      [[0, 2], [5, 8]], [[0, 2], [9, 15.5]], [[0, 1, 2], [19.5, 20.5]], [[1, 3], [5, 15.5]],
      [[4], [5, 8]], [[4], [9, 15.5]], [[5], [8, 13]], [[6], [11, 14]]] },
    { g: "Aquatics", c: "aq", n: "Rec swim", sub: "no slide or spray", s: [
      [[0, 2, 4], [5, 9]], [[0, 2, 4], [11, 15.5]], [[1, 3], [5, 8]], [[1, 3], [12, 15.5]], [[1], [19.5, 20.5]], [[6], [11, 14]]] },
    { g: "Aquatics", c: "aq", n: "Open swim", sub: "slide every 30 min", s: [
      [[3], [18, 20.5], "$6 community swim night"], [[4], [18, 20.5]], [[5], [13, 19]], [[6], [14, 17]]] },
    { g: "Courts", c: "ct", n: "Pickleball", s: [
      [MF, [6, 11], "3 courts"], [[0, 2, 4], [13.25, 15.25], "3–6 courts"],
      [[5], [7.5, 14], "3 courts"], [[6], [10, 14], "3 courts"]],
      off: { "2026-10-17": "No pickleball Oct 17", "2026-09-20": "No pickleball Sep 20" } },
    { g: "Courts", c: "ct", n: "Basketball", sub: "adult", s: [[MF, [5.5, 8]], [MF, [11.25, 13]]] },
    { g: "Courts", c: "ct", n: "Basketball", sub: "youth", s: [[MF, [15, 17]], [[5], [12, 16], "*"]] },
    { g: "Courts", c: "ct", n: "Basketball", sub: "adult & youth", s: [[MF, [17, 21], "*"], [[5], [16, 20]], [[6], [13, 17.5], "*"]] },
    { g: "Kids", c: "kd", n: "Child Watch", sub: "3 months – 9 years", s: [
      [MF, [8, 12]], [[0, 1, 2], [16.5, 19.5]], [[3], [17.5, 19.5]], [[5], [8, 12]]] },
    { g: "Kids", c: "kd", n: "The Zone", sub: "ages 6–12 · Activity Room 1", s: [[[0, 1, 2], [16.5, 19.5]], [[5], [8, 12]]] },
    { g: "Kids", c: "kd", n: "Jungle Gym", sub: "6 & under, with a parent", s: [[[0, 2, 4], [10, 12]], [[5], [16, 18]]] },
  ];
  const T0 = 5, T1 = 21;  // timeline 5 AM – 9 PM
  const DAYN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  function t(h) {
    const hh = Math.floor(h), mm = Math.round((h - hh) * 60), ap = hh >= 12 ? "PM" : "AM", h12 = hh % 12 || 12;
    return mm ? `${h12}:${String(mm).padStart(2, "0")} ${ap}` : `${h12} ${ap}`;
  }
  const short = h => t(h).replace(":00", "").replace(" AM", "a").replace(" PM", "p");
  const pct = h => ((h - T0) / (T1 - T0)) * 100;

  // This week's dates (Mon–Sun), so date-specific cancellations show on the right day.
  const now = new Date();
  const dow = (now.getDay() + 6) % 7;
  const monday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - dow);
  const dates = DAYN.map((_, i) => new Date(monday.getFullYear(), monday.getMonth(), monday.getDate() + i));
  const nowH = now.getHours() + now.getMinutes() / 60;
  let sel = dow;

  const slots = (a, d) => a.s.filter(([days]) => days.includes(d)).map(([, r, note]) => ({ r, note })).sort((x, y) => x.r[0] - y.r[0]);

  function renderDays() {
    $("md-days").innerHTML = DAYN.map((n, i) =>
      `<button data-d="${i}" class="${i === sel ? "on" : ""}"><small>${i === dow ? "Today" : dates[i].toLocaleDateString("en-US", { month: "short", day: "numeric" })}</small>${n}</button>`).join("");
  }

  function renderTimeline() {
    const date = dates[sel], dIso = iso(date), isToday = sel === dow;
    const b = BUILDING[sel];
    $("md-h").textContent = date.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
    $("md-bh").textContent = `Building open ${t(b[0])} – ${t(b[1])}`;
    let html = "", g = "";
    const closed = `<div class="md-closed" style="left:0;width:${pct(b[0])}%"></div><div class="md-closed" style="left:${pct(b[1])}%;right:0"></div>`;
    for (const a of ACTS) {
      if (a.g !== g) { g = a.g; html += `<div class="md-row grp"><div>${g}</div><div></div></div>`; }
      const off = a.off && a.off[dIso];
      const ss = slots(a, sel);
      const openNow = isToday && !off && ss.some(s => nowH >= s.r[0] && nowH < s.r[1]);
      const bars = ss.map(s => {
        const label = `${short(s.r[0])}–${short(s.r[1])}${s.note && s.note !== "*" ? " · " + s.note : ""}${s.note === "*" ? " *" : ""}`;
        const cls = off ? "off" : isToday && nowH >= s.r[1] ? `${a.c} done` : a.c;
        const tip = `${a.n}${a.sub ? " (" + a.sub + ")" : ""}: ${t(s.r[0])} – ${t(s.r[1])}${s.note ? " · " + s.note : ""}${off ? " — " + off : ""}`;
        return `<div class="md-bar ${cls}" style="left:${pct(s.r[0])}%;width:${pct(s.r[1]) - pct(s.r[0])}%" title="${esc(tip)}">${esc(off ? off : label)}</div>`;
      }).join("");
      html += `<div class="md-row"><div class="md-lab">${esc(a.n)}${openNow ? `<span class="md-now-b">OPEN</span>` : ""}${a.sub ? `<small>${esc(a.sub)}</small>` : ""}</div>
        <div class="md-track">${closed}${bars || ""}</div></div>`;
    }
    const ticks = [];
    for (let h = T0; h <= T1; h += 2) ticks.push(`<span style="left:${pct(h)}%">${short(h)}</span>`);
    html += `<div class="md-axis"><div></div><div>${ticks.join("")}</div></div>`;
    $("md-tl").innerHTML = html;
    if (isToday && nowH > T0 && nowH < T1) {
      // The now line sits over the tracks, offset by the label column.
      const lab = $("md-tl").querySelector(".md-track");
      const x = lab.offsetLeft + lab.offsetWidth * pct(nowH) / 100;
      $("md-tl").insertAdjacentHTML("beforeend", `<div class="md-nowline" style="left:${x}px"></div>`);
    }
  }

  function renderTable() {
    let g = "";
    const head = `<tr><th>Activity</th>${DAYN.map((n, i) => `<th class="${i === dow ? "today" : ""}">${n} <small>${dates[i].getMonth() + 1}/${dates[i].getDate()}</small></th>`).join("")}</tr>`;
    const body = ACTS.map(a => {
      let pre = "";
      if (a.g !== g) { g = a.g; pre = `<tr class="grp"><td colspan="8">${g}</td></tr>`; }
      const cells = DAYN.map((_, d) => {
        const off = a.off && a.off[iso(dates[d])];
        const ss = slots(a, d);
        const txt = ss.map(s => `${t(s.r[0])} – ${t(s.r[1])}${s.note ? ` <small>${esc(s.note)}</small>` : ""}`).join("<br>");
        const cls = [d === dow ? "today" : "", ss.length ? "" : "na"].join(" ");
        return `<td class="${cls}">${ss.length ? (off ? `<s>${txt}</s><br><small>${esc(off)}</small>` : txt) : "–"}</td>`;
      }).join("");
      return pre + `<tr><td><span class="md-dot" style="background:var(--${a.c})"></span>${esc(a.n)}${a.sub ? `<br><small>${esc(a.sub)}</small>` : ""}</td>${cells}</tr>`;
    }).join("");
    $("md-tw").innerHTML = `<table class="md-t"><thead>${head}</thead><tbody>${body}</tbody></table>`;
  }

  const go = d => { sel = (d + 7) % 7; renderDays(); renderTimeline(); };
  $("md-days").onclick = e => { const b = e.target.closest("button"); if (b) go(+b.dataset.d); };
  document.addEventListener("keydown", e => {
    if (/INPUT|TEXTAREA|SELECT/.test(e.target.tagName) || (e.key !== "ArrowLeft" && e.key !== "ArrowRight")) return;
    const step = e.key === "ArrowLeft" ? -1 : 1;
    if (e.ctrlKey || e.metaKey) { e.preventDefault(); go(sel + step); return; }
    const tw = $("md-tw");
    if (tw.scrollWidth > tw.clientWidth) { e.preventDefault(); tw.scrollBy({ left: step * 160, behavior: "smooth" }); }
  });
  window.addEventListener("resize", renderTimeline);
  renderDays(); renderTimeline(); renderTable();
})();
</script>
{% endraw %}
