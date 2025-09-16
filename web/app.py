import os, socket
from flask import Flask, jsonify
import psycopg2, redis

app = Flask(__name__)

# ---- config from env ----
DB_HOST = os.getenv("DB_HOST", "database")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# ---- liveness: used by docker healthcheck ----
@app.route("/live")
def live():
    return "ok", 200

# ---- readiness: verify DB + Redis ----
@app.route("/ready")
def ready():
    try:
        r = get_redis(); r.ping()
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "not-ready", "detail": str(e)}), 503

# ---- app home: shows counts & hostname ----
@app.route("/")
def index():
    hostname = socket.gethostname()
    try:
        r = get_redis()
        visits = r.incr("hits")  # increments on each refresh
    except Exception as e:
        visits = f"redis error: {e}"

    try:
        with get_db_conn() as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS visits (
                        id SERIAL PRIMARY KEY,
                        visited_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                cur.execute("INSERT INTO visits DEFAULT VALUES;")
                cur.execute("SELECT COUNT(*) FROM visits;")
                (row_count,) = cur.fetchone()
    except Exception as e:
        row_count = f"postgres error: {e}"

    return f"""
    <html>
      <head>
        <title>Docker Compose Lab</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 2rem; }}
          .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem; }}
          .pill {{ display:inline-block; padding:.25rem .6rem; border-radius:999px; background:#eee; }}
          code {{ background:#f6f8fa; padding:.2rem .4rem; border-radius:4px; }}
        </style>
      </head>
      <body>
        <h1>✅ Multi-Service App (Web + Postgres + Redis)</h1>
        <div class="card">
          <p><strong>Web container:</strong> <span class="pill">{hostname}</span></p>
          <p><strong>Redis hits:</strong> {visits}</p>
          <p><strong>Postgres rows in <code>visits</code>:</strong> {row_count}</p>
          <p>Health: <a href="/live">/live</a> • <a href="/ready">/ready</a></p>
        </div>
      </body>
    </html>
    """
