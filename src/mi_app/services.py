from .exceptions import (
    ExperimentoNoExistenteError,
    DatoNegativoError,
    IdExistente,
    DatosInsuficientesError
)
from .models import MovimientoRectilineoUniforme


from .storage import JSONStorage

class LaboratorioService:
    def __init__(self, storage: JSONStorage):
        self.storage: JSONStorage = storage

    def calcular_mru(self, mru: MovimientoRectilineoUniforme):

        datos = [mru.distancia, mru.tiempo, mru.velocidad]

        nones = datos.count(None)

        if nones > 1:
            raise DatosInsuficientesError(nones)

        ensayos = self.storage.load()
        if any(e.id == mru.id for e in ensayos):
            raise IdExistente(mru.id)

        if mru.id <= 0:
            raise ExperimentoNoExistenteError(mru.id)
        
        # Cambia tus validaciones por estas:
        if mru.velocidad is not None and mru.velocidad < 0:
            raise DatoNegativoError(mru.velocidad)

        if mru.tiempo is not None and mru.tiempo < 0:
            raise DatoNegativoError(mru.tiempo)

        if mru.distancia is not None and mru.distancia < 0:
            raise DatoNegativoError(mru.distancia)
        
        if mru.distancia is None:
            distancia_calculada = (mru.velocidad * mru.tiempo)
            mru.distancia = distancia_calculada
        elif mru.tiempo is None:
            if mru.velocidad == 0:
                raise ZeroDivisionError
            tiempo_calculado = (mru.distancia / mru.velocidad)
            mru.tiempo = tiempo_calculado
        elif mru.velocidad is None:
            if mru.tiempo == 0:
                raise ZeroDivisionError
            velocidad_calculada = (mru.distancia / mru.tiempo)
            mru.velocidad = velocidad_calculada

            ensayos.append(mru)
            self.storage.save(ensayos)
            return mru
    
    def eliminar_ensayo(self, ensayo_id: int):
        ensayos = self.storage.load()
        # Filtramos la lista para quitar el ID que queremos borrar
        nuevos_ensayos = [e for e in ensayos if e.id != ensayo_id]

        if len(nuevos_ensayos) == len(ensayos):
            raise ExperimentoNoExistenteError(ensayo_id)

        self.storage.save(nuevos_ensayos)
