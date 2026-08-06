import html
import httpx

API_URL = "https://remoteok.com/api"
HEADERS = {"User-Agent" : "job-market-tracker/0.1"}

def fetch_raw():
    resp = httpx.get(API_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.json()

def extract_jobs(raw):
    jobs=[]
    for item in raw:
        if "position" not in item:
            continue
        jobs.append({
            "id" : item.get("id"),
            "title" : html.unescape(item.get("position", "")),
            "company" : html.unescape(item.get("company")),
            "tags" : item.get("tags", []),
            "location" : item.get("locaion") or "Worldwide",
            "salary_min" : item.get("Salary_min") or None,
            "url" : item.get("url"), 
            "date" : item.get("date"),
        })
    return jobs

if __name__ == "__main__":
    jobs = extract_jobs(fetch_raw())
    jobs = [j for j in jobs if "react" in j["tags"]]
    print(f"{len(jobs)} jobs")
    for job in jobs[:5]:
        print(f" {job['title']} @ {job['company']} | {job['tags'][:3]}")