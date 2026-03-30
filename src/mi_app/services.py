"""Capa de servicios con la lógica de negocio del laboratorio."""

from .exceptions import (
    ErrorExperimentoNoEncontrado,
    ErrorIdDuplicado,
    ErrorDatosInsuficientes,
    ErrorDivisionPorCeroFisica,
    ErrorDiscriminanteNegativo,
)
from .models.mru import MovimientoRectilineoUniforme
from .models.mrua import MovimientoRectilineoUniformementeAcelerado
from .storage import JsonStorage


class LaboratoryService:
    """Servicio principal del dominio del laboratorio."""

    def __init__(self, storage: JsonStorage):
        self.storage: JsonStorage = storage

    def _verificar_id_unico(self, id_experimento: int) -> None:
        if id_experimento <= 0:
            raise ErrorExperimentoNoEncontrado(id_experimento)

        ensayos = self.storage.cargar()
        if any(ensayo.id == id_experimento for ensayo in ensayos):
            raise ErrorIdDuplicado(id_experimento)

    def _guardar_ensayo(self, ensayo: object) -> None:
        ensayos = self.storage.cargar()
        ensayos.append(ensayo)
        self.storage.guardar(ensayos)

    def _division_segura(self, numerador: float, denominador: float, nombre_magnitud: str) -> float:
        if denominador == 0:
            raise ErrorDivisionPorCeroFisica(nombre_magnitud)

        return numerador / denominador

    def _resolver_mru(self, mru: MovimientoRectilineoUniforme) -> MovimientoRectilineoUniforme:
        if mru.distancia is None:
            mru.distancia = mru.velocidad * mru.tiempo
        elif mru.tiempo is None:
            mru.tiempo = self._division_segura(mru.distancia, mru.velocidad, "tiempo")
        elif mru.velocidad is None:
            mru.velocidad = self._division_segura(mru.distancia, mru.tiempo, "velocidad")
        return mru

    def calcular_mru(self, mru: MovimientoRectilineoUniforme) -> MovimientoRectilineoUniforme:
        self._verificar_id_unico(mru.id)

        faltantes = [mru.distancia, mru.tiempo, mru.velocidad].count(None)
        if faltantes > 1:
            raise ErrorDatosInsuficientes(faltantes)

        mru = self._resolver_mru(mru)
        self._guardar_ensayo(mru)
        return mru

    def _resolver_tiempo_mrua(self, mrua: MovimientoRectilineoUniformementeAcelerado) -> float:
        if (
            mrua.velocidad_final is not None
            and mrua.velocidad_inicial is not None
            and mrua.aceleracion not in (None, 0)
        ):
            mrua.tiempo = (mrua.velocidad_final - mrua.velocidad_inicial) / mrua.aceleracion
            return mrua.tiempo

        return self._resolver_tiempo_cuadratico(
            mrua.aceleracion,
            mrua.velocidad_inicial,
            mrua.posicion_inicial,
            mrua.posicion_final,
        )

    def _resolver_tiempo_cuadratico(self, aceleracion: float, velocidad_inicial: float, posicion_inicial: float, posicion_final: float) -> float:
        coef_a = 0.5 * aceleracion
        coef_b = velocidad_inicial
        coef_c = posicion_inicial - posicion_final

        discriminante = coef_b ** 2 - 4 * coef_a * coef_c
        if discriminante < 0:
            raise ErrorDiscriminanteNegativo(discriminante)

        return (-coef_b + (discriminante ** 0.5)) / (2 * coef_a)

    def _resolver_aceleracion_mrua(self, mrua: MovimientoRectilineoUniformementeAcelerado) -> float:
        if mrua.tiempo == 0:
            raise ErrorDivisionPorCeroFisica("tiempo")

        return (mrua.velocidad_final - mrua.velocidad_inicial) / mrua.tiempo

    def resolver_mrua(self, mrua: MovimientoRectilineoUniformementeAcelerado) -> MovimientoRectilineoUniformementeAcelerado:
        if mrua.aceleracion is None:
            mrua.aceleracion = self._resolver_aceleracion_mrua(mrua)
        if mrua.posicion_final is None:
            mrua.posicion_final = (
                mrua.posicion_inicial
                + (mrua.velocidad_inicial * mrua.tiempo)
                + (0.5 * mrua.aceleracion * (mrua.tiempo ** 2))
            )
        if mrua.velocidad_final is None:
            mrua.velocidad_final = mrua.velocidad_inicial + (mrua.aceleracion * mrua.tiempo)
        if mrua.tiempo is None:
            mrua.tiempo = self._resolver_tiempo_mrua(mrua)
        return mrua

    def _resolver_mrua(self, mrua: MovimientoRectilineoUniformementeAcelerado) -> MovimientoRectilineoUniformementeAcelerado:
        return self.resolver_mrua(mrua)

    def _validar_existencia_y_no_negativos(self, mrua: MovimientoRectilineoUniformementeAcelerado) -> None:
        self._verificar_id_unico(mrua.id)

    def calcular_mrua(self, mrua: MovimientoRectilineoUniformementeAcelerado) -> MovimientoRectilineoUniformementeAcelerado:
        self._validar_existencia_y_no_negativos(mrua)
        mrua = self._resolver_mrua(mrua)
        self._guardar_ensayo(mrua)
        return mrua

    def eliminar_ensayo(self, id_experimento: int) -> None:
        ensayos = self.storage.cargar()
        ensayos_filtrados = [ensayo for ensayo in ensayos if ensayo.id != id_experimento]

        if len(ensayos_filtrados) == len(ensayos):
            raise ErrorExperimentoNoEncontrado(id_experimento)

        self.storage.guardar(ensayos_filtrados)
