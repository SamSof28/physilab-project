from dataclasses import dataclass
from .ensayo_base import ExperimentoFisico
from ..exceptions import ErrorValorNegativo

@dataclass
class MovimientoRectilineoUniformementeAcelerado(ExperimentoFisico):
    """Modelo para Movimiento Rectilíneo Uniforme Acelerado (MRUA).

    Puedes dejar exactamente uno de los parámetros de movimiento como None, 
    y la capa de servicio lo calculará a partir de los otros tres:
    - posicion_inicial (m)
    - posicion_final (m)
    - aceleracion (m/s^2)
    - tiempo (s)
    - velocidad_inicial (m/s)
    - velocidad_final (m/s)

    Atributos:
        posicion_inicial (float | None): Posición inicial en m
        posicion_final (float | None): Posición final en m
        aceleracion (float | None): aceleracion en m/s^2
        tiempo (float | None): Tiempo transcurrido en segundos.
        velocidad_inicial (float | None): Velocidad inicial en m/s.
        velocidad_final (float | None): Velocidad final en m/s.        
    """
    posicion_inicial: float | None = None
    posicion_final: float | None = None
    aceleracion: float | None = None
    tiempo: float | None = None
    velocidad_inicial: float | None = None
    velocidad_final: float | None = None

    def __post_init__(self):
        self._validar_consistencia()

    def _validar_consistencia(self) -> None:
        valores = [
            self.posicion_inicial, self.velocidad_inicial, 
            self.aceleracion, self.tiempo, 
            self.posicion_final, self.velocidad_final
        ]
        for valor in valores:
            if valor is not None and valor < 0:
                # El modelo se protege a sí mismo de datos imposibles
                raise ErrorValorNegativo(valor)


