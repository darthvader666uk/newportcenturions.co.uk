---
layout: default
title: Newport Centurions Korfball Club
description: Join Newport Centurions Korfball Club - South Wales' premier mixed-gender korfball team. Weekly training in Newport. Welsh League Champions.
seo_title: false
keywords: korfball, newport korfball, welsh korfball, mixed gender sport, korfball club, korfball training, korfball wales, join korfball, korfball beginners, korfball south wales
---

{% include ai-answer-snippets.html %}

<div class="modern-container" itemscope itemtype="https://schema.org/SportsTeam">

    <!-- Hero: Bold headline + stats strip -->
    <section class="hero-section">
        <picture class="logo-modern">
            <source srcset="images/newport-centurions-korfball-club-400.webp 400w, images/newport-centurions-korfball-club-800.webp 800w" sizes="(max-width: 768px) 80vw, 300px" type="image/webp">
            <img src="images/newport-centurions-korfball-club-400.webp" srcset="images/newport-centurions-korfball-club-400.webp 400w, images/newport-centurions-korfball-club-800.webp 800w" sizes="(max-width: 768px) 80vw, 300px" alt="Newport Centurions Korfball Club" class="logo" width="400" height="400" loading="eager" fetchpriority="high" itemprop="logo">
        </picture>
        <h1 class="hero-headline" itemprop="name">Play Mixed-Gender Korfball in Newport</h1>
        <p class="hero-subline">South Wales' premier korfball club. Beginners welcome.</p>
        <div class="stats-strip">
            <div class="stat"><span class="stat-number">{{ site.data.club.members }}</span><span class="stat-label">Members</span></div>
            <div class="stat-divider"></div>
            <div class="stat"><span class="stat-number">{{ site.data.club.teams }}</span><span class="stat-label">Teams</span></div>
            <div class="stat-divider"></div>
            <div class="stat"><span class="stat-number">{{ site.data.club.titles_count }}×</span><span class="stat-label">Champions</span></div>
        </div>
    </section>



    <!-- Training + Social grid -->
    <div class="content-grid">
        <section class="training-info glass-morphism">
            <h2>Next Training</h2>
            <div class="training-sessions">
                {%- for session in site.data.club.training %}
                <div class="training-session upcoming">
                    <strong>{{ session.day }}s</strong> — {{ session.display }}
                </div>
                {%- endfor %}
            </div>
            <p class="training-venue">{{ site.data.club.venue.name }}, {{ site.data.club.venue.locality }}</p>
            <a href="{{ site.data.club.venue.maps_url }}" target="_blank" rel="noopener noreferrer" class="modern-button">Get Directions</a>
        </section>

        <section class="social-section">
            <h2 class="follow-header" id="follow-us">Connect With Us</h2>
            <nav class="social-links" aria-label="Social Media Links">
                {%- for link in site.data.club.social %}
                <a href="{{ link.url }}" class="social-link" aria-label="Follow us on {{ link.name }}" rel="noopener noreferrer" target="_blank"><i class="fab {{ link.icon }}" aria-hidden="true"></i></a>
                {%- endfor %}
            </nav>
        </section>
    </div>

</div>
