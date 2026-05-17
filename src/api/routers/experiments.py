from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.schemas.experiment import ExperimentResponse
from src.schemas.mru import MRUSchema
from src.schemas.mrua import MRUASchema
from src.services.physics_service import PhysicsService
from src.api.dependencies import get_physics_service 

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

@router.get("", response_model=List[ExperimentResponse])
def get_all_experiments(service: PhysicsService = Depends(get_physics_service)):
    """Obtiene el listado maestro de todos los experimentos realizados."""
    return service.list_all()

@router.get("/{id}")
def get_experiment_detail(id: int, service: PhysicsService = Depends(get_physics_service)):
    """Obtiene un experimento específico junto con su desglose de variables físicas."""
    exp = service.get_one(id)
    if not exp:
        raise HTTPException(status_code=404, detail=f"El experimento con ID {id} no existe.")
    return exp

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_experiment(id: int, service: PhysicsService = Depends(get_physics_service)):
    """Elimina un experimento de la base de datos (Borrado en cascada automatizado)."""
    eliminado = service.remove_one(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail=f"No se encontró el experimento {id} para eliminar.")
    return {"message": f"Experimento {id} eliminado exitosamente."}