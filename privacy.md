---
layout: default
title: "Privacy Policy"
description: How Newport Centurions Korfball Club collects, uses and protects your personal data, including our use of cookies and analytics.
permalink: /privacy/
breadcrumb: "Privacy Policy"
robots: "index, follow"
---

<div class="page-content">
  <div class="content-block">

    <h1>Privacy Policy</h1>
    <p class="intro">This policy explains what personal data Newport Centurions Korfball Club collects through this website, why we collect it, and what rights you have. We are a volunteer-run amateur sports club and we keep data collection to the minimum we need.</p>

    <p><strong>Last updated:</strong> {{ site.time | date: "%-d %B %Y" }}</p>

    <h2>Who we are</h2>
    <p>{{ site.data.club.name }} ("we", "us") is an amateur korfball club based at {{ site.data.club.venue.short }}. For the purposes of UK GDPR we are the data controller for information collected via this website.</p>
    <p>You can contact us about anything in this policy at <a href="mailto:{{ site.data.club.email }}">{{ site.data.club.email }}</a>.</p>

    <h2>What we collect</h2>

    <h3>Information you give us</h3>
    <p>If you use our <a href="/contact/">contact form</a>, we collect the name, email address, phone number (optional) and message you provide. We use this solely to reply to your enquiry.</p>
    <p>The form is processed by <a href="https://formsubmit.co" target="_blank" rel="noopener noreferrer nofollow">FormSubmit</a>, which forwards your message to our club email address. Your message passes through their servers in the course of delivery. We do not add you to any mailing list and we do not pass your details to anyone else.</p>
    <p>We keep enquiry emails for as long as needed to deal with your enquiry, and routinely delete them within 12 months.</p>

    <h3>Information collected automatically</h3>
    <p>If — and only if — you consent, we use Google Analytics 4 to understand how the site is used (which pages are popular, roughly where visitors come from). This sets cookies on your device and sends data to Google, including a truncated version of your IP address.</p>
    <p><strong>No analytics cookies are set until you accept them.</strong> If you decline, or ignore the banner, Google Analytics is never loaded.</p>

    <h2>Cookies</h2>
    <table class="privacy-table">
      <thead>
        <tr><th>Cookie</th><th>Purpose</th><th>Set when</th><th>Expires</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><code>nc_consent</code></td>
          <td>Remembers whether you accepted or declined analytics, so we stop asking.</td>
          <td>Always (strictly necessary)</td>
          <td>6 months</td>
        </tr>
        <tr>
          <td><code>_ga</code>, <code>_ga_*</code></td>
          <td>Google Analytics — distinguishes visitors and sessions.</td>
          <td>Only after you accept</td>
          <td>Up to 2 years</td>
        </tr>
      </tbody>
    </table>

    <h3>Changing your mind</h3>
    <p>You can withdraw or grant consent at any time using the button below. Declining also clears any analytics cookies already set.</p>
    <p><button type="button" class="modern-button" data-consent-reopen>Change cookie preferences</button></p>

    <h2>Legal basis</h2>
    <ul>
      <li><strong>Contact form:</strong> legitimate interests — responding to someone who has deliberately contacted us.</li>
      <li><strong>Analytics cookies:</strong> your consent, under the Privacy and Electronic Communications Regulations (PECR) and UK GDPR.</li>
    </ul>

    <h2>Who we share data with</h2>
    <p>We do not sell or trade your data. It is shared only with the service providers that make the site work:</p>
    <ul>
      <li><strong>GitHub Pages</strong> — hosts this website and processes server logs, including IP addresses, for security and delivery.</li>
      <li><strong>FormSubmit</strong> — delivers contact form submissions to our email.</li>
      <li><strong>Google Analytics</strong> — only if you consent.</li>
      <li><strong>Cloudflare (cdnjs)</strong> — serves the icon font used on this site.</li>
    </ul>

    <h2>Embedded content</h2>
    <p>Our <a href="/contact/">contact page</a> has a Google Map and our <a href="/what-is-korfball/">what is korfball</a> page has a YouTube video. Neither loads automatically &mdash; each shows a placeholder until you click it. Nothing is requested from Google or YouTube, and no cookies are set by them, unless you choose to load the embed.</p>
    <p>If you do load one, that provider receives your IP address and may set its own cookies under its own privacy policy. The video uses YouTube's no-cookie domain, which reduces (but does not eliminate) tracking.</p>

    <h2>Young people</h2>
    <p>Our playing membership is open to those aged {{ site.data.club.min_age }} and over. We do not knowingly collect data from children under 13 through this website. If you believe a child has sent us their details, contact us and we will delete them.</p>

    <h2>Your rights</h2>
    <p>Under UK GDPR you have the right to access, correct, delete or restrict the processing of your personal data, to object to processing, and to data portability. To exercise any of these, email <a href="mailto:{{ site.data.club.email }}">{{ site.data.club.email }}</a>.</p>
    <p>If you are unhappy with how we have handled your data, you can complain to the Information Commissioner's Office at <a href="https://ico.org.uk" target="_blank" rel="noopener noreferrer">ico.org.uk</a> or on 0303 123 1113.</p>

    <h2>Changes to this policy</h2>
    <p>If we change how we handle data we will update this page and the "last updated" date above.</p>

  </div>
</div>
