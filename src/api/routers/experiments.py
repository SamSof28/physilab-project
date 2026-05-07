from fastapi import APIRouter, Depends, HTTPException
from src.schemas.mru import MRUSchema
from src.schemas.mrua import MRUASchema
from src.services.physics_service import PhysicsService
from src.api.dependencies import get_physics_service # Lo que rescatamos del profe

router = APIRouter()

@router.post("/calculate/mru")
def calculate_mru(
    nombre: str, 
    datos: MRUSchema, 
    service: PhysicsService = Depends(get_physics_service)
):
    """Calcula y guarda un ensayo de MRU."""
    try:
        # El router no sabe de física, solo le pasa el trabajo al Service
        return service.resolver_y_guardar_mru(nombre, datos)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/calculate/mrua")
def calculate_mrua(
    nombre: str, 
    datos: MRUASchema, 
    service: PhysicsService = Depends(get_physics_service)
):
    """Calcula y guarda un ensayo de MRUA."""
    try:
        return service.resolver_y_guardar_mrua(nombre, datos)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))