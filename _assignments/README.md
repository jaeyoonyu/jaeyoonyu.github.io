# Assignment settings (read by the Google Sheet script, not shown on the students' page)

One file per assignment, named `<id>.json` like the question file in `assets/assignments/`:

```json
{"code": "slice", "closes": "2026-12-03T23:59:00-05:00", "key": {"p2q1": ["750K", "750,000"], "p2q2": ["4"]}}
```

- `code`: word students must enter ("" for none). Also set `"code": true` in the question file so the page shows the box.
- `due`: submissions after this time are marked `late` in the Sheet but still accepted.
- `closes`: after this time submissions are refused (null to keep open). Use the -05:00 offset (Eastern).
- `key`: accepted answers per question id; numbers match within 0.5%, "$", "," and K/M suffixes are handled.
- A row in the Sheet's Assignments tab, if filled in, overrides these values. Changes reach the script within about 5 minutes.
