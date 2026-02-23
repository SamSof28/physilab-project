"""Capa de servicios con la lógica de negocio del laboratorio.

Este módulo contiene la clase `LaboratorioService` que valida entradas,
realiza cálculos físicos (p. ej. MRU) y delega la persistencia a
`JSONStorage`.
"""

from .exceptions import (
    ExperimentoNoExistenteError,
    DatoNegativoError,
    IdExistente,
    DatosInsuficientesError,
    DivisionPorCeroFisicaError,
)
from .models import MovimientoRectilineoUniforme


from .storage import JSONStorage


class LaboratorioService:
    """Servicio principal que coordina validaciones, cálculos y persistencia.

    Attributes:
        storage (JSONStorage): Implementación de persistencia usada para
            cargar y guardar ensayos.
    """

    def __init__(self, storage: JSONStorage):
        """Inicializa el servicio con la implementación de almacenamiento.

        Args:
            storage (JSONStorage): Objeto que implementa la persistencia.
        """
        self.storage: JSONStorage = storage

    def calcular_mru(self, mru: MovimientoRectilineoUniforme) -> MovimientoRectilineoUniforme:
        """Calcula la variable faltante del MRU y persiste el ensayo.

        Exactly one of `velocidad`, `distancia` o `tiempo` may be None; the
        service computes the missing value from the other two.

        Args:
            mru (MovimientoRectilineoUniforme): Instancia con los parámetros
                del ensayo; uno de los campos de movimiento puede ser None.

        Returns:
            MovimientoRectilineoUniforme: La misma instancia `mru` con el
            campo calculado completado.

        Raises:
            DatosInsuficientesError: Si faltan más de un dato para calcular.
            IdExistente: Si el `id` ya está en la base de datos.
            ExperimentoNoExistenteError: Si el `id` es inválido (<= 0).
            DatoNegativoError: Si se proporcionan valores negativos no permitidos.
            DivisionPorCeroFisicaError: Si una operación requiere dividir por cero.
        """

        datos = [mru.distancia, mru.tiempo, mru.velocidad]

        nones = datos.count(None)

        if nones > 1:
            raise DatosInsuficientesError(nones)

        ensayos = self.storage.load()
        if any(e.id == mru.id for e in ensayos):
            raise IdExistente(mru.id)

        if mru.id <= 0:
            raise ExperimentoNoExistenteError(mru.id)

        # Validaciones de valores negativos (si fueron provistos)
        if mru.velocidad is not None and mru.velocidad < 0:
            raise DatoNegativoError(mru.velocidad)

        if mru.tiempo is not None and mru.tiempo < 0:
            raise DatoNegativoError(mru.tiempo)

        if mru.distancia is not None and mru.distancia < 0:
            raise DatoNegativoError(mru.distancia)

        # Cálculo de la variable faltante
        if mru.distancia is None:
            distancia_calculada = (mru.velocidad * mru.tiempo)
            mru.distancia = distancia_calculada
        elif mru.tiempo is None:
            if mru.velocidad == 0:
                raise DivisionPorCeroFisicaError("tiempo")
            tiempo_calculado = (mru.distancia / mru.velocidad)
            mru.tiempo = tiempo_calculado
        elif mru.velocidad is None:
            if mru.tiempo == 0:
                raise DivisionPorCeroFisicaError("velocidad")
            velocidad_calculada = (mru.distancia / mru.tiempo)
            mru.velocidad = velocidad_calculada

        ensayos.append(mru)
        self.storage.save(ensayos)
        return mru

    def eliminar_ensayo(self, ensayo_id: int) -> None:
        """Elimina un ensayo identificado por `ensayo_id`.

        Si no existe un ensayo con el id suministrado se lanza
        `ExperimentoNoExistenteError`.

        Args:
            ensayo_id (int): Identificador del ensayo a eliminar.
        """
        ensayos = self.storage.load()
        nuevos_ensayos = [e for e in ensayos if e.id != ensayo_id]

        if len(nuevos_ensayos) == len(ensayos):
            raise ExperimentoNoExistenteError(ensayo_id)

        self.storage.save(nuevos_ensayos)
