# Docker Compose Lab — Web + Postgres + Redis

A minimal multi-service app:
- **web**: Flask + Gunicorn (port 8000 in container)
- **database**: Postgres 16 (init script creates `visits` table)
- **cache**: Redis 7 (AOF on)

## Prereqs
- Docker Desktop (with `docker compose`)

## Project Layout

my_project/
├─ docker-compose.yml
├─ web/
│ ├─ Dockerfile
│ ├─ app.py
│ └─ requirements.txt
├─ database/
│ ├─ Dockerfile
│ └─ init.sql
└─ cache/
└─ Dockerfil
