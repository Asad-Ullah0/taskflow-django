# TaskFlow

![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?logo=mysql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-reverse%20proxy-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

A multi-user task manager built with Django and MySQL, fully containerised with Docker and served through an Nginx reverse proxy.

The focus of this project is not only the application code but also **how it is packaged, connected and deployed**: a multi-stage Dockerfile, a three-container Docker Compose setup, a reverse proxy, health checks and persistent storage.

## Architecture

```
Browser  ──►  Nginx (port 80)  ──►  Django + Gunicorn (port 8000)  ──►  MySQL (port 3306)
              reverse proxy         application tier                    data tier
```

A classic three-tier design. Only Nginx is published to the outside world. Django and MySQL live on a private Docker network and cannot be reached directly from the internet.

## Features

- Register, login and logout
- Create, edit, delete and complete tasks without page reloads
- Priorities, due dates and overdue highlighting
- Search, status filters and sorting
- Live progress stats on the dashboard
- Every user sees only their own tasks
- Django admin panel

## DevOps highlights

| What | Why it matters |
|---|---|
| Multi-stage Dockerfile | Compilers stay in the build stage, so the final image is smaller and cleaner |
| Nginx reverse proxy | One public entry point, Django and the database are never exposed |
| Docker Compose | Nginx, Django and MySQL start together with a single command |
| MySQL health check | Django starts only after the database is truly ready, so there are no start-up crashes |
| Custom Docker network | Containers reach each other by service name (`db`, `web`) on a private network |
| Named volume | Database data survives container restarts and rebuilds |
| `.env` configuration | Secrets stay out of the code and out of Git, `.env.example` is the template |
| Automated start-up | Migrations and static files are handled on every start, and containers restart automatically after a crash or reboot |

## Run it

**1. Clone the project and create your `.env` file**

```bash
git clone https://github.com/Asad-Ullah0/django-app.git
cd django-app
cp .env.example .env
```

**2. Edit `.env` and set your own values**

`.env.example` is only a template, so open the new file (`nano .env`) and edit the environment variables to your own values, for example your own `DJANGO_SECRET_KEY` (any long random string), database name and database password.

**3. Start the app**

```bash
docker compose up -d --build
```

Open http://localhost and you are done.

## Create an admin user

```bash
docker compose exec web python manage.py createsuperuser
```

Then open http://localhost/admin

## Deploying on a server (AWS EC2)

Add your server IP or domain to `.env`, otherwise login and register will fail with a 403 error:

```
DJANGO_ALLOWED_HOSTS=localhost,YOUR_SERVER_IP
CSRF_TRUSTED_ORIGINS=http://YOUR_SERVER_IP
```

Allow inbound **HTTP (port 80)** in the security group, then apply the change:

```bash
docker compose up -d --force-recreate
```

## Useful commands

```bash
docker compose ps             # container status
docker compose logs -f web    # Django logs
docker compose down           # stop
docker compose down -v        # stop and delete the database
```

## Security notes

- Never upload your `.env` file to GitHub.
- Keep `DJANGO_DEBUG=0` in production.
- Use a strong `DJANGO_SECRET_KEY` and database password.

---

Built by [Asad Ullah](https://github.com/Asad-Ullah0)
