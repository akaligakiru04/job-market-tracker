import httpx, json

resp = httpx.get("https://remotejobs.org/api/v1/jobs?category=programming&limit=20")
print("status:", resp.status_code)
data = resp.json()
print("keys:", data.keys())
print(json.dumps(data["data"][0], indent=2))