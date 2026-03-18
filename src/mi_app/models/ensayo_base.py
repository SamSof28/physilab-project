from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ExperimentoFisico:
    """Representa metadatos comunes a todos los ensayos.

    Atributos:
        id (int): Identificador único del ensayo.
        nombre (str): Nombre descriptivo del ensayo.
        tipo (str): Tipo de ensayo (p.ej. 'Tiro Parabolico').
        fecha (str): Marca temporal ISO del registro (formato YYYY-MM-DD HH:MM).
    """

    id: int
    nombre: str
    tipo: str
    fecha: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

