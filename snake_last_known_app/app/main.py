from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import sightings

app = FastAPI(title="Last Known Snakes API", version="1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

Base.metadata.create_all(bind=engine)

app.include_router(sightings.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
