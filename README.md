# Old North Dayton Asset Map

A neighborhood asset mapping application built with Django and Leaflet. Residents can discover and contribute local resources — community organizations, green spaces, small businesses, and neighbors with skills to share.

## Features

- **Map view** — interactive Leaflet map with category-colored markers, clustering, and a sidebar filter/search
- **Directory view** — searchable, filterable card grid of all assets
- **Asset detail pages** — full info with a mini-map inset
- **Public submission form** — click-to-place pin on a map, goes to a moderation queue
- **Admin moderation** — approve, reject, or archive submissions; bulk actions; verified badge

## Local Development

**Requirements:** Python 3.9+

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data       # loads 15 Old North Dayton demo assets
python manage.py createsuperuser # for admin access at /admin/
python manage.py runserver
```

Visit `http://localhost:8000`

## Deployment (Railway)

The app is Railway-ready via `railway.toml`. It uses Nixpacks for building.

**Services needed:**
- Web service (this repo)
- PostgreSQL plugin (Railway injects `DATABASE_URL` automatically)

**Environment variables to set:**

| Variable | Value |
|---|---|
| `SECRET_KEY` | a long random string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.up.railway.app` |

The deploy command (in `railway.toml`) runs `collectstatic`, `migrate`, and `seed_data` automatically on each deploy. Seed data uses `update_or_create` so re-runs are safe.

**Create a superuser** from the Railway shell:
```bash
/opt/venv/bin/python manage.py createsuperuser
```

## Asset Categories

| Category | Description |
|---|---|
| Community Orgs & Nonprofits | Neighborhood associations, food pantries, mutual aid, faith communities |
| Green Space & Parks | Parks, community gardens, trails, urban farms |
| Small Businesses | Local shops, restaurants, and services |
| Skills & People | Neighbors offering skills or knowledge to the community |

## Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** PostgreSQL (production), SQLite (local dev)
- **Maps:** Leaflet.js + MarkerCluster
- **Styles:** Bootstrap 5
- **Static files:** WhiteNoise
- **Hosting:** Railway
