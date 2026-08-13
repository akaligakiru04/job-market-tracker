# Backlog — after Day 9

Ideas deferred during the sprint. Not commitments.

- [ ] Automated tests (pytest + FastAPI TestClient) — good standalone
      week-3 project; "added tests to an existing codebase" is a
      stronger story than tests written from the start
- [ ] Second data source (WeWorkRemotely RSS) + normalise into one
      schema — demonstrates real data-engineering work
- [ ] Scheduled refresh via external cron pinging /refresh
- [ ] Salary distribution stats endpoint
- [ ] POST /refresh is currently public. Anyone who reads /docs page can trigger a scrape, repeatedly. The standard fix is a secret token — the caller passes a header, the endpoint checks it against an environment variable, and rejects anything else with 401.