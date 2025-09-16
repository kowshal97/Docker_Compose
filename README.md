# Docker Compose Lab — Web + Postgres + Redis

A minimal multi-service app:
- **web**: Flask + Gunicorn (port 8000 in container)
- **database**: Postgres 16 (init script creates `visits` table)
- **cache**: Redis 7 (AOF on)

## Prereqs
- Docker Desktop (with `docker compose`)

## Project Layout

<pre>
my_project/
├─ docker-compose.yml
├─ web/
│  ├─ Dockerfile
│  ├─ app.py
│  └─ requirements.txt
├─ database/
│  ├─ Dockerfile
│  └─ init.sql
└─ cache/
   └─ Dockerfile
</pre>



## Quick Start
```bash
# from repo root
docker compose up -d --build
# open http://localhost:8080
```
## Scaling (demo)
Remove/empty the ports: block under web before scaling to avoid port conflicts.
```bash
docker compose up -d --scale web=3 --scale database=2
docker compose ps
```

## Screenshots

**Services healthy (`docker compose ps`)**  
![ps-healthy](screenshots/Screenshot 2025-09-16 093743.png)

**App running (`http://localhost:8080`)**  
![app-home](screenshots/Screenshot 2025-09-16 093656.png)

**Readiness (`/ready`)**  
![ready](screenshots/Screenshot 2025-09-16 094133.png)

**Scaling (`web=3`, `database=2`)**  
![scaling](screenshots/Screenshot 2025-09-16 094538.png)

**Teardown (`docker compose down` then `ps`)**  
![down-empty](screenshots/Screenshot 2025-09-16 093722.png)



