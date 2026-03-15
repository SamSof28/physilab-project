"""Persistencia JSON para los ensayos de PhysiLab.

Este módulo provee una interfaz `Storage` y una implementación `JSONStorage`
que se encarga de serializar y deserializar instancias de los modelos físicos
desde/hacia un archivo JSON.

Las implementaciones deben trabajar con las clases:
`TiroParabolico`, `CaidaLibre` y `MovimientoRectilineoUniforme`.
"""

import json
from pathlib import Path
from typing import List, Protocol
from .models import UniformRectilinearMotion, UniformlyAcceleratedRectilinearMotion
from .exceptions import InvalidExperimentNameError

class Storage(Protocol):
    """Protocolo que define la interfaz de persistencia para los ensayos.

    Implementaciones deben exponer los métodos `load()` y `save(...)`.
    """

    def load(self) -> List[UniformRectilinearMotion | UniformlyAcceleratedRectilinearMotion]: ...

    def save(self, experiments: List[UniformRectilinearMotion | UniformlyAcceleratedRectilinearMotion]) -> None: ...


class JsonStorage:
    """Implementación de `Storage` que usa un archivo JSON para persistir ensayos.

    Attributes:
        filepath (Path): Ruta al archivo JSON donde se almacenan los ensayos.
    """

    def __init__(self, filepath: Path):
        """Inicializa el almacenamiento con la ruta al archivo.

        Args:
            filepath (Path): Ruta al archivo JSON destino.
        """
        self.filepath = filepath

    def load(self) -> List[UniformRectilinearMotion | UniformlyAcceleratedRectilinearMotion]:
        """Carga y deserializa los ensayos desde el archivo JSON.

        Si el archivo no existe, devuelve una lista vacía.

        Returns:
            List[UniformRectilinearMotion | UniformlyAcceleratedRectilinearMotion]:
                Lista de instancias deserializadas.

        Raises:
            NombreExperimentoIncorrecto: Si el campo `tipo` en el JSON no coincide
                con ninguna de las clases de modelo esperadas.
        """
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r") as f:
            data = json.load(f)

        experiments: List[UniformRectilinearMotion | UniformlyAcceleratedRectilinearMotion] = []

        for item in data:
            experiment_type = item.get("tipo")

            if experiment_type == "Movimiento Rectilineo Uniforme":
                experiments.append(UniformRectilinearMotion(**item))
            elif experiment_type == "Movimiento Rectilineo Uniformemente Acelerado": 
                experiments.append(UniformlyAcceleratedRectilinearMotion(**item))
            else:
                raise InvalidExperimentNameError(experiment_type)

        return experiments

    def save(self, experiments: List[UniformRectilinearMotion | UniformlyAcceleratedRectilinearMotion]) -> None:
        """Serializa y guarda la lista de ensayos en el archivo JSON.

        Args:
            experiments: Lista de instancias de ensayo a persistir.
        """
        with open(self.filepath, "w") as f:
            json.dump([experiment.__dict__ for experiment in experiments], f, indent=2, ensure_ascii=False)

