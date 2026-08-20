---
layout: page
title: projects
permalink: /projects/
description: Ongoing research and engineering projects in liquid-metal electronics, wearable bioelectronics, and electrochemical biosensing.
nav: true
nav_order: 3
display_categories: [research, engineering, interests]
horizontal: false
---

<!-- pages/projects.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>

<h2 id="code-repositories" class="category" style="margin-top:3rem;">code &amp; repositories</h2>

<p>
  All open-source code, hardware files, and project repositories live on GitHub. Browse the active repositories below or visit the full profile.
</p>

<p class="text-center my-4">
  <a class="btn btn-primary btn-lg" href="https://github.com/charleskim990819" target="_blank" rel="noopener">
    <i class="fab fa-github"></i>&nbsp; View all repositories on GitHub &rarr;
  </a>
</p>

<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">
  <div class="col">
    <div class="card h-100 shadow-sm border-0">
      <div class="card-body">
        <h5 class="card-title mb-2">
          <i class="fab fa-github text-muted"></i>&nbsp;
          <a href="https://github.com/charleskim990819/Biopotential-EXG-sPCB" target="_blank" rel="noopener">Biopotential-EXG-sPCB</a>
        </h5>
        <p class="card-text">
          Stretchable PCB reconstruction of the BioAmp EXG Pill biopotential front-end, with liquid-metal printing and AutoCAD mask design for the soft-PCB form factor.
        </p>
        <p class="text-muted small mb-0">
          <span class="badge bg-light text-dark">Hardware</span>
          <span class="badge bg-light text-dark">KiCad</span>
          <span class="badge bg-light text-dark">sPCB</span>
        </p>
      </div>
    </div>
  </div>

  <div class="col">
    <div class="card h-100 shadow-sm border-0">
      <div class="card-body">
        <h5 class="card-title mb-2">
          <i class="fab fa-github text-muted"></i>&nbsp;
          <a href="https://github.com/charleskim990819/charleskim990819.github.io" target="_blank" rel="noopener">charleskim990819.github.io</a>
        </h5>
        <p class="card-text">
          Source code for this academic homepage. Built on Jekyll with the al-folio theme, deployed via GitHub Pages and Cloudflare DNS.
        </p>
        <p class="text-muted small mb-0">
          <span class="badge bg-light text-dark">Jekyll</span>
          <span class="badge bg-light text-dark">HTML / SCSS</span>
          <span class="badge bg-light text-dark">YAML</span>
        </p>
      </div>
    </div>
  </div>
</div>
