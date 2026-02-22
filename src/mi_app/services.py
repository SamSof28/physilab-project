import numpy as np
from .exceptions import (
    ExperimentoNoExistente,
    DatoNegativoError,
    IdExistente
)
from .models import (
    EnsayoFisico, 
    TiroParabolico, 
    CaidaLibre, MovimientoRectilineoUniforme)


from .storage import Storage, JSONStorage

class LaboratorioService:
    def __init__(self, storage: JSONStorage):
        self.storage: JSONStorage = storage

    def crear_mru(self, mru: MovimientoRectilineoUniforme):
        if mru.id <= 0:
            raise ExperimentoNoExistente(mru.id)
        
        if mru.velocidad < 0:
            raise DatoNegativoError(mru.velocidad)
        
        if mru.tiempo < 0:
            raise DatoNegativoError(mru.tiempo)
        
        ensayos = self.storage.load()
        if any(e.id == mru.id for e in ensayos):
            raise IdExistente(mru.id)
        

        distancia_calculada = (mru.velocidad * mru.tiempo).item()
        mru.distancia = distancia_calculada

        ensayos.append(mru)
        self.storage.save(ensayos)
        return mru