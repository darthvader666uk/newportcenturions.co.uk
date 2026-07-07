---
layout: default
title: Events – Newport Centurions Korfball Club
description: Upcoming events, training sessions, and beginner dates for Newport Centurions Korfball Club in Newport, Wales.
permalink: /events/
---

<div class="page-content">
  <div class="content-block">
  <h1>Events</h1>
  <p class="events-intro">Mark your calendar — here's what's coming up at Newport Centurions.</p>

  <div class="events-list">

    <div class="event-card event-highlight" data-event-date="2026-08-18">
      <div class="event-date">
        <span class="event-month">AUG</span>
        <span class="event-day">18</span>
        <span class="event-year">2026</span>
      </div>
      <div class="event-details">
        <span class="event-tag tag-season">Season Start</span>
        <h2>First Session Back</h2>
        <p>The 2026/27 season kicks off. Regular training resumes at John Frost School.</p>
        <p class="event-time">🕕 Tuesdays 6–8pm &amp; Thursdays 8–9pm</p>
      </div>
    </div>

    <div class="event-card event-beginner" data-event-date="2026-09-08">
      <div class="event-date">
        <span class="event-month">SEP</span>
        <span class="event-day">8</span>
        <span class="event-year">2026</span>
      </div>
      <div class="event-details">
        <span class="event-tag tag-beginner">Beginners Welcome</span>
        <h2>Beginner Session</h2>
        <p>Never played korfball? This is your chance. Turn up, give it a go — no experience needed.</p>
        <p class="event-time">🕕 6:00 PM – 8:00 PM · John Frost School</p>
      </div>
    </div>

    <div class="event-card event-beginner" data-event-date="2026-09-15">
      <div class="event-date">
        <span class="event-month">SEP</span>
        <span class="event-day">15</span>
        <span class="event-year">2026</span>
      </div>
      <div class="event-details">
        <span class="event-tag tag-beginner">Beginners Welcome</span>
        <h2>Beginner Session</h2>
        <p>Another chance to try korfball. First 2 sessions are free — come and see if it's for you.</p>
        <p class="event-time">🕕 6:00 PM – 8:00 PM · John Frost School</p>
      </div>
    </div>

    <div class="event-card event-beginner" data-event-date="2026-09-22">
      <div class="event-date">
        <span class="event-month">SEP</span>
        <span class="event-day">22</span>
        <span class="event-year">2026</span>
      </div>
      <div class="event-details">
        <span class="event-tag tag-beginner">Beginners Welcome</span>
        <h2>Beginner Session</h2>
        <p>Last beginner session of the intake. Don't miss your chance to join this season.</p>
        <p class="event-time">🕕 6:00 PM – 8:00 PM · John Frost School</p>
      </div>
    </div>

  </div>

  <div class="events-cta">
    <p>All sessions held at <strong>The John Frost School, Duffryn, NP10 8YD</strong>.</p>
    <p>First 2 sessions are free. No kit needed — just turn up in sportswear.</p>
    <a href="/join-us/" class="modern-button">Join Us</a>
    <a href="/contact/" class="cta-button">Questions? Contact Us</a>
  </div>

  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var cards = document.querySelectorAll('.event-card[data-event-date]');
  var visibleCount = 0;

  cards.forEach(function(card) {
    var eventDate = new Date(card.getAttribute('data-event-date') + 'T23:59:59');
    if (eventDate < today) {
      card.style.display = 'none';
      card.setAttribute('aria-hidden', 'true');
    } else {
      visibleCount++;
    }
  });

  if (visibleCount === 0) {
    var list = document.querySelector('.events-list');
    if (list) {
      list.innerHTML = '<p style="text-align:center; color: var(--text-muted); padding: 2rem 0;">No upcoming events right now. Check back soon!</p>';
    }
  }
});
</script>
