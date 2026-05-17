# Importaremos tu servicio de física cuando lo creemos
from src.services.physics_service import PhysicsService

def get_physics_service() -> PhysicsService:
    """Provee la lógica de negocio de PhysiLab lista para usar."""
    return PhysicsService()