import sqlite3

DB_PATH = "jobs.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute(""" 
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
                posted_at TEXT
            )
            """)

def save_jobs(jobs):
    with get_conn() as conn:
        for job in jobs:
            conn.execute("""
                INSERT OR REPLACE INTO jobs ( id, title, company, category, 
                location, min_salary, max_salary, type, url, posted_at) 
                VALUES (?,?,?,?,?,?,?,?,?,?)""", (
                    job["id"], job["title"], job["company"],
                    job["category"],job["location"],job["min_salary"],job["max_salary"]
                    ,job["type"],job["url"],job["posted_at"]
                ))
    return len(jobs)

def load_jobs(search=None, min_salary=None, limit=50):
    sql = "SELECT * FROM jobs"
    conditions = []
    values = []

    if search:
        conditions.append("title LIKE ?")
        values.append(f"%{search}%")

    if min_salary is not None:
        conditions.append("min_salary >= ?")
        values.append(min_salary)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY posted_at DESC LIMIT ?"
    values.append(limit)

    with get_conn() as conn:
        rows = conn.execute(sql,values).fetchall()

    return [dict(r) for r in rows]

def load_job(job_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?",
         (job_id,)).fetchone()

    return dict(row) if row else None

if __name__ == "__main__":
    from scraper import fetch_raw, extract_jobs

    init_db()
    n = save_jobs(extract_jobs(fetch_raw()))
    print(f"saved {n} jobs")

    print("all:" , len(load_jobs()))
    print("search = engineer:" ,len(load_jobs(search="engineer")))
    print("min_salary = 50000", len(load_jobs(min_salary = 50000)))
    print("both ", len(load_jobs(search= "engineer", min_salary=50000)))