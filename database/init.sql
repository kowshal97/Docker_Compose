-- database/init.sql
CREATE TABLE IF NOT EXISTS visits (
  id SERIAL PRIMARY KEY,
  visited_at TIMESTAMPTZ DEFAULT NOW()
);
