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
from .models import TiroParabolico, CaidaLibre, MovimientoRectilineoUniforme
from .exceptions import NombreExperimentoIncorrecto

class Storage(Protocol):
    """Protocolo que define la interfaz de persistencia para los ensayos.

    Implementaciones deben exponer los métodos `load()` y `save(...)`.
    """

    def load(self) -> List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]: ...

    def save(self, ensayos_fisicos: List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]) -> None: ...


class JSONStorage:
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

    def load(self) -> List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]:
        """Carga y deserializa los ensayos desde el archivo JSON.

        Si el archivo no existe, devuelve una lista vacía.

        Returns:
            List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]:
                Lista de instancias deserializadas.

        Raises:
            NombreExperimentoIncorrecto: Si el campo `tipo` en el JSON no coincide
                con ninguna de las clases de modelo esperadas.
        """
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r") as f:
            data = json.load(f)

        ensayos: List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme] = []

        for item in data:
            tipo = item.get("tipo")

            if tipo == "Tiro Parabolico":
                ensayos.append(TiroParabolico(**item))
            elif tipo == "Caida Libre":
                ensayos.append(CaidaLibre(**item))
            elif tipo == "Movimiento Rectilineo Uniforme":
                ensayos.append(MovimientoRectilineoUniforme(**item))
            else:
                raise NombreExperimentoIncorrecto(tipo)

        return ensayos

    def save(self, ensayos_fisicos: List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]) -> None:
        """Serializa y guarda la lista de ensayos en el archivo JSON.

        Args:
            ensayos_fisicos: Lista de instancias de ensayo a persistir.
        """
        with open(self.filepath, "w") as f:
            json.dump([ensayo.__dict__ for ensayo in ensayos_fisicos], f, indent=2, ensure_ascii=False)