from fastapi import FastAPI

app = FastAPI(title="Maret Tracker API")

@app.get("/")
def root():
    return {
        "service" : "Market tracker API"
        "status" : "under construction"
        "docs" : "/docs"
    }

@app.get("/health")
def health():
    return {"status" : "ok"}