---
name: project-assetmapping
description: Old North Dayton neighborhood asset mapping app — Django + Leaflet proof of concept
metadata:
  type: project
---

A Django 4.2 + Leaflet web app for mapping community assets in Old North Dayton. Proof of concept, built for a demo meeting.

**Tech stack:** Django 4.2, Django REST Framework, Leaflet.js, MarkerCluster, Bootstrap 5, SQLite, Pillow

**Key URLs:**
- `/` — full-viewport map with sidebar filters
- `/assets/` — searchable/filterable card directory
- `/assets/<id>/` — asset detail with mini-map
- `/submit/` — public crowdsourced submission form (click-to-place pin)
- `/api/assets.geojson` — GeoJSON endpoint consumed by Leaflet
- `/admin/` — Django admin with moderation queue

**Models:** `Category` (name, slug, icon, color) and `Asset` (full metadata, status: pending/active/archived, verified flag)

**Categories:** Community Orgs & Nonprofits (purple), Green Space & Parks (green), Small Businesses (orange), Skills & People (blue)

**Seed data:** 15 demo assets across 4 categories, all set as Old North Dayton

**Admin login:** username `admin`, password `OND-demo-2024!`

**To run:**
```
source env/bin/activate
python manage.py runserver
```

**Why:** Demo for a short meeting. Built-in moderation queue (pending → active/archived) for crowdsourced submissions.
