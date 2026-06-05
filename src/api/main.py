from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api.routers import experiments
from src.core.config import settings
from src.core.exceptions import (
    AppError,
    DuplicateError,
    NotFoundError,
    StorageError,
    ValidationError,
)

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Backend modular de procesamiento físico y cinemático para PhysiLab",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(experiments.router, prefix="/experiments", tags=["Experiments CRUD"])


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    status_code = 500

    if isinstance(exc, NotFoundError):
        status_code = 404
    elif isinstance(exc, DuplicateError):
        status_code = 409
    elif isinstance(exc, ValidationError):
        status_code = 422
    elif isinstance(exc, StorageError):
        status_code = 502

    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message, "error": exc.__class__.__name__},
    )


@app.get("/", tags=["Root"])
def read_root():
    return {"status": "online", "message": "Bienvenido a la API de PhysiLab"}
