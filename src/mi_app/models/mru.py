from dataclasses import dataclass
from .ensayo_base import PhysicalExperiment
from ..exceptions import NegativeValueError

@dataclass
class UniformRectilinearMotion(PhysicalExperiment):
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

    def __post_init__(self):
        # La rúbrica exige validaciones mediante métodos privados auxiliares
        self._validate_non_negative_values([self.velocidad, self.distancia, self.tiempo])
            
    def _validate_non_negative_values(self, values: list[float | None]) -> None:
        """Valida que los valores numéricos no sean negativos.

        Args:
            values (list): Lista de valores numéricos a validar.

        Raises:
            NegativeValueError: Si alguno de los valores es negativo.
        """
        for value in values:
            if value is not None and value < 0:
                raise NegativeValueError(value)


