/**
 * Class submissions for jaeyoonyu.github.io
 * One Google Sheet receives every assignment's answers. Paste this whole file into
 * Extensions > Apps Script of that Sheet, run `setup` once, then Deploy > New deployment > Web app
 * (Execute as: Me, Who has access: Anyone). See SETUP.md.
 *
 * Tabs (created by `setup`):
 *   Roster       Name | Email | Section            (paste from the LMS)
 *   Assignments  ID | Title | Code | Closes | Key  (one row per assignment; Code, Closes, Key optional)
 *   Gradebook    built automatically: one row per student, one column per assignment
 *   Questions    question text of each assignment, saved with the first submission
 *   Log          every submission, including resubmissions
 *   <ID>         one tab per assignment: the latest submission of each student
 *
 * Key format: q1=750K|750,000; q2=4; q4a=decrease   (alternatives separated by |, items by ;)
 * Numbers match if within 0.5%; "$", "," and spaces are ignored; K and M suffixes are read as thousands and millions.
 */

var TABS = {
  Roster: ['Name', 'Email', 'Section'],
  Assignments: ['ID', 'Title', 'Code', 'Closes', 'Key'],
  Gradebook: ['Name', 'Email', 'Section'],
  Questions: ['Saved', 'Assignment', 'Item', 'Question', 'Type', 'Points'],
  Log: ['Time', 'Assignment', 'Email', 'Answers (JSON)']
};

function setup() {
  var ss = SpreadsheetApp.getActive();
  Object.keys(TABS).forEach(function (name) {
    var sh = ss.getSheetByName(name) || ss.insertSheet(name);
    if (sh.getLastRow() === 0) {
      sh.appendRow(TABS[name]);
      sh.getRange(1, 1, 1, TABS[name].length).setFontWeight('bold');
      sh.setFrozenRows(1);
    }
  });
  var first = ss.getSheets()[0];
  if (first.getName() === 'Sheet1' && first.getLastRow() === 0) ss.deleteSheet(first);
  ss.setActiveSheet(ss.getSheetByName('Gradebook'));
}

function doGet() {
  return json_({ok: true, message: 'Submission service is running.'});
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var p = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActive();
    var id = String(p.assignment || '').trim();
    var email = String(p.email || '').trim().toLowerCase();
    if (!/^[a-z0-9][a-z0-9-]{0,60}$/.test(id)) return json_({ok: false, message: 'Unknown assignment.'});
    if (!email) return json_({ok: false, message: 'Enter your email.'});

    // roster check
    var roster = rows_(ss.getSheetByName('Roster'));
    var student = null;
    roster.forEach(function (r) { if (String(r.Email).trim().toLowerCase() === email) student = r; });
    if (roster.length && !student) return json_({ok: false, message: 'This email is not on the class roster. Check the spelling (use your CMU email).'});
    student = student || {Name: '', Email: email, Section: ''};

    // assignment settings (optional row)
    var conf = null;
    rows_(ss.getSheetByName('Assignments')).forEach(function (r) { if (String(r.ID).trim() === id) conf = r; });
    if (conf && String(conf.Code).trim() && String(conf.Code).trim().toLowerCase() !== String(p.code || '').trim().toLowerCase())
      return json_({ok: false, message: 'The submission code is not correct.'});
    if (conf && conf.Closes && new Date() > new Date(conf.Closes))
      return json_({ok: false, message: 'Submissions for this assignment are closed.'});
    if (!conf) {
      ss.getSheetByName('Assignments').appendRow([id, p.title || id, '', '', '']);
      conf = {ID: id, Title: p.title || id, Code: '', Closes: '', Key: ''};
    }

    var items = (p.questions || []).map(function (q) { return {id: String(q.id), text: String(q.text || ''), type: q.type || 'text', points: Number(q.points || 0)}; });
    var answers = p.answers || {};
    saveQuestions_(ss, id, items);
    ss.getSheetByName('Log').appendRow([new Date(), id, email, safe_(JSON.stringify(answers))]);

    // per-assignment tab: latest submission per student
    var key = parseKey_(conf.Key);
    var auto = 0, autoMax = 0;
    items.forEach(function (q) {
      if (key[q.id]) { autoMax += q.points || 1; if (matches_(answers[q.id], key[q.id])) auto += q.points || 1; }
    });
    var sh = ss.getSheetByName(id);
    var head = ['Time', 'Name', 'Email', 'Section'].concat(items.map(function (q) { return q.id; })).concat(['Auto', 'Manual', 'Total']);
    if (!sh) {
      sh = ss.insertSheet(id);
      sh.appendRow(head);
      sh.getRange(1, 1, 1, head.length).setFontWeight('bold');
      sh.setFrozenRows(1);
    }
    var cols = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
    items.forEach(function (q) {   // a question added later gets its own column before Auto
      if (cols.indexOf(q.id) < 0) { var at = cols.indexOf('Auto') + 1; sh.insertColumnBefore(at); sh.getRange(1, at).setValue(q.id).setFontWeight('bold'); cols = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0]; }
    });
    var emailCol = cols.indexOf('Email') + 1;
    var row = 0, n = sh.getLastRow();
    if (n > 1) {
      var em = sh.getRange(2, emailCol, n - 1, 1).getValues();
      for (var i = 0; i < em.length; i++) if (String(em[i][0]).toLowerCase() === email) { row = i + 2; break; }
    }
    if (!row) row = n + 1;
    var manualCol = cols.indexOf('Manual') + 1, autoCol = cols.indexOf('Auto') + 1, totalCol = cols.indexOf('Total') + 1;
    var keepManual = row <= n ? sh.getRange(row, manualCol).getValue() : '';
    var vals = cols.map(function (c) {
      if (c === 'Time') return new Date();
      if (c === 'Name') return student.Name;
      if (c === 'Email') return email;
      if (c === 'Section') return student.Section;
      if (c === 'Auto') return autoMax ? auto : '';
      if (c === 'Manual') return keepManual;
      if (c === 'Total') return '';
      return answers.hasOwnProperty(c) ? safe_(answers[c]) : '';
    });
    sh.getRange(row, 1, 1, vals.length).setValues([vals]);
    var a1 = function (c) { return sh.getRange(row, c).getA1Notation(); };
    sh.getRange(row, totalCol).setFormula('=IF(AND(' + a1(autoCol) + '="",' + a1(manualCol) + '=""),"submitted",N(' + a1(autoCol) + ')+N(' + a1(manualCol) + '))');
    rebuildGradebook_(ss);
    return json_({ok: true, message: 'Submitted. Thank you' + (student.Name ? ', ' + student.Name : '') + '. You can resubmit until the assignment closes; the last one counts.'});
  } catch (err) {
    return json_({ok: false, message: 'Something went wrong: ' + err.message});
  } finally {
    lock.releaseLock();
  }
}

function rebuildGradebook() { rebuildGradebook_(SpreadsheetApp.getActive()); }

function rebuildGradebook_(ss) {
  var gb = ss.getSheetByName('Gradebook');
  var roster = rows_(ss.getSheetByName('Roster'));
  var ids = rows_(ss.getSheetByName('Assignments')).map(function (r) { return String(r.ID).trim(); })
    .filter(function (id) { return id && ss.getSheetByName(id); });
  var head = ['Name', 'Email', 'Section'].concat(ids);
  var out = [head];
  roster.forEach(function (r, i) {
    var line = [r.Name, String(r.Email).trim().toLowerCase(), r.Section];
    ids.forEach(function (id) {
      var q = "'" + id.replace(/'/g, "''") + "'";
      line.push('=IFERROR(INDEX(' + q + '!$A:$ZZ, MATCH($B' + (i + 2) + ', ' + q + '!$C:$C, 0), MATCH("Total", ' + q + '!$1:$1, 0)), "missing")');
    });
    out.push(line);
  });
  gb.clearContents();
  gb.getRange(1, 1, out.length, head.length).setValues(out);
  gb.getRange(1, 1, 1, head.length).setFontWeight('bold');
  gb.setFrozenRows(1);
  if (gb.getConditionalFormatRules().length === 0) {
    var rng = gb.getRange('D2:ZZ');
    gb.setConditionalFormatRules([SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('missing').setFontColor('#b3200f').setRanges([rng]).build()]);
  }
}

function saveQuestions_(ss, id, items) {
  var sh = ss.getSheetByName('Questions');
  var have = {};
  rows_(sh).forEach(function (r) { if (r.Assignment === id) have[r.Item] = r.Question; });
  var now = new Date();
  items.forEach(function (q) {
    if (have[q.id] !== q.text) sh.appendRow([now, id, q.id, q.text, q.type, q.points]);
  });
}

function parseKey_(s) {
  var k = {};
  String(s || '').split(';').forEach(function (part) {
    var i = part.indexOf('=');
    if (i > 0) k[part.slice(0, i).trim()] = part.slice(i + 1).split('|').map(function (a) { return a.trim(); });
  });
  return k;
}

function num_(s) {
  var t = String(s == null ? '' : s).toLowerCase().replace(/[\s$,]/g, '');
  var m = t.match(/^\(?(-?\d*\.?\d+)(k|m|b)?\)?%?$/);
  if (!m) return null;
  var v = parseFloat(m[1]) * ({k: 1e3, m: 1e6, b: 1e9}[m[2]] || 1);
  return /^\(.*\)$/.test(t) ? -v : v;
}

function matches_(ans, accepted) {
  var a = String(ans == null ? '' : ans).trim().toLowerCase();
  if (!a) return false;
  return accepted.some(function (k) {
    var x = num_(a), y = num_(k);
    if (x !== null && y !== null) return Math.abs(x - y) <= Math.max(1e-9, Math.abs(y) * 0.005);
    return a.replace(/\s+/g, ' ') === k.toLowerCase().replace(/\s+/g, ' ');
  });
}

function rows_(sh) {
  if (!sh || sh.getLastRow() < 2) return [];
  var v = sh.getDataRange().getValues(), h = v[0];
  return v.slice(1).filter(function (r) { return r.join('') !== ''; }).map(function (r) {
    var o = {}; h.forEach(function (c, i) { o[c] = r[i]; }); return o;
  });
}

function safe_(v) {   // keep a typed answer as text, never as a formula
  var s = String(v == null ? '' : v).slice(0, 5000);
  return /^[=+@]/.test(s) || /^-[^\d.]/.test(s) ? "'" + s : s;
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
