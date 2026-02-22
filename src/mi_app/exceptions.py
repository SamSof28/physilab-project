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

class ExperimentoNoExistente(BaseDatosError):
    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__(f"El id {id} del experimento no existe")

class NombreExperimentoIncorrecto(BaseDatosError):
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        super().__init__(f"El nombre {nombre} no es un experimento valido")