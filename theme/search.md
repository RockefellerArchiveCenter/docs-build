---
layout: default
title: Search Results
permalink: /search/
---

<div class="container">
  <div class="row">
    <div class="col-sm-8">
    {% capture doc-name %}{{ doc.slug }}{% endcapture %}
    {% include search-doc.html content=doc-name %}
    </div>
  </div>
</div>

<div class="container">
  <div class="row">
    <div class="col">
      <div id="results"></div>
    </div>
  </div>
</div>
