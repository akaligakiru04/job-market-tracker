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
def get_jobs():
    return extract_jobs(fetch_raw())