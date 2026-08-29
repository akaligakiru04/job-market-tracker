#Market Tracker API

A FastAPI service that scrapes remote job listings on demand, stores them in PostgreSQL, and exposes them via REST API with a simple web dashboard

**Live** https://job-market-tracker-0m51.onrender.com/
**Docs** https://job-market-tracker-0m51.onrender.com/docs

In active development.

#Stack
- Python / FastAPI
- PostgreSQL
- BeautifulSoup + httpx
- Deployed on Render

##Status
- [x] API skeleton deployed
- [ ] Scraper
- [ ] Database layer
- [ ] Filtering endpoints
- [ ] Dashboard front page

*Notes:*
-hosted on Render's free tier - the first request after inactivity takes 30-60s to wake the server.
-filtering by minimum salary excludes jobs with unknown salary so ?min_salary=50000 will drop most listings.
- upstream failures return 502 rather than a generic error, and cached results remain available
- POST /refresh is currently public. Anyone who reads /docs page can trigger a scrape, repeatedly. Eventual fix is a secret token, the caller passes a header, the endpoint checks it against an environment variable, and rejects anything else with 401.
- stale listings are to be pruned via a last_seen timestamp rather than a destructive reload, meaning a failed scrape never empties the database. (after postgre migration)
- first database query after idle takes a few extra seconds to wake up just like Render.
