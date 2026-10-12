---
layout: page
title: "Midland Community Center"
permalink: /midland/
sitemap: false
---

{% raw %}
<style>
.md { --line: rgba(128,128,128,.22); --muted: rgba(120,128,124,1); --accent: #1a7a5e; --today: rgba(26,122,94,.07);
  --th-bg: #fff; font-size: 14px; line-height: 1.4;
  width: min(1100px, calc(100vw - 32px)); position: relative; left: 50%; transform: translateX(-50%); }
@media (prefers-color-scheme: dark) {
  .md { --muted: #96a29b; --accent: #53c79e; --today: rgba(83,199,158,.09); --th-bg: #1d1f23; }
}
.md * { box-sizing: border-box; }
.md-sub { color: var(--muted); font-size: 12.5px; margin: -6px 0 14px; line-height: 1.7; }

/* activity buttons */
.md-acts { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
.md-acts button { border: 1px solid var(--line); background: transparent; color: inherit; border-radius: 12px;
  padding: 8px 16px; font-size: 15px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 7px; }
.md-acts button:hover { border-color: var(--muted); }
.md-acts button.on { background: var(--c); border-color: var(--c); color: #fff; }
.md-acts .live { width: 8px; height: 8px; border-radius: 50%; background: #2ecc71; box-shadow: 0 0 0 2px rgba(46,204,113,.3); }
.md-acts button.on .live { background: #fff; box-shadow: none; }

.md-head { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; margin-bottom: 4px; }
.md-head h3 { margin: 0; font-size: 20px; }
.md-head span { color: var(--muted); font-size: 13px; }
.md-status { font-size: 14px; margin-bottom: 10px; }
.md-status b { color: var(--accent); }
.md-legend { display: flex; gap: 14px; flex-wrap: wrap; font-size: 12px; color: var(--muted); margin-bottom: 8px; }
.md-sw { display: inline-block; width: 12px; height: 8px; border-radius: 2px; margin-right: 5px; vertical-align: 0; }

/* week view: one block per day, one lane per sub-type */
.md-week { border-top: 1px solid var(--line); }
.md-day { display: grid; grid-template-columns: 74px 1fr; border-bottom: 1px solid var(--line); }
.md-day.today { background: var(--today); }
.md-dn { padding: 7px 0 7px 6px; font-weight: 700; font-size: 14px; line-height: 1.2; }
.md-dn small { display: block; font-weight: 400; font-size: 11px; color: var(--muted); }
.md-day.today .md-dn { color: var(--accent); }
.md-lanes { padding: 4px 0; }
.md-lane { display: grid; grid-template-columns: var(--ln, 0px) minmax(0, 1fr) 290px; gap: 10px; align-items: center; min-height: 24px; }
.md-ln { font-size: 11px; color: var(--muted); white-space: nowrap; overflow: hidden; }
.md-track { position: relative; height: 18px; background: rgba(128,128,128,.07); border-radius: 4px; }
.md-closed { position: absolute; top: 0; bottom: 0; background: repeating-linear-gradient(135deg, rgba(128,128,128,.13) 0 3px, transparent 3px 7px); }
.md-bar { position: absolute; top: 2px; bottom: 2px; border-radius: 4px; }
.md-bar.past { opacity: .35; }
.md-bar.off { background: transparent !important; border: 1.5px dashed var(--muted); }
.md-nowline { position: absolute; top: -3px; bottom: -3px; width: 2px; background: #e74c3c; z-index: 2; }
.md-times { font-size: 12.5px; font-variant-numeric: tabular-nums; line-height: 1.35; }
.md-times .none { color: var(--muted); }
.md-times small { color: var(--muted); }
.md-times s { color: var(--muted); }
.md-axis { display: grid; grid-template-columns: 74px var(--ln, 0px) minmax(0, 1fr) 290px; gap: 0 10px; font-size: 10.5px; color: var(--muted); }
.md-axis > div:nth-child(3) { position: relative; height: 16px; }
.md-axis span { position: absolute; transform: translateX(-50%); white-space: nowrap; }
@media (max-width: 700px) {
  .md-day { grid-template-columns: 52px 1fr; }
  .md-lane { grid-template-columns: var(--ln, 0px) minmax(0, 1fr); }
  .md-times { grid-column: 1 / -1; padding: 0 0 4px; }
  .md-axis { grid-template-columns: 52px var(--ln, 0px) minmax(0, 1fr); }
  .md-axis > div:nth-child(4) { display: none; }
}

/* all activities, for reference */
.md-all { margin-top: 26px; }
.md-all summary { cursor: pointer; font-weight: 600; color: var(--muted); }
.md-tw { overflow-x: auto; margin-top: 8px; border: 1px solid var(--line); border-radius: 10px; }
table.md-t { border-collapse: separate; border-spacing: 0; font-size: 12.5px; width: 100%; min-width: 760px; }
.md-t th, .md-t td { padding: 5px 8px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.md-t th:first-child, .md-t td:first-child { position: sticky; left: 0; background: var(--th-bg); min-width: 130px; font-weight: 600; z-index: 1; }
.md-t thead th { background: var(--th-bg); }
.md-t td { white-space: nowrap; font-variant-numeric: tabular-nums; }
.md-t .today { background: var(--today); }
.md-t td small { color: var(--muted); }
.md-foot { color: var(--muted); font-size: 11.5px; margin-top: 12px; line-height: 1.7; }
</style>

<div class="md" id="md">
  <div class="md-sub">
    Greater Midland Community Center drop-in hours, effective Sep 8 – Dec 19, 2026.<br>
    Day pass $11 adult, $8 child.
  </div>
  <div class="md-acts" id="md-acts"></div>
  <div class="md-head" id="md-head"></div>
  <div class="md-status" id="md-status"></div>
  <div class="md-legend" id="md-legend"></div>
  <div id="md-week"></div>
  <details class="md-all">
    <summary>All activities, this week</summary>
    <div class="md-tw" id="md-tw"></div>
  </details>
  <div class="md-foot">
    Source: <a href="https://static1.squarespace.com/static/54352636e4b03176bba53234/t/6aa13f751adad704fe9ce89f/1788952437416/Drop-In+9.8+-+12.19+%282%29.pdf" target="_blank" rel="noopener">Drop-In Hours PDF</a> ·
    <a href="https://greatermidland.org/community-center" target="_blank" rel="noopener">greatermidland.org/community-center</a>.<br>
    * Varies with the program schedule — check before going.<br>
    Hatched areas are when the building is closed.<br>
    Ctrl+← / Ctrl+→ switch activities.
  </div>
</div>

<script>
(() => {
  // Days: 0 = Mon … 6 = Sun. Times are hours (13.25 = 1:15 PM).
  // Each activity has one or more lanes (Swim: lap / rec / open); each lane lists [days, [start, end], note].
  const MF = [0, 1, 2, 3, 4];
  const BUILDING = [[5, 21], [5, 21], [5, 21], [5, 21], [5, 21], [7, 20], [10, 17.5]];
  const ACTS = [
    { id: "swim", n: "Swim", c: "#2a78d6", lanes: [
      { n: "Lap swim", c: "#2a78d6", s: [
        [[0, 2], [5, 8]], [[0, 2], [9, 15.5]], [[0, 1, 2], [19.5, 20.5]], [[1, 3], [5, 15.5]],
        [[4], [5, 8]], [[4], [9, 15.5]], [[5], [8, 13]], [[6], [11, 14]]] },
      { n: "Rec swim", sub: "no slide or spray", c: "#17a2b8", s: [
        [[0, 2, 4], [5, 9]], [[0, 2, 4], [11, 15.5]], [[1, 3], [5, 8]], [[1, 3], [12, 15.5]], [[1], [19.5, 20.5]], [[6], [11, 14]]] },
      { n: "Open swim", sub: "slide every 30 min", c: "#8e5bd6", s: [
        [[3], [18, 20.5], "$6 community swim night"], [[4], [18, 20.5]], [[5], [13, 19]], [[6], [14, 17]]] }] },
    { id: "pickleball", n: "Pickleball", c: "#d9682b", lanes: [
      { n: "Pickleball", c: "#d9682b", s: [
        [MF, [6, 11], "3 courts"], [[0, 2, 4], [13.25, 15.25], "3–6 courts"], [[5], [7.5, 14], "3 courts"], [[6], [10, 14], "3 courts"]],
        off: { "2026-10-17": "No pickleball Oct 17", "2026-09-20": "No pickleball Sep 20" } }] },
    { id: "basketball", n: "Basketball", c: "#b5541c", lanes: [
      { n: "Adult", c: "#b5541c", s: [[MF, [5.5, 8]], [MF, [11.25, 13]]] },
      { n: "Youth", c: "#e8a33d", s: [[MF, [15, 17]], [[5], [12, 16], "*"]] },
      { n: "Adult & youth", c: "#d9682b", s: [[MF, [17, 21], "*"], [[5], [16, 20]], [[6], [13, 17.5], "*"]] }] },
    { id: "childwatch", n: "Child Watch", sub: "ages 3 months – 9 years", c: "#1a7a5e", lanes: [
      { n: "Child Watch", c: "#1a7a5e", s: [[MF, [8, 12]], [[0, 1, 2], [16.5, 19.5]], [[3], [17.5, 19.5]], [[5], [8, 12]]] }] },
    { id: "zone", n: "The Zone", sub: "ages 6–12 · Activity Room 1", c: "#2e9e74", lanes: [
      { n: "The Zone", c: "#2e9e74", s: [[[0, 1, 2], [16.5, 19.5]], [[5], [8, 12]]] }] },
    { id: "junglegym", n: "Jungle Gym", sub: "ages 6 & under, with a parent or guardian", c: "#5a9e3a", lanes: [
      { n: "Jungle Gym", c: "#5a9e3a", s: [[[0, 2, 4], [10, 12]], [[5], [16, 18]]] }] },
  ];
  const T0 = 5, T1 = 21;  // axis 5 AM – 9 PM
  const DAYN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  function t(h) {
    const hh = Math.floor(h), mm = Math.round((h - hh) * 60), ap = hh >= 12 ? "PM" : "AM", h12 = hh % 12 || 12;
    return mm ? `${h12}:${String(mm).padStart(2, "0")} ${ap}` : `${h12} ${ap}`;
  }
  const range = r => {  // "5 – 8 AM", "9 AM – 3:30 PM"
    const a = t(r[0]), b = t(r[1]);
    return a.slice(-2) === b.slice(-2) ? `${a.slice(0, -3)} – ${b}` : `${a} – ${b}`;
  };
  const pct = h => ((h - T0) / (T1 - T0)) * 100;

  // This week's dates (Mon–Sun), so date-specific cancellations land on the right day.
  const now = new Date();
  const dow = (now.getDay() + 6) % 7;
  const dates = DAYN.map((_, i) => new Date(now.getFullYear(), now.getMonth(), now.getDate() - dow + i));
  const nowH = now.getHours() + now.getMinutes() / 60;

  const slots = (lane, d) => lane.s.filter(([days]) => days.includes(d))
    .map(([, r, note]) => ({ r, note, off: lane.off && lane.off[iso(dates[d])] })).sort((x, y) => x.r[0] - y.r[0]);

  // "Open now" (lane + end time) or the next start within the coming week.
  function status(a) {
    const open = [];
    a.lanes.forEach(l => slots(l, dow).forEach(s => { if (!s.off && nowH >= s.r[0] && nowH < s.r[1]) open.push([l, s]); }));
    if (open.length) return { open: true, html: "<b>Open now</b> · " + open.map(([l, s]) =>
      `${a.lanes.length > 1 ? esc(l.n) + " " : ""}until ${t(s.r[1])}`).join(" · ") };
    for (let k = 0; k < 8; k++) {
      const d = (dow + k) % 7, cand = [];
      a.lanes.forEach(l => slots(l, d).forEach(s => { if (!s.off && (k > 0 || s.r[0] > nowH)) cand.push([l, s]); }));
      cand.sort((x, y) => x[1].r[0] - y[1].r[0]);
      if (cand.length) {
        const [l, s] = cand[0], when = k === 0 ? "today" : k === 1 ? "tomorrow" : DAYN[d];
        return { open: false, html: `Closed now · next: <b>${when} ${t(s.r[0])}</b>${a.lanes.length > 1 ? " (" + esc(l.n) + ")" : ""}` };
      }
    }
    return { open: false, html: "" };
  }

  let cur = ACTS.findIndex(a => a.id === location.hash.slice(1));
  if (cur < 0) cur = 0;

  function renderButtons() {
    $("md-acts").innerHTML = ACTS.map((a, i) =>
      `<button data-i="${i}" class="${i === cur ? "on" : ""}" style="--c:${a.c}">${status(a).open ? `<span class="live" title="Open now"></span>` : ""}${esc(a.n)}</button>`).join("");
  }

  function renderActivity() {
    const a = ACTS[cur], multi = a.lanes.length > 1;
    $("md").style.setProperty("--ln", multi ? "92px" : "0px");
    $("md-head").innerHTML = `<h3>${esc(a.n)}</h3>${a.sub ? `<span>${esc(a.sub)}</span>` : ""}`;
    $("md-status").innerHTML = status(a).html;
    $("md-legend").innerHTML = multi ? a.lanes.map(l =>
      `<span><span class="md-sw" style="background:${l.c}"></span>${esc(l.n)}${l.sub ? ` — ${esc(l.sub)}` : ""}</span>`).join("") : "";
    let html = "";
    DAYN.forEach((dn, d) => {
      const b = BUILDING[d], isToday = d === dow;
      const lanes = a.lanes.map(l => {
        const ss = slots(l, d);
        const bars = ss.map(s => {
          const cls = s.off ? "off" : isToday && nowH >= s.r[1] ? "past" : "";
          return `<div class="md-bar ${cls}" style="left:${pct(s.r[0])}%;width:${pct(s.r[1]) - pct(s.r[0])}%;background:${l.c}"
            title="${esc(`${l.n}: ${range(s.r)}${s.note ? " · " + s.note : ""}${s.off ? " — " + s.off : ""}`)}"></div>`;
        }).join("");
        const nowline = isToday && nowH > T0 && nowH < T1 ? `<div class="md-nowline" style="left:${pct(nowH)}%"></div>` : "";
        const closed = `<div class="md-closed" style="left:0;width:${pct(b[0])}%"></div><div class="md-closed" style="left:${pct(b[1])}%;right:0"></div>`;
        const times = ss.length ? ss.map(s => {
          const txt = `${range(s.r)}${s.note ? ` <small>${esc(s.note)}</small>` : ""}`;
          return s.off ? `<s>${range(s.r)}</s> <small>${esc(s.off)}</small>` : txt;
        }).join(" · ") : `<span class="none">—</span>`;
        return `<div class="md-lane"><div class="md-ln">${multi ? esc(l.n) : ""}</div>
          <div class="md-track">${closed}${bars}${nowline}</div><div class="md-times">${times}</div></div>`;
      }).join("");
      html += `<div class="md-day ${isToday ? "today" : ""}"><div class="md-dn">${dn}<small>${isToday ? "Today" : `${dates[d].getMonth() + 1}/${dates[d].getDate()}`}</small></div>
        <div class="md-lanes">${lanes}</div></div>`;
    });
    const ticks = [];
    for (let h = T0; h <= T1; h += 2) ticks.push(`<span style="left:${pct(h)}%">${t(h).replace(":00", "").replace(" ", "").toLowerCase()}</span>`);
    html += `<div class="md-axis"><div></div><div></div><div>${ticks.join("")}</div><div></div></div>`;
    $("md-week").innerHTML = `<div class="md-week">${html}</div>`;
  }

  function renderTable() {
    const head = `<tr><th>Activity</th>${DAYN.map((n, i) => `<th class="${i === dow ? "today" : ""}">${n} <small>${dates[i].getMonth() + 1}/${dates[i].getDate()}</small></th>`).join("")}</tr>`;
    const body = ACTS.flatMap(a => a.lanes.map(l => {
      const name = a.lanes.length > 1 ? `${a.n} · ${l.n}` : a.n;
      const cells = DAYN.map((_, d) => {
        const ss = slots(l, d);
        const txt = ss.map(s => s.off ? `<s>${range(s.r)}</s> <small>${esc(s.off)}</small>` : `${range(s.r)}${s.note ? ` <small>${esc(s.note)}</small>` : ""}`).join("<br>");
        return `<td class="${d === dow ? "today" : ""}">${txt || "–"}</td>`;
      }).join("");
      return `<tr><td><span class="md-sw" style="background:${l.c}"></span>${esc(name)}</td>${cells}</tr>`;
    })).join("");
    $("md-tw").innerHTML = `<table class="md-t"><thead>${head}</thead><tbody>${body}</tbody></table>`;
  }

  const go = i => { cur = (i + ACTS.length) % ACTS.length; history.replaceState(null, "", "#" + ACTS[cur].id); renderButtons(); renderActivity(); };
  $("md-acts").onclick = e => { const b = e.target.closest("button"); if (b) go(+b.dataset.i); };
  document.addEventListener("keydown", e => {
    if (/INPUT|TEXTAREA|SELECT/.test(e.target.tagName) || (e.key !== "ArrowLeft" && e.key !== "ArrowRight")) return;
    const step = e.key === "ArrowLeft" ? -1 : 1;
    if (e.ctrlKey || e.metaKey) { e.preventDefault(); go(cur + step); return; }
    const tw = $("md-tw");
    if (tw.offsetParent && tw.scrollWidth > tw.clientWidth) { e.preventDefault(); tw.scrollBy({ left: step * 160, behavior: "smooth" }); }
  });
  renderButtons(); renderActivity(); renderTable();
})();
</script>
{% endraw %}
