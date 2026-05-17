from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import experiments
from src.core.config import settings

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Backend modular de procesamiento físico y cinemático para PhysiLab"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(experiments.router, prefix="/experiments", tags=["Experiments CRUD"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "online", "message": "Bienvenido a la API de PhysiLab"}