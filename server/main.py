
from contextlib import asynccontextmanager

from fastapi import FastAPI

from server.database import create_tables, engine
from server.controllers.auth_controller import router as auth_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    engine.dispose()


app = FastAPI(
    title="ThreatGuard AI",
    lifespan=lifespan,
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "ThreatGuard AI API is running"}
