from fastapi import FastAPI
from scraper import fetch_raw, extract_jobs

app = FastAPI(title="Market Tracker API")

@app.get("/")
def root():
    return {
        "service" : "Market tracker API",
        "status" : "under construction",
        "docs" : "/docs"
    }

@app.get("/health")
def health():
    return {"status" : "ok"}

@app.get("/jobs")
def get_jobs(search: str | None = None):
    jobs = extract_jobs(fetch_raw())
    if search:
        jobs = [j for j in jobs if search.lower() in (j["title"] or "").lower()]
    return jobs