# TaskFlow

![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?logo=mysql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-1.27-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

A multi-user task manager built with Django and MySQL, containerised with Docker and served through an Nginx reverse proxy.

## Architecture

```text
Browser ──► Nginx :80 ──► Django + Gunicorn :8000 ──► MySQL :3306
```

Only Nginx is public. Django and MySQL run on a private Docker network. Database data is kept in a named volume, and Django starts only after the MySQL health check passes.

## Quick Start

```bash
git clone https://github.com/Asad-Ullah0/taskflow-django.git
cd taskflow-django
cp .env.example .env     # set your own secret key and passwords
docker compose up -d --build
```

Open http://localhost. Create an admin user with:

```bash
docker compose exec web python manage.py createsuperuser
```

## Configuration

Set these in `.env` (never commit it):

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Required when `DJANGO_DEBUG=0` |
| `DJANGO_ALLOWED_HOSTS` | `*` allows any host (fine for testing). In production, use your domain or server IP |
| `CSRF_TRUSTED_ORIGINS` | e.g. `http://YOUR_SERVER_IP` |
| `MYSQL_*` / `DB_*` | Database credentials (must match) |

## Operations

```bash
docker compose ps            # status
docker compose logs -f web   # logs
docker compose down          # stop (data kept)
docker compose down -v       # stop and delete database
```

## Deploy on AWS EC2

Install Docker, clone the repo, create `.env`, open port 80 in the Security Group, then run `docker compose up -d --build`.

---

Built by [Asad Ullah](https://github.com/Asad-Ullah0)
