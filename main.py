import httpx
from fastapi import FastAPI , HTTPException
from scraper import fetch_raw, extract_jobs
from db import init_db, save_jobs, load_jobs, load_job, prune_stale

from pydantic import BaseModel

class Job(BaseModel):
    id: str
    title: str
    company: str | None = None
    category: str | None = None 
    location: str | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    type: str | None = None
    url: str | None = None
    posted_at: str | None = None


app = FastAPI(title="Market Tracker API")

init_db()

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

@app.get("/jobs" , response_model = list[Job])
def get_jobs(search: str | None = None , min_salary: int | None = None, limit: int = 50):
    return load_jobs(search,min_salary, limit)

@app.get("/jobs/{job_id}" , response_model=Job)
def get_job(job_id : str): 
    job = load_job(job_id)                               # str not int because ReemoteJobs.org uses UUIDs like eced844d-7f....
    if job is None:
        raise HTTPException(status_code=404, detail = "job not found")
    return job

@app.post("/refresh")
def refresh():
    try:
        jobs = extract_jobs(fetch_raw())
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502, detail=f"Upstream source unavailable: {e}"
        )
    count = save_jobs(jobs)
    removed = prune_stale
    return {"saved" : count, "pruned": removed}