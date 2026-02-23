"""Modelos de dominio para los ensayos físicos de PhysiLab.

Este módulo define las entidades usadas por la aplicación:
- EnsayoFisico: clase base con metadatos comunes.
- TiroParabolico: propiedades específicas para tiro parabólico.
- CaidaLibre: propiedades específicas para caída libre.
- MovimientoRectilineoUniforme: propiedades para MRU.

Las unidades se indican en los docstrings de cada atributo cuando aplican.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EnsayoFisico:
    """Representa metadatos comunes a todos los ensayos.

    Attributes:
        id (int): Identificador único del ensayo.
        nombre (str): Nombre descriptivo del ensayo.
        tipo (str): Tipo de ensayo (p.ej. 'Tiro Parabolico').
        fecha (str): Marca temporal ISO del registro (formato YYYY-MM-DD HH:MM).
    """

    id: int
    nombre: str
    tipo: str
    fecha: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))


@dataclass
class TiroParabolico(EnsayoFisico):
    """Modelo para cálculos y resultados de un tiro parabólico.

    Attributes:
        velocidad_inicial (float): Velocidad inicial en m/s.
        angulo (float): Ángulo de lanzamiento en grados.
        gravedad (float): Aceleración debida a la gravedad en m/s^2.
        alcance_maximo (float): Alcance máximo calculado en metros.
        altura_maxima (float): Altura máxima alcanzada en metros.
        tiempo_vuelo (float): Tiempo total de vuelo en segundos.
    """

    velocidad_inicial: float = 0.0  # m/s
    angulo: float = 0.0  # grados
    gravedad: float = 9.8  # m/s^2
    alcance_maximo: float = 0.0  # m
    altura_maxima: float = 0.0  # m
    tiempo_vuelo: float = 0.0  # s


@dataclass
class CaidaLibre(EnsayoFisico):
    """Modelo para cálculos de caída libre desde una altura.

    Attributes:
        velocidad_inicial (float): Velocidad inicial en m/s (por defecto 0).
        altura (float): Altura inicial en metros.
        gravedad (float): Aceleración debida a la gravedad en m/s^2.
    """

    velocidad_inicial: float = 0.0  # m/s
    altura: float = 0.0  # m
    gravedad: float = 9.8  # m/s^2


@dataclass
class MovimientoRectilineoUniforme(EnsayoFisico):
    """Modelo para Movimiento Rectilíneo Uniforme (MRU).

    Exactly one of the movement parameters may be left as None and the
    service layer will compute it from the other two:
    - velocidad (m/s)
    - distancia (m)
    - tiempo (s)

    Attributes:
        velocidad (float | None): Velocidad constante en m/s.
        distancia (float | None): Distancia recorrida en metros.
        tiempo (float | None): Tiempo transcurrido en segundos.
    """

    velocidad: float | None = None
    distancia: float | None = None
    tiempo: float | None = None

