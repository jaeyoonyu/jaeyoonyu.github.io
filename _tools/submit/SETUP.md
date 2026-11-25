# Class submissions: one-time setup (about 10 minutes)

Students answer on the site (`/submit/?a=<assignment id>`); every answer lands in one Google Sheet.
Questions live in this repository (`assets/assignments/<id>.json`); answers, roster, answer keys and
submission codes live only in the Sheet.

## 1. Make the Sheet and paste the script
1. Create a new Google Sheet (e.g. "ACC250 Submissions").
2. Extensions > Apps Script. Delete what is there, paste all of `_tools/submit/Code.gs`, click Save.
3. In the function menu at the top choose `setup`, click Run, and allow the permissions it asks for
   ("unverified app" warning: Advanced > Go to project). The Sheet now has the tabs
   Roster, Assignments, Gradebook, Questions, Log.

## 2. Publish it as a web app
1. Deploy > New deployment > gear icon > Web app.
2. Execute as: **Me**. Who has access: **Anyone**. Deploy.
3. Copy the Web app URL (ends in `/exec`) and give it to Claude (it goes in `_config.yml` as `submit_endpoint`).
   If you later change the script, use Deploy > Manage deployments > edit > New version, so the URL stays the same.

## 3. Paste the roster
Roster tab: Name | Email | Section, one student per row (from the LMS export). Only these emails can submit.

## 4. Each assignment
Claude adds two files to the repository: the questions (`assets/assignments/<id>.json`, shown on the page) and the
settings (`_assignments/<id>.json`: code, close time, answer key; read only by the script, never shown on the page).
Nothing to do in the Sheet. A filled-in row in the Assignments tab (ID | Title | Code | Closes | Key, Key as
`q1=750K|750,000; q2=4`) overrides the file, for a change you want to make yourself.

## Where to look
- **Gradebook**: one row per student, one column per assignment: the total, `submitted` (text-only work not yet scored) or `missing`.
- **<assignment id> tab**: each student's latest answers, `Auto` score, a `Manual` column you fill in, `Total`.
- **Questions**: the exact question text students answered. **Log**: every submission, resubmissions included.
- To rebuild the Gradebook after editing the roster: Apps Script > run `rebuildGradebook`.

## Reading the answers from the course report (optional)
`doGet` answers `?action=submissions&key=<READ_KEY>` with every student's latest submission per assignment (JSONP with `&callback=`).
1. Apps Script > Project Settings > Script properties > add `READ_KEY` with a long random value (keep it out of this repository).
2. Deploy > Manage deployments > edit > New version.
Without the right key the answer is only "Submission service is running."
