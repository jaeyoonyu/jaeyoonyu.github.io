---
layout: page
title: "CMU"
---

{% raw %}
<style>
.cmu { --accent: #1a7a5e; --line: rgba(128,128,128,.25); --muted: #5c6863; --card: rgba(255,255,255,.7);
  display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; margin-top: 8px; }
@media (prefers-color-scheme: dark) {
  .cmu { --accent: #53c79e; --muted: #96a29b; --card: rgba(255,255,255,.03); }
}
.cmu a.card { display: block; border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px;
  background: var(--card); box-shadow: 0 1px 3px rgba(0,0,0,.06); text-decoration: none; color: inherit;
  transition: border-color .15s, transform .15s; }
.cmu a.card:hover { border-color: var(--accent); transform: translateY(-1px); }
.cmu .tag { font-size: 10px; text-transform: uppercase; letter-spacing: .08em; color: var(--accent); font-weight: 600; }
.cmu .name { font-family: Charter, "Bitstream Charter", Cambria, Georgia, serif; font-size: 17px; margin: 3px 0 4px; }
.cmu .name::after { content: " ↗"; color: var(--accent); font-size: 14px; }
.cmu .desc { font-size: 13px; color: var(--muted); line-height: 1.35; }
</style>

<div class="cmu">
  <a class="card" href="https://www.cmich.edu/centrallink" target="_blank" rel="noopener">
    <div class="tag">Portal</div><div class="name">CentralLink</div>
    <div class="desc">Single sign-on portal for CMU apps and services</div></a>
  <a class="card" href="https://blackboard.cmich.edu/" target="_blank" rel="noopener">
    <div class="tag">Teaching</div><div class="name">Blackboard</div>
    <div class="desc">Course sites, grades, and assignments</div></a>
  <a class="card" href="https://classlist.apps.cmich.edu/" target="_blank" rel="noopener">
    <div class="tag">Teaching</div><div class="name">Class List</div>
    <div class="desc">Enrolled students by section</div></a>
  <a class="card" href="https://courseregistration.apps.cmich.edu/?academicTerm=2027500&amp;departments=ACC" target="_blank" rel="noopener">
    <div class="tag">Teaching</div><div class="name">Course Registration — ACC</div>
    <div class="desc">ACC course sections and seats (term 2027500)</div></a>
  <a class="card" href="https://www.cmich.edu/offices-departments/registrars-office/calendars/academic-calendar" target="_blank" rel="noopener">
    <div class="tag">Calendar</div><div class="name">Academic Calendar</div>
    <div class="desc">Term dates, breaks, and deadlines</div></a>
  <a class="card" href="https://www.cmich.edu/offices-departments/faculty-personnel-services/collective-bargaining-agreements-union-information" target="_blank" rel="noopener">
    <div class="tag">Faculty</div><div class="name">Collective Bargaining Agreements</div>
    <div class="desc">Faculty contracts and union information</div></a>
  <a class="card" href="https://www.cmich.edu/offices-departments/finance-administrative-services/financial-services-reporting/travel-business-expenses" target="_blank" rel="noopener">
    <div class="tag">Finance</div><div class="name">Travel &amp; Business Expenses</div>
    <div class="desc">Travel policy, reimbursement, and expense forms</div></a>
  <a class="card" href="https://www.cmich.edu/offices-departments/finance-administrative-services/financial-services-reporting/travel-business-expenses/mileage-reimbursement#Official-CMU-mileage-chart" target="_blank" rel="noopener">
    <div class="tag">Finance</div><div class="name">Mileage Reimbursement</div>
    <div class="desc">Official CMU mileage chart and rates</div></a>
  <a class="card" href="https://centralmichigan-my.sharepoint.com" target="_blank" rel="noopener">
    <div class="tag">Files</div><div class="name">SharePoint</div>
    <div class="desc">OneDrive / SharePoint files</div></a>
  <a class="card" href="https://connect.edu.mheducation.com/instructor/courses" target="_blank" rel="noopener">
    <div class="tag">Teaching</div><div class="name">McGraw Hill Connect</div>
    <div class="desc">Instructor course list</div></a>
  <a class="card" href="https://help.anthology.com/blackboard/instructor/en/assessments/questions/reuse-questions/upload-or-import-questions.html" target="_blank" rel="noopener">
    <div class="tag">Teaching</div><div class="name">Blackboard Question Import</div>
    <div class="desc">File format for uploading test questions</div></a>
</div>
{% endraw %}
