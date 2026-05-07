from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import experiments # Importamos tu router
from src.core.config import settings

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version
)

# Configuración de CORS (Permitir que Streamlit hable con FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pondrías la URL de tu Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# "Enchufamos" el router de experimentos
app.include_router(experiments.router, prefix="/experiments", tags=["Physics"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de PhysiLab"}