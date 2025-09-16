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


## Quick Start
```bash
# from repo root
docker compose up -d --build
# open http://localhost:8080

## Scaling (demo)
Remove/empty the ports: block under web before scaling to avoid port conflicts.

