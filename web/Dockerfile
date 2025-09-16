FROM python:3.11-slim

WORKDIR /app

# System deps for psycopg2 + curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Requirements live in project/web/
COPY web/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App code lives in project/web/
COPY web/app.py /app/app.py

EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
