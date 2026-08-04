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

*Note: hosted on Render's free tier - the first request after inactivity takes 30-60s to wake the server.*