---
layout: default
title: "Training & Events"
description: Upcoming events, training sessions, and beginner dates for Newport Centurions Korfball Club. Find out when and where we train in Newport, Wales.
permalink: /events/
breadcrumb: "Events"
---
{%- assign club = site.data.club -%}
{%- assign venue = club.venue -%}

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {%- for event in club.season.events %}
    {
      "@type": "Event",
      "name": "{{ club.short_name }} {{ event.title }}",
      "description": {{ event.schema_description | jsonify }},
      "startDate": "{{ event.date | date: '%Y-%m-%d' }}T{{ event.start_time }}:00+01:00",
      "endDate": "{{ event.date | date: '%Y-%m-%d' }}T{{ event.end_time }}:00+01:00",
      "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
      "eventStatus": "https://schema.org/ScheduledEvent",
      "location": {
        "@type": "Place",
        "name": {{ venue.name | jsonify }},
        "address": {
          "@type": "PostalAddress",
          "streetAddress": {{ venue.street | jsonify }},
          "addressLocality": {{ venue.locality | jsonify }},
          "postalCode": {{ venue.postcode | jsonify }},
          "addressCountry": {{ venue.country | jsonify }}
        }
      },
      "organizer": {
        "@type": "SportsOrganization",
        "name": {{ club.name | jsonify }},
        "url": "{{ site.url }}"
      },
      "performer": {
        "@type": "SportsOrganization",
        "name": {{ club.name | jsonify }}
      },
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "GBP",
        "description": {{ club.free_sessions_text | jsonify }}
      }
    }{% unless forloop.last %},{% endunless %}
    {%- endfor %}
  ]
}
</script>

<div class="page-content">
  <div class="content-block">
  <h1>Events</h1>
  <p class="events-intro">Mark your calendar — here's what's coming up at Newport Centurions.</p>

  <div class="events-list">
    {%- for event in club.season.events %}

    <div class="event-card {{ event.card_class }}" data-event-date="{{ event.date | date: '%Y-%m-%d' }}">
      <div class="event-date">
        <span class="event-month">{{ event.date | date: '%b' | upcase }}</span>
        <span class="event-day">{{ event.date | date: '%-d' }}</span>
        <span class="event-year">{{ event.date | date: '%Y' }}</span>
      </div>
      <div class="event-details">
        <span class="event-tag {{ event.tag_class }}">{{ event.tag }}</span>
        <h2>{{ event.title }}</h2>
        <p>{{ event.description }}{% if event.beginner %} {{ club.free_sessions_text }}.{% endif %}</p>
        <p class="event-time">🕕 {{ event.time_display }}{% unless event.card_class == 'event-highlight' %} · {{ venue.name }}{% endunless %}</p>
      </div>
    </div>
    {%- endfor %}

    <p class="events-empty" hidden>No dates in the diary right now — but training runs
      {% for t in club.training %}{{ t.day }}s {{ t.display }}{% unless forloop.last %} and {% endunless %}{% endfor %}
      all season. <a href="/contact/">Get in touch</a> and come along.</p>

  </div>

  <div class="events-cta">
    <p>All sessions held at <strong>{{ venue.name }}, {{ venue.street }}, {{ venue.postcode }}</strong>.</p>
    <p>{{ club.free_sessions_text }}. No kit needed — just turn up in sportswear.</p>
    <a href="/join-us/" class="modern-button">Join Us</a>
    <a href="/contact/" class="cta-button">Questions? Contact Us</a>
  </div>

  </div>
</div>

<script>
// Hide events whose date has passed. Runs client-side so the page stays
// accurate between rebuilds, not just at build time.
document.addEventListener('DOMContentLoaded', function () {
  var today = new Date();
  today.setHours(0, 0, 0, 0);

  var cards = document.querySelectorAll('.event-card[data-event-date]');
  var visible = 0;

  cards.forEach(function (card) {
    var when = new Date(card.getAttribute('data-event-date') + 'T23:59:59');
    if (when < today) {
      card.hidden = true;
    } else {
      visible++;
    }
  });

  if (visible === 0) {
    var empty = document.querySelector('.events-empty');
    if (empty) { empty.hidden = false; }
  }
});
</script>
