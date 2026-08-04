from fastapi import FastAPI

app = FastAPI(title="Maret Tracker API")

@app.get("/health")
def health():
    return {"status" : "ok"}