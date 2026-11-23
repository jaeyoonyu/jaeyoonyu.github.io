---
layout: page
title: Submit
sitemap: false
---

<style>
.sub-form h2 { margin-bottom:.2em; }
.sub-form h3 { margin:1.4em 0 .4em; font-size:1.05em; }
.sub-meta { color:#555; margin-top:0; }
.sub-note { margin:.3em 0 0; padding:.45em .7em; border-left:3px solid #3333b3; background:#f3f3fb; }
.sub-who { display:grid; grid-template-columns:max-content minmax(0, 22em); gap:.5em 1em; align-items:center; margin:1em 0; }
.sub-form input, .sub-form textarea, .sub-form select { font:inherit; padding:.35em .5em; border:1px solid #bbb; border-radius:4px; box-sizing:border-box; }
.sub-form textarea { width:100%; }
.sub-q > li { margin-bottom:1em; }
.sub-q > li.lab { list-style:none; margin-left:-1.4em; }
.sub-q > li p { margin:.2em 0 .35em; }
.sub-form button { font:inherit; padding:.5em 1.4em; border:0; border-radius:4px; background:#3333b3; color:#fff; cursor:pointer; }
.sub-form button[disabled] { opacity:.6; }
.sub-msg.ok { color:#1a7a5e; font-weight:600; }
.sub-msg.bad { color:#b3200f; font-weight:600; }
@media (max-width:520px) { .sub-who { grid-template-columns:1fr; } }
</style>

<div id="submit-app" data-endpoint="{{ site.submit_endpoint }}"><p>Loading…</p></div>
<script src="/assets/submit/submit.js?v=5"></script>
