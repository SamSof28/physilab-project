import pytest
from unittest.mock import MagicMock
from src.mi_app.services import LaboratoryService
from src.mi_app.models.mru import UniformRectilinearMotion
from src.mi_app.exceptions import (
    NegativeValueError,
    InsufficientDataError,
    PhysicsDivisionByZeroError,
    DuplicateIdError,
    ExperimentNotFoundError,
)

# --- FIXTURES ---
@pytest.fixture
def service_mock() -> LaboratoryService:
    """Crea una instancia del servicio con un storage simulado."""
    mock_storage = MagicMock()
    mock_storage.load.return_value = [] # Simula base de datos vacía
    return LaboratoryService(mock_storage)

# --- TESTS DE MRU ---

def test_mru_distance_calculation(service_mock) -> None:
    """Prueba el cálculo básico: V * T = D."""
    experiment = UniformRectilinearMotion(
        id=1, name="Prueba", experiment_type="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=5, distancia=None
    )
    service_mock.calculate_mru(experiment)
    assert experiment.distancia == 50

def test_mru_time_resolution(service_mock) -> None:
    """Prueba el despeje: T = D / V."""
    experiment = UniformRectilinearMotion(
        id=2, name="Despeje T", experiment_type="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=None, distancia=100
    )
    service_mock.calculate_mru(experiment)
    assert experiment.tiempo == 10

def test_mru_speed_resolution(service_mock) -> None:
    """Prueba el despeje: V = D / T."""
    experiment = UniformRectilinearMotion(
        id=2, name="Despeje V", experiment_type="Movimiento Rectilineo Uniforme",
        velocidad=None, tiempo=5 , distancia=100
    )
    service_mock.calculate_mru(experiment)
    assert experiment.velocidad == 20

def test_negative_speed_raises_error(service_mock) -> None:
    """Prueba que se lance DatoNegativoError al ingresar una velocidad negativa."""
    with pytest.raises(NegativeValueError):
        UniformRectilinearMotion(
            id=99,
            name="Prueba Error",
            experiment_type="Movimiento Rectilineo Uniforme",
            velocidad=-10,
            tiempo=5,
            distancia=None,
        )

def test_mru_insufficient_data_error(service_mock) -> None:
    """Prueba que falle si faltan 2 o más datos."""
    experiment = UniformRectilinearMotion(
        id=3, name="Incompleto", experiment_type="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=None, distancia=None # Faltan 2 datos
    )
    with pytest.raises(InsufficientDataError):
        service_mock.calculate_mru(experiment)

def test_division_by_zero_error(service_mock) -> None:
    """Prueba que falla si V = 0 para calcular el tiempo T"""
    experiment = UniformRectilinearMotion(
        id=3, name="Prueba Cero", experiment_type="Movimiento Rectilineo Uniforme", 
        velocidad=0, tiempo=None, distancia=20 
    )

    with pytest.raises(PhysicsDivisionByZeroError):
        service_mock.calculate_mru(experiment)

def test_empty_storage_load(service_mock) -> None:
    """"""
    service_mock.storage.load.return_value = []

    experiment = UniformRectilinearMotion(
        id=101, 
        name="Primer Ensayo", 
        experiment_type="Movimiento Rectilineo Uniforme",
        velocidad=10.0, 
        tiempo=2.0, 
        distancia=None
    )
    
    service_mock.calculate_mru(experiment)

    assert experiment.distancia == 20.0 

def test_duplicate_id_error(service_mock) -> None:
    """
    Verifica que el servicio lance IdExistente si el ID ya está registrado en el storage.
    """

    existing_experiment = UniformRectilinearMotion(
        id=50, name="Existente", experiment_type="MRU", velocidad=5, tiempo=2, distancia=10
    )
    service_mock.storage.load.return_value = [existing_experiment]

    new_experiment = UniformRectilinearMotion(
        id=50, 
        name="Intruso", 
        experiment_type="Movimiento Rectilineo Uniforme",
        velocidad=10, 
        tiempo=5
    )

    with pytest.raises(DuplicateIdError):
        service_mock.calculate_mru(new_experiment)


def test_delete_experiment_success(service_mock) -> None:
    """
    Verifica que al eliminar un ensayo, se llame al método save del storage.
    """

    experiment = UniformRectilinearMotion(
        id=7, name="Para Borrar", experiment_type="MRU", velocidad=10, tiempo=5, distancia=50
    )
    service_mock.storage.load.return_value = [experiment]

    service_mock.delete_experiment(7)

    service_mock.storage.save.assert_called_once() 

def test_delete_experiment_not_found_error(service_mock) -> None:
    """"""

    service_mock.storage.load.return_value = []

    with pytest.raises(ExperimentNotFoundError):
        service_mock.delete_experiment(999)