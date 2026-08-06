import httpx

API_URL = "https://remotejobs.org/api/v1/jobs"
HEADERS = {"User-Agent": "job-market-tracker/0.1"}


def fetch_raw(category="programming", limit=50):
    params = {"category": category, "limit": limit}
    resp = httpx.get(API_URL, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.json()["data"]


def extract_jobs(raw):
    jobs = []
    for item in raw:
        company = item.get("company") or {}
        category = item.get("category") or {}
        jobs.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "company": company.get("name"),
            "category": category.get("slug"),
            "location": item.get("location") or "Remote",
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "type": item.get("type"),
            "url": item.get("apply_url"),
            "posted_at": item.get("posted_at"),
        })
    return jobs


if __name__ == "__main__":
    jobs = extract_jobs(fetch_raw())
    print(f"{len(jobs)} jobs")
    for job in jobs[:5]:
        print(f"- {job['title']} @ {job['company']} | {job['salary_min']}")