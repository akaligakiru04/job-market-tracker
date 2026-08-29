import os
from datetime import datetime, timedelta, timezone

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
STALE_AFTER_DAYS = 3


def get_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    company TEXT,
                    category TEXT,
                    location TEXT,
                    min_salary INTEGER,
                    max_salary INTEGER,
                    type TEXT,
                    url TEXT,
                    posted_at TEXT,
                    last_seen TIMESTAMPTZ NOT NULL
                )
            """)


def save_jobs(jobs):
    now = datetime.now(timezone.utc)
    with get_conn() as conn:
        with conn.cursor() as cur:
            for job in jobs:
                cur.execute("""
                    INSERT INTO jobs
                    (id, title, company, category, location,
                     min_salary, max_salary, type, url, posted_at, last_seen)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        company = EXCLUDED.company,
                        category = EXCLUDED.category,
                        location = EXCLUDED.location,
                        min_salary = EXCLUDED.min_salary,
                        max_salary = EXCLUDED.max_salary,
                        type = EXCLUDED.type,
                        url = EXCLUDED.url,
                        posted_at = EXCLUDED.posted_at,
                        last_seen = EXCLUDED.last_seen
                """, (
                    job["id"], job["title"], job["company"], job["category"],
                    job["location"], job["min_salary"], job["max_salary"],
                    job["type"], job["url"], job["posted_at"], now,
                ))
    return len(jobs)


def prune_stale():
    cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_AFTER_DAYS)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM jobs WHERE last_seen < %s", (cutoff,))
            return cur.rowcount


def load_jobs(search=None, min_salary=None, limit=50):
    sql = "SELECT * FROM jobs"
    conditions = []
    values = []

    if search:
        conditions.append("title ILIKE %s")
        values.append(f"%{search}%")

    if min_salary is not None:
        conditions.append("min_salary >= %s")
        values.append(min_salary)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY posted_at DESC LIMIT %s"
    values.append(limit)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            return [dict(r) for r in cur.fetchall()]

def count_jobs(search=None, min_salary=None):
    sql = "SELECT COUNT(*) AS total FROM jobs"
    conditions = []
    values = []

    if search:
        conditions.append("title ILIKE %s")
        values.append(f"%{search}%")

    if min_salary is not None:
        conditions.append("min_salary >= %s")
        values.append(min_salary)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            return cur.fetchone()["total"]

def load_job(job_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
            row = cur.fetchone()
    return dict(row) if row else None


if __name__ == "__main__":
    from scraper import fetch_raw, extract_jobs

    init_db()
    n = save_jobs(extract_jobs(fetch_raw()))
    print(f"saved {n} jobs")
    print("pruned:", prune_stale())

    print("all:", len(load_jobs()))
    print("search=engineer:", len(load_jobs(search="engineer")))
    print("min_salary=50000:", len(load_jobs(min_salary=50000)))
    print("both:", len(load_jobs(search="engineer", min_salary=50000)))