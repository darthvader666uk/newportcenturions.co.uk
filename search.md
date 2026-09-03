---
layout: default
title: "Search"
description: Search Newport Centurions Korfball Club for training times, korfball rules, FAQs and events.
permalink: /search/
sitemap: false
breadcrumb: "Search"
robots: "noindex, follow"
---

<div class="page-content">
  <div class="content-block">

    <h1>Search</h1>

    <form class="search-form" role="search" id="search-form" onsubmit="return false;">
      <label for="search-input" class="sr-only">Search this site</label>
      <input type="search" id="search-input" name="q" class="search-input"
             placeholder="Training times, korfball rules, how to join…"
             autocomplete="off" autocapitalize="off" spellcheck="false">
      <button type="submit" class="search-submit" aria-label="Search">
        <i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>
      </button>
    </form>

    <p class="search-status" id="search-status" role="status" aria-live="polite"></p>

    <div class="search-results" id="search-results"></div>

    <noscript>
      <p>Search needs JavaScript. You can browse the site from the menu, or try the
      <a href="/faq/">FAQ</a>, <a href="/glossary/">glossary</a> or
      <a href="/what-is-korfball/">what is korfball</a> pages.</p>
    </noscript>

  </div>
</div>

<script>
(function () {
  var input   = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var status  = document.getElementById('search-status');

  var index = null;
  var pending = null;

  // Common words match nearly every page and drown out the real signal.
  var STOPWORDS = ['a','an','and','are','as','at','be','but','by','can','do',
    'does','for','from','how','i','if','in','is','it','of','on','or','the',
    'to','we','what','when','where','who','why','you','your','with','my'];

  function loadIndex() {
    if (index) { return Promise.resolve(index); }
    return fetch('{{ "/search.json" | relative_url }}')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        index = data.filter(Boolean);   // trailing null from the Liquid loop
        return index;
      });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Score by where the term hits: title beats description beats body.
  // `phrase` is the whole query, used to reward an exact title match --
  // otherwise stopword stripping makes "what is korfball" score the same
  // on every page mentioning korfball.
  function score(entry, terms, phrase) {
    var title = (entry.title || '').toLowerCase();
    var desc  = ((entry.description || '') + ' ' + (entry.keywords || '')).toLowerCase();
    var body  = (entry.body || '').toLowerCase();
    var total = 0;

    var matched = 0;

    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      var hit = 0;
      if (title.indexOf(t) !== -1) { hit += title.indexOf(t) === 0 ? 12 : 8; }
      if (desc.indexOf(t) !== -1)  { hit += 4; }
      if (body.indexOf(t) !== -1)  { hit += 1; }
      if (hit > 0) { matched++; }
      total += hit;
    }

    if (matched === 0) { return 0; }

    if (phrase && phrase.length > 3 && title.indexOf(phrase) !== -1) {
      total += title.indexOf(phrase) === 0 ? 30 : 20;
    }
    // Reward documents that cover more of the query without excluding
    // partial matches entirely — "training times" should still find the
    // training pages even if the word "times" never appears.
    return total * (1 + matched / terms.length);
  }

  function snippet(entry, terms) {
    var body = entry.body || entry.description || '';
    var lower = body.toLowerCase();
    var at = -1;
    for (var i = 0; i < terms.length && at === -1; i++) {
      at = lower.indexOf(terms[i]);
    }
    if (at === -1) { return entry.description || body.slice(0, 160); }
    var start = Math.max(0, at - 70);
    var text = (start > 0 ? '…' : '') + body.slice(start, start + 200).trim() + '…';
    return text;
  }

  function highlight(text, terms) {
    var out = escapeHtml(text);
    terms.forEach(function (t) {
      if (!t) { return; }
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  }

  function render(query) {
    var q = query.trim().toLowerCase();

    if (q.length < 2) {
      results.innerHTML = '';
      status.textContent = q.length ? 'Keep typing…' : '';
      return;
    }

    var terms = q.split(/\s+/).filter(function (t) {
      return t && STOPWORDS.indexOf(t) === -1;
    });
    // All stopwords ("how do i")? Fall back to the raw words.
    if (!terms.length) { terms = q.split(/\s+/).filter(Boolean); }

    var matches = index
      .map(function (e) { return { entry: e, score: score(e, terms, q) }; })
      .filter(function (m) { return m.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, 20);

    if (!matches.length) {
      status.textContent = 'No results for "' + query.trim() + '".';
      results.innerHTML = '<p class="search-empty">Try a different word, or browse the ' +
        '<a href="/faq/">FAQ</a> or <a href="/glossary/">glossary</a>.</p>';
      return;
    }

    status.textContent = matches.length + (matches.length === 1 ? ' result' : ' results');
    results.innerHTML = matches.map(function (m) {
      var e = m.entry;
      return '<article class="search-result">' +
        '<h2><a href="' + escapeHtml(e.url) + '">' + highlight(e.title, terms) + '</a></h2>' +
        '<p>' + highlight(snippet(e, terms), terms) + '</p>' +
        '<p class="search-result-url">' + escapeHtml(e.url) + '</p>' +
        '</article>';
    }).join('');
  }

  function onInput() {
    var value = input.value;
    clearTimeout(pending);
    pending = setTimeout(function () {
      loadIndex().then(function () { render(value); }).catch(function () {
        status.textContent = 'Search is unavailable right now.';
      });
    }, 120);
  }

  input.addEventListener('input', onInput);

  // Support /search/?q=term and deep links from elsewhere
  var initial = new URLSearchParams(location.search).get('q');
  if (initial) {
    input.value = initial;
    onInput();
  }
  input.focus();
})();
</script>
