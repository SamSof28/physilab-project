class AppError(Exception):
    """Clase base para las excepciones del programa"""
    pass

class FisicaLabError(AppError):
    """Clase base para los errores relacionados con Fisica"""
    pass

class BaseDatosError(AppError):
    """Clase base para los errores relacionados con la base de datos"""
    pass

class AnguloInvalidoError(FisicaLabError):
    def __init__(self, angulo: float) -> None:
        self.angulo: float = angulo
        super().__init__(f"El Angulo {angulo}° ingresado es invalido")

class DatoNegativoError(FisicaLabError):
    def __init__(self, numero: float) -> None:
        self.numero: float = numero
        super().__init__(f"El número {numero} ingresado es invalido")

class DivisionPorCeroFisicaError(AppError):
    """Excepción lanzada cuando una operación física resulta en división por cero."""
    def __init__(self, magnitud: str):
        self.magnitud = magnitud
        super().__init__(f"Error Matemático: No se puede calcular {magnitud} con un divisor de cero.")

class DatosInsuficientesError(FisicaLabError):
    def __init__(self, cantidad_faltante: int = 1) -> None:
        self.cantidad_faltante: int = cantidad_faltante
        super().__init__(f"Faltan {cantidad_faltante} dato(s) para realizar el cálculo")

class ExperimentoNoExistenteError(BaseDatosError):
    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__(f"El id {id} del experimento no es valido")

class NombreExperimentoIncorrecto(BaseDatosError):
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        super().__init__(f"El nombre {nombre} no es un experimento valido")

class IdExistente(BaseDatosError):
    def __init__(self, id: int):
        self.id: int = id
        super().__init__(f"El id {id} ingresado ya se encuentra usado en la base de datos")