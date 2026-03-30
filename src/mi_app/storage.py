"""Persistencia JSON para los ensayos de PhysiLab."""

import json
from pathlib import Path
from typing import Protocol

from .models import MovimientoRectilineoUniforme, MovimientoRectilineoUniformementeAcelerado
from .exceptions import ErrorNombreExperimentoInvalido


class Storage(Protocol):
    """Protocolo que define la interfaz de persistencia para los ensayos."""

    def cargar(self) -> list[MovimientoRectilineoUniforme | MovimientoRectilineoUniformementeAcelerado]: ...

    def guardar(self, ensayos: list[MovimientoRectilineoUniforme | MovimientoRectilineoUniformementeAcelerado]) -> None: ...


class JsonStorage:
    """Implementación de persistencia basada en un archivo JSON."""

    def __init__(self, ruta_archivo: Path):
        self.ruta_archivo = ruta_archivo

    def cargar(self) -> list[MovimientoRectilineoUniforme | MovimientoRectilineoUniformementeAcelerado]:
        if not self.ruta_archivo.exists():
            return []

        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        ensayos: list[MovimientoRectilineoUniforme | MovimientoRectilineoUniformementeAcelerado] = []

        for item in datos:
            tipo_experimento = item.get("tipo")

            if tipo_experimento == "Movimiento Rectilineo Uniforme":
                ensayos.append(MovimientoRectilineoUniforme(**item))
            elif tipo_experimento == "Movimiento Rectilineo Uniformemente Acelerado":
                ensayos.append(MovimientoRectilineoUniformementeAcelerado(**item))
            else:
                raise ErrorNombreExperimentoInvalido(tipo_experimento)

        return ensayos

    def guardar(self, ensayos: list[MovimientoRectilineoUniforme | MovimientoRectilineoUniformementeAcelerado]) -> None:
        with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump([ensayo.__dict__ for ensayo in ensayos], archivo, indent=2, ensure_ascii=False)
