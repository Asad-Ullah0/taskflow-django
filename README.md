# TaskFlow

![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?logo=mysql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-1.27-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

A multi-user task manager built with Django and MySQL, containerised with Docker and served through an Nginx reverse proxy.

## Features

- Register, log in and log out
- Create, edit, delete and complete tasks without page reloads
- Priorities, due dates and overdue highlighting
- Search, status filters and sorting
- Live dashboard statistics
- Every user sees only their own tasks
- Django admin panel

## Architecture

```text
Browser ──► Nginx :80 ──► Django + Gunicorn :8000 ──► MySQL :3306
```

Only Nginx is public. Django and MySQL run on a private Docker network.

## DevOps Highlights

| Practice | Benefit |
|---|---|
| Multi-stage Dockerfile | Build tools stay out of the final image |
| Nginx reverse proxy | Single public entry point |
| MySQL health check | Django starts only when the database is ready |
| Named volume | Database survives restarts and rebuilds |
| `.env` configuration | Secrets stay out of code and Git |
| Restart policy | Containers recover after a crash or reboot |

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

Admin panel: http://localhost/admin

## Configuration

Set these in `.env` (never commit it):

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Required when `DJANGO_DEBUG=0` |
| `DJANGO_DEBUG` | `0` for production, `1` for development |
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

1. Install Docker and clone the repo.
2. Create `.env` from `.env.example` and set production values.
3. Open port 80 in the Security Group.
4. Run `docker compose up -d --build`.

## Security Notes

- Never upload `.env` to GitHub.
- Keep `DJANGO_DEBUG=0` in production.
- Use a strong `DJANGO_SECRET_KEY` and database password.
- Replace `DJANGO_ALLOWED_HOSTS=*` with your own domain or IP in production.

## Project Structure

```text
app/          Django project (config, accounts, tasks, templates, static)
nginx/        Nginx configuration
Dockerfile    Multi-stage build
docker-compose.yml
.env.example
```

---

Built by [Asad Ullah](https://github.com/Asad-Ullah0)
