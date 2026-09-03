---
layout: default
title: "Fixtures & Results"
description: Upcoming korfball fixtures and recent results for Newport Centurions Korfball Club, competing in the Welsh Korfball League and Western Regional League.
permalink: /fixtures/
breadcrumb: "Fixtures"
keywords: newport centurions fixtures, korfball fixtures wales, welsh korfball league results, korfball results newport, korfball match schedule
---
{%- assign club = site.data.club -%}
{%- assign today = 'now' | date: '%Y-%m-%d' -%}

{%- comment -%}
  Fixtures come from _data/fixtures.yml, which is written by the
  sync-fixtures workflow from the club's Google Calendar. Nothing here is
  edited by hand.
{%- endcomment -%}

{%- assign all_fixtures = site.data.fixtures.fixtures | sort: 'date_iso' -%}
{%- assign upcoming = all_fixtures | where_exp: "f", "f.date_iso >= today" -%}
{%- assign past = all_fixtures | where_exp: "f", "f.date_iso < today" -%}

{%- if upcoming.size > 0 %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {%- for f in upcoming -%}
    {
      "@type": "SportsEvent",
      "name": {{ f.title | jsonify }},
      "sport": "Korfball",
      "startDate": "{{ f.date | date: '%Y-%m-%d' }}{% unless f.all_day %}T{{ f.start_time }}:00{% endunless %}",
      {%- unless f.all_day %}{% if f.end_time %}
      "endDate": "{{ f.date | date: '%Y-%m-%d' }}T{{ f.end_time }}:00",
      {%- endif %}{% endunless %}
      "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
      "eventStatus": "https://schema.org/ScheduledEvent",
      "location": {
        "@type": "Place",
        "name": {{ f.location | default: club.venue.name | jsonify }}
      },
      "organizer": {
        "@type": "SportsOrganization",
        "name": {{ club.name | jsonify }},
        "url": "{{ site.url }}"
      },
      "competitor": {
        "@type": "SportsTeam",
        "name": {{ club.name | jsonify }}
      }
    }{% unless forloop.last %},{% endunless %}
    {%- endfor %}
  ]
}
</script>
{%- endif %}

<div class="page-content">
  <div class="content-block">

    <h1>Fixtures &amp; Results</h1>
    <p class="intro">{{ club.short_name }} compete in the
      {% for l in club.leagues %}{{ l }}{% unless forloop.last %} and the {% endunless %}{% endfor %}.
      Fixtures are pulled straight from the club calendar.</p>

    {%- if site.data.fixtures.fixtures.size == 0 %}

    <p class="fixtures-empty">No fixtures published yet. Training runs
      {% include training.html format="short" separator=" and " %} at
      {{ club.venue.name }} &mdash; see <a href="/events/">upcoming events</a>
      or <a href="/contact/">get in touch</a>.</p>

    {%- else %}

    <section class="fixtures-section">
      <h2>Upcoming</h2>
      {%- if upcoming.size > 0 %}
      <ul class="fixture-list">
        {%- for f in upcoming %}
        {%- assign is_home = false -%}
        {%- if f.location contains club.venue.name or f.location contains club.venue.postcode -%}
          {%- assign is_home = true -%}
        {%- endif -%}
        <li class="fixture" data-fixture-date="{{ f.date | date: '%Y-%m-%d' }}">
          <div class="fixture-date">
            <span class="fixture-month">{{ f.date | date: '%b' | upcase }}</span>
            <span class="fixture-day">{{ f.date | date: '%-d' }}</span>
            <span class="fixture-year">{{ f.date | date: '%Y' }}</span>
          </div>
          <div class="fixture-details">
            <span class="fixture-tag {% if is_home %}tag-home{% else %}tag-away{% endif %}">{% if is_home %}Home{% else %}Away{% endif %}</span>
            <h3>{{ f.title }}</h3>
            <p class="fixture-meta">
              {%- unless f.all_day %}🕕 {{ f.start_time }}{% if f.end_time %}–{{ f.end_time }}{% endif %}{% endunless %}
              {%- if f.location %} · 📍 {{ f.location }}{% endif %}
            </p>
          </div>
        </li>
        {%- endfor %}
      </ul>
      {%- else %}
      <p class="fixtures-empty">Nothing scheduled at the moment &mdash; check back soon.</p>
      {%- endif %}
    </section>

    {%- if past.size > 0 %}
    <section class="fixtures-section">
      <h2>Recent</h2>
      <ul class="fixture-list fixture-list--past">
        {%- assign reversed_past = past | reverse %}
        {%- for f in reversed_past limit: 10 %}
        <li class="fixture fixture--past">
          <div class="fixture-date">
            <span class="fixture-month">{{ f.date | date: '%b' | upcase }}</span>
            <span class="fixture-day">{{ f.date | date: '%-d' }}</span>
            <span class="fixture-year">{{ f.date | date: '%Y' }}</span>
          </div>
          <div class="fixture-details">
            <h3>{{ f.title }}</h3>
            {%- if f.location %}
            <p class="fixture-meta">📍 {{ f.location }}</p>
            {%- endif %}
          </div>
        </li>
        {%- endfor %}
      </ul>
    </section>
    {%- endif %}

    {%- endif %}

    <div class="events-cta">
      <p>Want to play? {{ club.free_sessions_text }} &mdash; no experience needed.</p>
      <a href="/join-us/" class="modern-button">Join Us</a>
      <a href="/events/" class="cta-button">Training &amp; Events</a>
    </div>

    {%- if site.data.fixtures.generated %}
    <p class="fixtures-updated">Last updated {{ site.data.fixtures.generated | date: "%-d %B %Y" }} from the club calendar.</p>
    {%- endif %}

  </div>
</div>

<script>
// Move a fixture out of "Upcoming" once its date passes, so the list stays
// honest between the nightly rebuilds.
document.addEventListener('DOMContentLoaded', function () {
  var today = new Date();
  today.setHours(0, 0, 0, 0);

  document.querySelectorAll('.fixture[data-fixture-date]').forEach(function (el) {
    var when = new Date(el.getAttribute('data-fixture-date') + 'T23:59:59');
    if (when < today) { el.hidden = true; }
  });
});
</script>
