import pytest
from unittest.mock import MagicMock
from src.mi_app.services import LaboratorioService
from src.mi_app.models import MovimientoRectilineoUniforme
from src.mi_app.exceptions import (
    DatoNegativoError,
    DatosInsuficientesError,
    DivisionPorCeroFisicaError,
    IdExistente,
    ExperimentoNoExistenteError
)

# --- FIXTURES ---
@pytest.fixture
def service_mock() -> LaboratorioService:
    """Crea una instancia del servicio con un storage simulado."""
    mock_storage = MagicMock()
    mock_storage.load.return_value = [] # Simula base de datos vacía
    return LaboratorioService(mock_storage)

# --- TESTS DE MRU ---

def test_calculo_distancia_mru(service_mock) -> None:
    """Prueba el cálculo básico: V * T = D."""
    ensayo = MovimientoRectilineoUniforme(
        id=1, nombre="Prueba", tipo="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=5, distancia=None
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.distancia == 50

def test_despeje_tiempo_mru(service_mock) -> None:
    """Prueba el despeje: T = D / V."""
    ensayo = MovimientoRectilineoUniforme(
        id=2, nombre="Despeje T", tipo="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=None, distancia=100
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.tiempo == 10

def test_despeje_velocidad_mru(service_mock) -> None:
    """Prueba el despeje: V = D / T."""
    ensayo = MovimientoRectilineoUniforme(
        id=2, nombre="Despeje V", tipo="Movimiento Rectilineo Uniforme",
        velocidad=None, tiempo=5 , distancia=100
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.velocidad == 20

def test_dato_negativo_error_velocidad(service_mock) -> None:
    """Prueba que se lance DatoNegativoError al ingresar una velocidad negativa."""
    # 1. Creamos el ensayo con un dato que SABEMOS que está mal (v = -10)
    ensayo = MovimientoRectilineoUniforme(
        id=99, 
        nombre="Prueba Error", 
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=-10, 
        tiempo=5,
        distancia=None
    )
    
    with pytest.raises(DatoNegativoError):
        service_mock.calcular_mru(ensayo)

def test_mru_error_datos_insuficientes(service_mock) -> None:
    """Prueba que falle si faltan 2 o más datos."""
    ensayo = MovimientoRectilineoUniforme(
        id=3, nombre="Incompleto", tipo="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=None, distancia=None # Faltan 2 datos
    )
    with pytest.raises(DatosInsuficientesError):
        service_mock.calcular_mru(ensayo)

def test_division_por_cero_error(service_mock) -> None:
    """Prueba que falla si V = 0 para calcular el tiempo T"""
    ensayo = MovimientoRectilineoUniforme(
        id=3, nombre="Prueba Cero", tipo="Movimiento Rectilineo Uniforme", 
        velocidad=0, tiempo=None, distancia=20 
    )

    with pytest.raises(DivisionPorCeroFisicaError):
        service_mock.calcular_mru(ensayo)

def test_storage_load_vacio(service_mock) -> None:
    """"""
    service_mock.storage.load.return_value = []

    ensayo = MovimientoRectilineoUniforme(
        id=101, 
        nombre="Primer Ensayo", 
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10.0, 
        tiempo=2.0, 
        distancia=None
    )
    
    service_mock.calcular_mru(ensayo)

    assert ensayo.distancia == 20.0 

def test_error_id_repetido(service_mock) -> None:
    """
    Verifica que el servicio lance IdExistente si el ID ya está registrado en el storage.
    """

    ensayo_existente = MovimientoRectilineoUniforme(
        id=50, nombre="Existente", tipo="MRU", velocidad=5, tiempo=2, distancia=10
    )
    service_mock.storage.load.return_value = [ensayo_existente] 

    nuevo_ensayo = MovimientoRectilineoUniforme(
        id=50, 
        nombre="Intruso", 
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10, 
        tiempo=5
    )

    with pytest.raises(IdExistente): 
        service_mock.calcular_mru(nuevo_ensayo)


def test_eliminar_ensayo_exito(service_mock) -> None:
    """
    Verifica que al eliminar un ensayo, se llame al método save del storage.
    """

    ensayo = MovimientoRectilineoUniforme(
        id=7, nombre="Para Borrar", tipo="MRU", velocidad=10, tiempo=5, distancia=50
    )
    service_mock.storage.load.return_value = [ensayo] 

    service_mock.eliminar_ensayo(7)

    service_mock.storage.save.assert_called_once() 

def test_eliminar_ensayo_error_no_existe(service_mock) -> None:
    """"""

    service_mock.storage.load.return_value = []

    with pytest.raises(ExperimentoNoExistenteError):
        service_mock.eliminar_ensayo(999)