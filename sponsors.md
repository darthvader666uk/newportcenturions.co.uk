---
title: "Sponsors - Newport Centurions Korfball Club"
description: "Meet our valued sponsors supporting Newport Centurions Korfball Club. Discover sponsorship opportunities for sports partnerships in South Wales korfball."
layout: default
permalink: /sponsors/
canonical_url: "https://newportcenturions.co.uk/sponsors/"
image: /assets/images/sponsors/hazlewoods-logo.png
image_alt: "Newport Centurions Korfball Club sponsors and partners"

# SEO Meta Tags
keywords: "korfball sponsors, Newport Centurions sponsors, sports sponsorship Wales, korfball club partnerships, South Wales sponsors, sports team sponsorship, official partners, business sponsorship opportunities"
robots: "index, follow, max-image-preview:large"
og_type: "website"
og_url: "https://newportcenturions.co.uk/sponsors/"
og_title: "Our Valued Sponsors - Newport Centurions Korfball Club"
og_description: "Discover our valued sponsors including Hazlewoods, who support Newport Centurions Korfball Club in South Wales."
og_image: "/assets/images/sponsors/hazlewoods-logo.png"
twitter_card: "summary_large_image"
twitter_title: "Newport Centurions Korfball Club Sponsors"
twitter_description: "Discover sponsorship opportunities and our valued partner organizations"
twitter_image: "/assets/images/sponsors/hazlewoods-logo.png"

# AI Search Optimization
schema_type: "OrganizationSponsorship"
ai_keywords:
  - "korfball club sponsors"
  - "sports sponsorship opportunities Wales"
  - "community partnership Newport"
  - "local business sponsorship sports"
  - "sports team sponsorship UK"
  - "Hazlewoods Newport Centurions"
  - "official sports partners Wales"
  - "mixed-gender korfball partnerships"
  - "sports club partnership programs"
  - "corporate sponsorship korfball"

# Article metadata for AI
article_type: "sponsored-content"
publish_date: 2025-11-04
update_date: 2025-11-04

# For search engine visibility
content_type: "partnership-page"
target_audience: "local-businesses,sponsors,korfball-community"
---

<div class="page-content">
  <div class="content-block">
    <div class="sponsors-hero">
      <h1 itemprop="name" role="heading">Our Valued Sponsors</h1>
      <p class="lead" itemprop="description">
        Newport Centurions Korfball Club partners with leading organizations who share our commitment to korfball in South Wales. Our sponsors provide essential support for our team's development.
      </p>
    </div>

<!-- Sponsors List -->

{% if site.data.sponsors.sponsors %}

<section class="sponsors-grid" vocab="https://schema.org/" typeof="Organization">

{% assign featured_sponsors = site.data.sponsors.sponsors | where: "featured", true %}

{% if featured_sponsors.size > 0 %}

  <div class="sponsors-list">
    {% for sponsor in featured_sponsors %}
    <div class="sponsor-card featured" itemscope itemtype="https://schema.org/Organization" role="region" aria-label="{{ sponsor.name }} sponsor information">
      {% if sponsor.logo %}
      <img src="{{ sponsor.logo }}" alt="{{ sponsor.logo_alt }}" class="sponsor-logo" loading="lazy" width="200" height="100" itemprop="image">
      {% endif %}
      <p class="sponsor-category"><strong>{{ sponsor.category }}</strong></p>
      <p class="sponsor-type" itemprop="description">{{ sponsor.description }}</p>
      {% if sponsor.website %}
      <a href="{{ sponsor.website }}" target="_blank" rel="noopener noreferrer" class="sponsor-link" title="Visit {{ sponsor.name }}">Learn More →</a>
      {% endif %}
    </div>
    {% endfor %}
  </div>
{% endif %}

{% assign all_sponsors = site.data.sponsors.sponsors | where: "featured", false %}
{% if all_sponsors.size > 0 %}

<div class="sponsors-all">
  <h3>Our Partners</h3>
  <div class="sponsors-list">
    {% for sponsor in all_sponsors %}
    <div class="sponsor-card" itemscope itemtype="https://schema.org/Organization" role="region" aria-label="{{ sponsor.name }} sponsor information">
      {% if sponsor.logo %}
      <img src="{{ sponsor.logo }}" alt="{{ sponsor.logo_alt }}" class="sponsor-logo" loading="lazy" width="150" height="80" itemprop="image">
      {% endif %}
      <h4 itemprop="name">{{ sponsor.name }}</h4>
      <p class="sponsor-category">{{ sponsor.category }}</p>
      <p class="sponsor-type" itemprop="description">{{ sponsor.description }}</p>
    </div>
    {% endfor %}
  </div>
</div>
{% endif %}

{% endif %}

<!-- Team Kits Section -->
<section class="team-kits" itemscope itemtype="https://schema.org/SportsTeam">
  <h2 itemprop="name">Our Teams</h2>
  <p class="team-intro" itemprop="description">Representing Newport Centurions in distinctive Home and Away Kits</p>

  <div class="kits-container">
    <div class="kit-card" role="article" aria-label="Home Kit">
      <div class="kit-image">
        <img src="/assets/images/team/home-kit.jpg" alt="Newport Centurions Home Kit - Black striped korfball uniform" loading="lazy" itemprop="image">
      </div>
      <h3>Home Kit</h3>
      <p>Our classic black kit with proud Newport Centurions branding, representing professionalism and tradition</p>
    </div>

    <div class="kit-card" role="article" aria-label="Away Kit">
      <div class="kit-image">
        <img src="/assets/images/team/away-kit.jpg" alt="Newport Centurions Away Kit - Orange striped korfball uniform" loading="lazy" itemprop="image">
      </div>
      <h3>Away Kit</h3>
      <p>Our vibrant orange away kit representing the team's energy, passion, and dynamic spirit on the court</p>
    </div>

  </div>
</section>

  <div class="related-pages">
    <h2>Explore</h2>
    <div class="related-links">
      <a href="/join-us/">Join the Club</a>
      <a href="/about/">About Us</a>
      <a href="/contact/">Contact Us</a>
    </div>
  </div>

<!-- Structured Data for AI Search Engines -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://newportcenturions.co.uk#sponsorship",
  "name": "Newport Centurions Korfball Club Sponsorship Program",
  "url": "https://newportcenturions.co.uk/sponsors/",
  "description": "Official sponsorship program for Newport Centurions Korfball Club - South Wales' premier mixed-gender korfball team",
  "image": "https://newportcenturions.co.uk/assets/images/sponsors/hazlewoods-logo.png",
  "mainEntity": {
    "@type": "SportsTeam",
    "name": "Newport Centurions Korfball Club",
    "url": "https://newportcenturions.co.uk",
    "sport": "Korfball",
    "location": {
      "@type": "Place",
      "name": "Newport, Wales"
    }
  },
  "areaServed": {
    "@type": "Place",
    "name": "South Wales"
  },
  "parentOrganization": {
    "@type": "Organization",
    "@id": "https://newportcenturions.co.uk#organization",
    "name": "Newport Centurions Korfball Club"
  },
  "sponsor": {
    "@type": "Organization",
    "name": "Hazlewoods",
    "url": "https://hazlewoods.co.uk",
    "description": "Official Partner",
    "image": "https://newportcenturions.co.uk/assets/images/sponsors/hazlewoods-logo.png"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "Sponsorship Inquiries",
    "email": "sponsors@newportcenturions.co.uk",
    "availableLanguage": "English"
  },
  "sameAs": [
    "https://facebook.com/newportcenturions",
    "https://twitter.com/newportkorfball",
    "https://instagram.com/newportkorfball"
  ]
}
</script>

<!-- Breadcrumb Schema for AI Navigation -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://newportcenturions.co.uk"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Sponsors",
      "item": "https://newportcenturions.co.uk/sponsors/"
    }
  ]
}
</script>

<!-- FAQ Schema for AI Search Engines -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How can my business sponsor Newport Centurions Korfball Club?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We offer various sponsorship packages tailored to your business goals. Our official partnership program includes brand visibility, community engagement, and sports event opportunities. Contact us at sponsors@newportcenturions.co.uk for detailed sponsorship options."
      }
    },
    {
      "@type": "Question",
      "name": "What is korfball?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Korfball is a mixed-gender team sport originating from the Netherlands. It combines elements of basketball and netball and is played on court by teams of four men and four women. Newport Centurions is a competitive korfball club based in Wales."
      }
    },
    {
      "@type": "Question",
      "name": "Why sponsor Newport Centurions?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sponsoring Newport Centurions provides excellent community visibility, association with grassroots sports excellence, and opportunities to connect with diverse audiences across South Wales. Our partners gain brand recognition through team events, social media, and match day activities."
      }
    },
    {
      "@type": "Question",
      "name": "What benefits do sponsors receive?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sponsorship benefits include logo placement on team jerseys and website, social media promotion, event invitations, match day presence, and brand association with a professional sports team. Custom packages available based on partnership level."
      }
    }
  ]
}
</script>

  </div>
</div>
