// Class submission form: /submit/?a=<assignment id> reads /assets/assignments/<id>.json and posts to the
// Google Apps Script web app set as submit_endpoint in _config.yml (see _tools/submit/SETUP.md).
(function () {
  var box = document.getElementById('submit-app');
  if (!box) return;
  var endpoint = box.getAttribute('data-endpoint');
  var id = (new URLSearchParams(location.search).get('a') || '').replace(/[^a-z0-9-]/gi, '');
  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text != null) e.textContent = text;
    return e;
  }
  function say(msg, ok) { var p = el('p', {class: 'sub-msg ' + (ok ? 'ok' : 'bad')}, msg); box.replaceChildren(p); }
  if (!id) return fetch('/assets/assignments/index.json').then(function (r) { return r.json(); }).then(function (list) {
    box.replaceChildren(el('p', {}, 'Choose an assignment:'));
    var ul = el('ul');
    list.filter(function (a) { return !a.hidden; }).forEach(function (a) { var li = el('li'); li.append(el('a', {href: '?a=' + a.id}, a.title)); ul.append(li); });
    box.append(ul);
  }).catch(function () { say('No assignment selected.', false); });

  fetch('/assets/assignments/' + id + '.json', {cache: 'no-store'}).then(function (r) {
    if (!r.ok) throw new Error('missing'); return r.json();
  }).then(function (a) {
    document.title = a.title;
    var form = el('form', {class: 'sub-form', novalidate: ''});
    form.append(el('h2', {}, a.title));
    var meta = el('p', {class: 'sub-meta'});
    meta.append(document.createTextNode((a.course ? a.course + ' \u00b7 ' : '') + 'Due: ' + (a.due || '\u2014')));
    if (a.reading) { meta.append(document.createTextNode(' \u00b7 ')); meta.append(el('a', {href: a.reading.url, target: '_blank'}, a.reading.label)); }
    form.append(meta);
    if (a.note) form.append(el('p', {class: 'sub-note'}, a.note));

    var who = el('div', {class: 'sub-who'});
    var em = el('input', {type: 'email', id: 'sub-email', autocomplete: 'email', placeholder: 'yourid@cmich.edu', required: ''});
    try { em.value = localStorage.getItem('sub-email') || ''; } catch (e) {}
    var l1 = el('label', {for: 'sub-email'}, 'CMU email'); who.append(l1, em);
    var code = null;
    if (a.code) { code = el('input', {type: 'text', id: 'sub-code', autocomplete: 'off', placeholder: 'given in class'}); who.append(el('label', {for: 'sub-code'}, 'Submission code'), code); }
    form.append(who);
    if (!endpoint) form.append(el('p', {class: 'sub-msg bad'}, 'Submissions are not open yet. You can read the questions now.'));

    var qs = [];
    (a.sections || [{questions: a.questions}]).forEach(function (s) {
      if (s.title) form.append(el('h3', {}, s.title));
      var ol = el('ol', {class: 'sub-q'});
      s.questions.forEach(function (q) {
        var li = el('li'); var pq = el('p'); if (q.label) { li.className = 'lab'; pq.append(el('b', {}, q.label + '. ')); } pq.append(document.createTextNode(q.text)); li.append(pq); var inp;
        if (q.type === 'choice') {
          inp = el('select', {id: 'q-' + q.id}); inp.append(el('option', {value: ''}, 'Choose\u2026'));
          q.choices.forEach(function (c) { inp.append(el('option', {value: c}, c)); });
        } else if (q.type === 'number') {
          inp = el('input', {type: 'text', id: 'q-' + q.id, inputmode: 'decimal', autocomplete: 'off'});
        } else {
          inp = el('textarea', {id: 'q-' + q.id, rows: '4'});
        }
        li.append(inp); ol.append(li); qs.push({q: q, inp: inp});
      });
      form.append(ol);
    });
    var btn = el('button', {type: 'submit'}, 'Submit');
    var msg = el('p', {class: 'sub-msg', 'aria-live': 'polite'});
    form.append(btn, msg);
    box.replaceChildren(form);

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!endpoint) { msg.className = 'sub-msg bad'; msg.textContent = 'Submissions are not open yet.'; return; }
      var email = em.value.trim();
      if (!/^\S+@\S+\.\S+$/.test(email)) { msg.className = 'sub-msg bad'; msg.textContent = 'Enter your CMU email.'; em.focus(); return; }
      var answers = {}, blank = 0;
      qs.forEach(function (x) { answers[x.q.id] = x.inp.value.trim(); if (!answers[x.q.id]) blank++; });
      try { localStorage.setItem('sub-email', email); } catch (e) {}
      btn.disabled = true; msg.className = 'sub-msg'; msg.textContent = 'Sending\u2026';
      var body = {assignment: a.id, title: a.title, email: email, code: code ? code.value.trim() : '', answers: answers,
        questions: qs.map(function (x) { return {id: x.q.id, text: x.q.text, type: x.q.type, points: x.q.points || 0}; })};
      fetch(endpoint, {method: 'POST', headers: {'Content-Type': 'text/plain;charset=utf-8'}, body: JSON.stringify(body)})
        .then(function (r) { return r.json(); })
        .then(function (res) {
          msg.className = 'sub-msg ' + (res.ok ? 'ok' : 'bad');
          msg.textContent = res.message + (res.ok && blank ? ' (' + blank + ' question' + (blank > 1 ? 's were' : ' was') + ' left blank.)' : '');
        })
        .catch(function () { msg.className = 'sub-msg bad'; msg.textContent = 'Could not reach the submission service. Check your connection and try again.'; })
        .then(function () { btn.disabled = false; });
    });
  }).catch(function () { say('This assignment was not found. Check the link.', false); });
})();
