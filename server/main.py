from fastapi import FastAPI
from config import settings
app = FastAPI(title="ThreatGuard AI")


@app.get("/")
def home():
    return {"message": "ThreatGuard AI API is running"}

print("Configuration loaded:", bool(settings.DATABASE_URL))