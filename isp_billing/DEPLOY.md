# Deployment Guide

This guide explains how to deploy the **isp_billing** Django application to [Render](https://render.com) and obtain a public URL.

## Project layout

```
isp_billing/          ← root directory for deployment
├── manage.py
├── requirements.txt
├── Procfile
├── isp_billing/
│   ├── settings.py
│   ├── wsgi.py
│   └── urls.py
└── billing_app/
```

## Quick deploy with Render Blueprint

The repository already contains a `render.yaml` at the repo root that provisions:

- A **web service** running gunicorn
- A **PostgreSQL database** (free plan)

Steps:

1. Fork or push this repository to your GitHub account.
2. Go to <https://dashboard.render.com/> → **New** → **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect `render.yaml` and pre-fill all settings. Click **Apply**.
5. Wait for the build to finish — your public URL will appear as `https://<service-name>.onrender.com`.

## Manual deploy on Render

If you prefer to configure the service manually:

| Setting | Value |
|---|---|
| **Root Directory** | `isp_billing` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn isp_billing.wsgi:application` |

## Required environment variables

| Variable | Description | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Long random secret key | `generate` on Render |
| `DEBUG` | Enable debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | `.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | `https://*.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection string | set by Render database |

## Local development

```bash
cd isp_billing
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Verify gunicorn locally

```bash
cd isp_billing
gunicorn isp_billing.wsgi:application
```

## Collect static files (CI / build step)

```bash
cd isp_billing
python manage.py collectstatic --noinput
```

Static files are served by [WhiteNoise](https://whitenoise.readthedocs.io/) — no separate static file hosting required.
