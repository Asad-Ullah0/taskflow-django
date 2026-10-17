# Stage 1
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y gcc pkg-config default-libmysqlclient-dev

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt

# Stage 2
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libmariadb3

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/ .

RUN mkdir -p accounts tasks/migrations && touch config/__init__.py accounts/__init__.py tasks/__init__.py tasks/migrations/__init__.py
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
