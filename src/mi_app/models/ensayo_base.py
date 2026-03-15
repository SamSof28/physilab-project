from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PhysicalExperiment:
    """Representa metadatos comunes a todos los ensayos.

    Attributes:
        id (int): Identificador único del ensayo.
        nombre (str): Nombre descriptivo del ensayo.
        tipo (str): Tipo de ensayo (p.ej. 'Tiro Parabolico').
        fecha (str): Marca temporal ISO del registro (formato YYYY-MM-DD HH:MM).
    """

    id: int
    name: str
    experiment_type: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

