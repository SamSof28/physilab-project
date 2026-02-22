from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class EnsayoFisico:
    """Clase base para representar un experimento"""
    id: int
    nombre: str
    tipo: str
    fecha: str = field(default_factory=lambda : datetime.now().strftime("%Y-%m-%d %H: %M"))
    

@dataclass
class TiroParabolico(EnsayoFisico):
    """Modelo especifico para simulaciones y calculos de Tiro Parabolico"""
    velocidad_inicial: float = 0.0 #m/s
    angulo: float = 0.0#grados
    gravedad: float = 9.8 #m/s^2
    alcance_maximo: float = 0.0
    altura_maxima: float = 0.0 
    tiempo_vuelo: float = 0.0

@dataclass
class CaidaLibre(EnsayoFisico):
    """Modelo especifico para simulaciones y calculos de Caida Libre"""
    velocidad_inicial: float = 0.0#m/s
    altura: float = 0.0#metros
    gravedad: float = 9.8 #m/s^2

@dataclass
class MovimientoRectilineoUniforme(EnsayoFisico):
    """Modelo especifico para simulaciones y calculos de M.R.U"""
    velocidad: float = 0.0
