from dataclasses import dataclass
from .ensayo_base import PhysicalExperiment
from ..exceptions import NegativeValueError

@dataclass
class UniformlyAcceleratedRectilinearMotion(PhysicalExperiment):
    """Modelo para Movimiento Rectilíneo Uniforme Acelerado (MRUA).

    Exactly one of the movement parameters may be left as None and the
    service layer will compute it from the other two:
    - velocidad (m/s)
    - distancia (m)
    - tiempo (s)

    Attributes:
        velocidad (float | None): Velocidad constante en m/s.
        posicion (float | None): posicion recorrida en metros.
        tiempo (float | None): Tiempo transcurrido en segundos.
        aceleracion (float | None): Aceleración constante en m / s^2
    """
    posicion_inicial: float | None = None
    velocidad_inicial: float | None = None
    aceleracion: float | None = None
    tiempo: float | None = None
    posicion_final: float | None = None
    velocidad_final: float | None = None

    def __post_init__(self):
        self._validate_consistency()

    def _validate_consistency(self) -> None:
        values = [
            self.posicion_inicial, self.velocidad_inicial, 
            self.aceleracion, self.tiempo, 
            self.posicion_final, self.velocidad_final
        ]
        for value in values:
            if value is not None and value < 0:
                # El modelo se protege a sí mismo de datos imposibles
                raise NegativeValueError(value)


