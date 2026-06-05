from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from typing import List
from src.schemas.experiment import ExperimentResponse
from src.schemas.mru import MRUSchema
from src.schemas.mrua import MRUASchema
from src.services.physics_service import PhysicsService
from src.api.dependencies import get_physics_service

router = APIRouter()


@router.post("/calculate/mru", status_code=status.HTTP_201_CREATED)
def calculate_mru(
    nombre: str = Query(..., min_length=3, max_length=100),
    datos: MRUSchema = Body(...),
    service: PhysicsService = Depends(get_physics_service),
):
    """Calcula y guarda un ensayo de MRU."""
    return service.resolver_y_guardar_mru(nombre, datos)


@router.post("/calculate/mrua", status_code=status.HTTP_201_CREATED)
def calculate_mrua(
    nombre: str = Query(..., min_length=3, max_length=100),
    datos: MRUASchema = Body(...),
    service: PhysicsService = Depends(get_physics_service),
):
    """Calcula y guarda un ensayo de MRUA."""
    return service.resolver_y_guardar_mrua(nombre, datos)


@router.get("", response_model=List[ExperimentResponse])
def get_all_experiments(service: PhysicsService = Depends(get_physics_service)):
    """Obtiene el listado maestro de todos los experimentos realizados."""
    return service.list_all()


@router.get("/{id}")
def get_experiment_detail(
    id: int, service: PhysicsService = Depends(get_physics_service)
):
    """Obtiene un experimento específico junto con su desglose de variables físicas."""
    exp = service.get_one(id)
    if not exp:
        raise HTTPException(
            status_code=404, detail=f"El experimento con ID {id} no existe."
        )
    return exp


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_experiment(id: int, service: PhysicsService = Depends(get_physics_service)):
    """Elimina un experimento de la base de datos (Borrado en cascada automatizado)."""
    eliminado = service.remove_one(id)
    if not eliminado:
        raise HTTPException(
            status_code=404, detail=f"No se encontró el experimento {id} para eliminar."
        )
    return {"message": f"Experimento {id} eliminado exitosamente."}


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_experiment_name(
    id: int,
    nuevo_nombre: str = Query(..., min_length=3, max_length=100),
    service: PhysicsService = Depends(get_physics_service),
):
    """Actualiza el nombre identificativo de un experimento existente."""
    actualizado = service.update_experiment_title(id, nuevo_nombre)
    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontro el experimento con id: {id} para actualizar.",
        )

    return {
        "message": f"Experimento {id} actualizado correctamente a '{nuevo_nombre}'."
    }
