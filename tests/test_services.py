import pytest
from unittest.mock import MagicMock
from pydantic import ValidationError

from src.core.exceptions import (
    ErrorDivisionPorCeroFisica,
    ErrorDiscriminanteNegativo,
    ErrorValorNegativo,
)
from src.schemas.mru import MRUSchema
from src.schemas.mrua import MRUASchema
from src.services.physics_service import PhysicsService


@pytest.fixture
def service_mock() -> PhysicsService:
    """Crea una instancia del servicio aislando por completo la base de datos."""
    service = PhysicsService()
    # Reemplazamos el repositorio real por un simulador (Mock)
    service.repository = MagicMock()
    return service


# --- PRUEBAS DE MOVIMIENTO RECTILÍNEO UNIFORME (MRU) ---

def test_calculo_distancia_mru(service_mock) -> None:
    """Verifica el cálculo básico de MRU: velocidad * tiempo = distancia."""
    datos = MRUSchema(velocidad=10.0, tiempo=5.0, distancia=None)
    service_mock.resolver_y_guardar_mru("Ensayo Test", datos)
    assert datos.distancia == 50.0


def test_despeje_tiempo_mru(service_mock) -> None:
    """Verifica el despeje de tiempo en MRU: distancia / velocidad."""
    datos = MRUSchema(velocidad=10.0, tiempo=None, distancia=100.0)
    service_mock.resolver_y_guardar_mru("Ensayo Test", datos)
    assert datos.tiempo == 10.0


def test_despeje_velocidad_mru(service_mock) -> None:
    """Verifica el despeje de velocidad en MRU: distancia / tiempo."""
    datos = MRUSchema(velocidad=None, tiempo=5.0, distancia=100.0)
    service_mock.resolver_y_guardar_mru("Ensayo Test", datos)
    assert datos.velocidad == 20.0


def test_division_por_cero_mru(service_mock) -> None:
    """Verifica que falle arrojando una excepción controlada si la velocidad es 0 al despejar tiempo."""
    datos = MRUSchema(velocidad=0.0, tiempo=None, distancia=50.0)
    with pytest.raises(ErrorDivisionPorCeroFisica):
        service_mock.resolver_y_guardar_mru("Ensayo Fallido", datos)


# --- PRUEBAS DE VALIDACIÓN DE CONTRATOS (SCHEMAS) ---

def test_valor_negativo_mru_lanza_error() -> None:
    """Verifica que Pydantic atrape valores negativos mediante nuestro validador corporativo."""
    with pytest.raises(ErrorValorNegativo):
        MRUSchema(velocidad=-10.0, tiempo=5.0, distancia=None)


def test_valor_negativo_mrua_lanza_error() -> None:
    """Verifica que el esquema de MRUA también bloquee parámetros físicos negativos."""
    with pytest.raises(ErrorValorNegativo):
        MRUASchema(posicion_inicial=0.0, aceleracion=-2.5, tiempo=4.0)


# --- PRUEBAS DE MOVIMIENTO RECTILÍNEO UNIFORMEMENTE ACELERADO (MRUA) ---

def test_calculo_posicion_final_mrua(service_mock) -> None:
    """Verifica la ecuación completa de posición para MRUA."""
    mrua_data = MRUASchema(
        posicion_inicial=10.0,
        posicion_final=None,
        aceleracion=2.0,
        tiempo=3.0,
        velocidad_inicial=5.0,
        velocidad_final=None
    )
    service_mock.resolver_y_guardar_mrua("Ensayo Acelerado", mrua_data)
    # xf = 10 + (5*3) + (0.5 * 2 * 3^2) = 10 + 15 + 9 = 34
    assert mrua_data.posicion_final == 34.0


def test_mrua_discriminante_negativo_lanza_error(service_mock) -> None:
    """Verifica que situaciones físicas imposibles (raíz negativa en el tiempo) disparen el error matemático."""
    mrua_inviable = MRUASchema(
        posicion_inicial=100.0,
        posicion_final=0.0,
        aceleracion=2.0,
        tiempo=None,
        velocidad_inicial=5.0,
        velocidad_final=None
    )
    with pytest.raises(ErrorDiscriminanteNegativo):
        service_mock.resolver_y_guardar_mrua("Ensayo Imposible", mrua_inviable)


# --- PRUEBAS DE PERSISTENCIA Y BORRADO (CRUD LOGIC) ---

def test_eliminar_experimento_exitoso(service_mock) -> None:
    """Verifica que el servicio retorne True cuando el repositorio confirma la eliminación."""
    service_mock.repository.delete.return_value = True
    resultado = service_mock.remove_one(5)
    assert resultado is True
    service_mock.repository.delete.assert_called_once_with(5)


def test_eliminar_experimento_inexistente(service_mock) -> None:
    """Verifica que el servicio retorne False si intentamos borrar un ID que no figura en la base de datos."""
    service_mock.repository.delete.return_value = False
    resultado = service_mock.remove_one(9999)
    assert resultado is False