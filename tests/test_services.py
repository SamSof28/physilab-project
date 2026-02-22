import pytest
from unittest.mock import MagicMock
from src.mi_app.services import LaboratorioService
from src.mi_app.models import MovimientoRectilineoUniforme
from src.mi_app.exceptions import DatosInsuficientesError

# --- FIXTURES ---
@pytest.fixture
def service_mock():
    """Crea una instancia del servicio con un storage simulado."""
    mock_storage = MagicMock()
    mock_storage.load.return_value = [] # Simula base de datos vacía
    return LaboratorioService(mock_storage)

# --- TESTS DE MRU ---

def test_calculo_distancia_mru(service_mock):
    """Prueba el cálculo básico: V * T = D."""
    ensayo = MovimientoRectilineoUniforme(
        id=1, nombre="Prueba", tipo="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=5, distancia=None
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.distancia == 50

def test_despeje_tiempo_mru(service_mock):
    """Prueba el despeje: D / V = T."""
    ensayo = MovimientoRectilineoUniforme(
        id=2, nombre="Despeje T", tipo="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=None, distancia=100
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.tiempo == 10

def test_mru_error_datos_insuficientes(service_mock):
    """Prueba que falle si faltan 2 o más datos."""
    ensayo = MovimientoRectilineoUniforme(
        id=3, nombre="Incompleto", tipo="Movimiento Rectilineo Uniforme", 
        velocidad=10, tiempo=None, distancia=None # Faltan 2 datos
    )
    with pytest.raises(DatosInsuficientesError):
        service_mock.calcular_mru(ensayo)

# --- ESPACIO PARA TIRO PARABÓLICO (Próximamente) ---
# def test_calculo_parabolico(service_mock):
#     ...