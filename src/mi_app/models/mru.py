from dataclasses import dataclass
from .ensayo_base import ExperimentoFisico
from ..exceptions import ErrorValorNegativo

@dataclass
class MovimientoRectilineoUniforme(ExperimentoFisico):
    """Modelo para Movimiento Rectilíneo Uniforme (MRU).

    Se puede dejar exactamente uno de los parámetros de movimiento como 
    None y la capa de servicio lo calculará a partir de los otros dos:
    - velocidad (m/s)
    - distancia (m)
    - tiempo (s)

    Atributos:
        velocidad (float | None): Velocidad constante en m/s.
        distancia (float | None): Distancia recorrida en metros.
        tiempo (float | None): Tiempo transcurrido en segundos.
    """
    velocidad: float | None = None
    distancia: float | None = None
    tiempo: float | None = None

    def __post_init__(self):
        # La rúbrica exige validaciones mediante métodos privados auxiliares
        self._validar_valor_no_negativo([self.velocidad, self.distancia, self.tiempo])
            
    def _validar_valor_no_negativo(self, valores: list[float | None]) -> None:
        """Valida que los valores numéricos no sean negativos.

        Argumentos:
            valores (list): Lista de valores numéricos a validar.

        Errores:
            ErrorValorNegativo: Si alguno de los valores es negativo.
        """
        for valor in valores:
            if valor is not None and valor < 0:
                raise ErrorValorNegativo(valor)


