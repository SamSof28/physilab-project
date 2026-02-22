import json
from pathlib import Path
from typing import List, Protocol
from .models import EnsayoFisico, TiroParabolico, CaidaLibre, MovimientoRectilineoUniforme
from .exceptions import NombreExperimentoIncorrecto

class Storage(Protocol):
    def load(self, filepath: Path) -> List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]: ...

    def save(self, ensayos_fisicos: List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]) -> None: ...


class JSONStorage:
    def __init__(self, filepath: Path):
        self.filepath = filepath

    def load(self) -> List[TiroParabolico | CaidaLibre | MovimientoRectilineoUniforme]:
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
        with open(self.filepath, "w") as f:
            json.dump([ensayo.__dict__ for ensayo in ensayos_fisicos], f, indent=2)