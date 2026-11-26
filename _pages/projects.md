---
layout: default
title: projects
permalink: /projects/
description: Liquid-metal materials, wearable instruments, and software I have built or contributed to.
nav: true
nav_order: 3
featured_project: /projects/2_project/
groups:
  - { category: research, title: Materials and electrodes }
  - { category: engineering, title: Instruments and circuits }
  - { category: coursework, title: Coursework }
  - { category: interests, title: Research concepts }
---

<div class="project-index">
  <header class="project-index-header">
    <h1>Projects</h1>
    <a href="https://github.com/charleskim990819">GitHub <span aria-hidden="true">↗</span></a>
  </header>

{% assign featured = site.projects | where: 'url', page.featured_project | first %}

  <section class="project-spotlight" aria-labelledby="spotlight-title">
    <figure>
      <img src="{{ '/assets/img/mrs-led-twisted-strip.webp' | relative_url }}" width="1200" height="673" alt="Two gloved hands twist a flexible strip with a green LED glowing at the center.">
      <figcaption>In a separate test, one LED stays lit as the strip twists. Photo from my MRS presentation.</figcaption>
    </figure>
    <div class="project-spotlight-copy">
      <h2 id="spotlight-title">Four LEDs light up on the back of a hand</h2>
      <p>I printed the circuit with liquid metal ink and transferred it onto skin using a water-soluble film. A coin cell supplied the power.</p>
      <a class="project-detail-link" href="{{ featured.url | relative_url }}">See the water-transfer project <span aria-hidden="true">→</span></a>
    </div>
  </section>

{% for group in page.groups %}
{% assign entries = site.projects | where: 'category', group.category | sort: 'importance' %}

<section class="project-group" aria-labelledby="{{ group.category }}">
<h2 id="{{ group.category }}">{{ group.title }}</h2>
<ul>
{% for project in entries %}
{% unless project.url == featured.url %}
<li>
<a class="project-entry" href="{{ project.url | relative_url }}">
<h3>{{ project.title | escape }}</h3>
<p>{{ project.description | escape }}</p>
<span aria-hidden="true">→</span>
</a>
</li>
{% endunless %}
{% endfor %}
</ul>
</section>
{% endfor %}

<a id="code-repositories" class="project-source" href="https://github.com/charleskim990819/charleskim990819.github.io">Website source <span aria-hidden="true">↗</span></a>

</div>
