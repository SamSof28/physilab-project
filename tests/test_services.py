import pytest
from unittest.mock import MagicMock

from src.mi_app.exceptions import (
    ErrorDatosInsuficientes,
    ErrorDivisionPorCeroFisica,
    ErrorExperimentoNoEncontrado,
    ErrorIdDuplicado,
    ErrorValorNegativo,
)
from src.mi_app.models.mru import MovimientoRectilineoUniforme
from src.mi_app.services import LaboratoryService


@pytest.fixture
def service_mock() -> LaboratoryService:
    """Crea una instancia del servicio con un almacenamiento simulado."""
    almacenamiento_simulado = MagicMock()
    almacenamiento_simulado.cargar.return_value = []
    return LaboratoryService(almacenamiento_simulado)


def test_calculo_distancia_mru(service_mock) -> None:
    """Verifica el cálculo básico de MRU: velocidad * tiempo = distancia."""
    ensayo = MovimientoRectilineoUniforme(
        id=1,
        nombre="Prueba",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10,
        tiempo=5,
        distancia=None,
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.distancia == 50


def test_despeje_tiempo_mru(service_mock) -> None:
    """Verifica el despeje de tiempo: distancia / velocidad."""
    ensayo = MovimientoRectilineoUniforme(
        id=2,
        nombre="Despeje T",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10,
        tiempo=None,
        distancia=100,
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.tiempo == 10


def test_despeje_velocidad_mru(service_mock) -> None:
    """Verifica el despeje de velocidad: distancia / tiempo."""
    ensayo = MovimientoRectilineoUniforme(
        id=3,
        nombre="Despeje V",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=None,
        tiempo=5,
        distancia=100,
    )
    service_mock.calcular_mru(ensayo)
    assert ensayo.velocidad == 20


def test_valor_negativo_lanza_error(service_mock) -> None:
    """Verifica que una velocidad negativa lance el error de valor negativo."""
    with pytest.raises(ErrorValorNegativo):
        MovimientoRectilineoUniforme(
            id=99,
            nombre="Prueba Error",
            tipo="Movimiento Rectilineo Uniforme",
            velocidad=-10,
            tiempo=5,
            distancia=None,
        )


def test_datos_insuficientes_mru(service_mock) -> None:
    """Verifica que falle si faltan dos o más datos en MRU."""
    ensayo = MovimientoRectilineoUniforme(
        id=4,
        nombre="Incompleto",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10,
        tiempo=None,
        distancia=None,
    )
    with pytest.raises(ErrorDatosInsuficientes):
        service_mock.calcular_mru(ensayo)


def test_division_por_cero_mru(service_mock) -> None:
    """Verifica que falle si la velocidad es 0 al calcular tiempo."""
    ensayo = MovimientoRectilineoUniforme(
        id=5,
        nombre="Prueba Cero",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=0,
        tiempo=None,
        distancia=20,
    )

    with pytest.raises(ErrorDivisionPorCeroFisica):
        service_mock.calcular_mru(ensayo)


def test_carga_vacia_almacenamiento(service_mock) -> None:
    """Verifica que se calcule y persista correctamente con almacenamiento vacío."""
    service_mock.almacenamiento.cargar.return_value = []

    ensayo = MovimientoRectilineoUniforme(
        id=101,
        nombre="Primer Ensayo",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10.0,
        tiempo=2.0,
        distancia=None,
    )

    service_mock.calcular_mru(ensayo)

    assert ensayo.distancia == 20.0


def test_id_duplicado_lanza_error(service_mock) -> None:
    """Verifica que se lance error si el ID ya está registrado."""
    ensayo_existente = MovimientoRectilineoUniforme(
        id=50,
        nombre="Existente",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=5,
        tiempo=2,
        distancia=10,
    )
    service_mock.almacenamiento.cargar.return_value = [ensayo_existente]

    nuevo_ensayo = MovimientoRectilineoUniforme(
        id=50,
        nombre="Intruso",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10,
        tiempo=5,
        distancia=None,
    )

    with pytest.raises(ErrorIdDuplicado):
        service_mock.calcular_mru(nuevo_ensayo)


def test_eliminar_ensayo_exitoso(service_mock) -> None:
    """Verifica que al eliminar un ensayo se invoque el guardado."""
    ensayo = MovimientoRectilineoUniforme(
        id=7,
        nombre="Para Borrar",
        tipo="Movimiento Rectilineo Uniforme",
        velocidad=10,
        tiempo=5,
        distancia=50,
    )
    service_mock.almacenamiento.cargar.return_value = [ensayo]

    service_mock.eliminar_ensayo(7)

    service_mock.almacenamiento.guardar.assert_called_once()


def test_eliminar_ensayo_no_encontrado(service_mock) -> None:
    """Verifica que se lance error cuando el ensayo no existe."""
    service_mock.almacenamiento.cargar.return_value = []

    with pytest.raises(ErrorExperimentoNoEncontrado):
        service_mock.eliminar_ensayo(999)
