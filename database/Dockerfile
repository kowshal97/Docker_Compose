FROM postgres:16-alpine

ENV POSTGRES_DB=appdb \
    POSTGRES_USER=appuser \
    POSTGRES_PASSWORD=apppass

# expects the file at: my_project/database/init.sql
COPY database/init.sql /docker-entrypoint-initdb.d/01_init.sql

EXPOSE 5432
