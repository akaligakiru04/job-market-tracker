from fastapi import FastAPI , HTTPException
from scraper import fetch_raw, extract_jobs

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
    jobs = extract_jobs(fetch_raw())

    if search:
        jobs = [
            j for j in jobs 
            if search.lower() in (j["title"] or "").lower()
        ]

    if min_salary is not None:
        jobs = [
            j for j in jobs
            if j["min_salary"] is not None
            and j["min_salary"] >= min_salary
        ]
    return jobs[:limit]

@app.get("/jobs/{job_id}" , response_model=Job)
def get_job(job_id : str):                                # str not int because ReemoteJobs.org uses UUIDs like eced844d-7f....
    jobs = extract_jobs(fetch_raw())
    for j in jobs:
        if j["id"] == job_id:
            return j
    raise HTTPException(status_code=404 , detail="job not found")   # Fast API returns a proper 404 with a json error body instead of null with a status of 200

