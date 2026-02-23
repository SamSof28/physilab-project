class AppError(Exception):
    """Base class for all custom exceptions in PhysiLab.

    Use this as the root exception so higher-level code can catch
    application-specific errors uniformly.
    """


class FisicaLabError(AppError):
    """Errors related to physics computations or input validation.

    Examples: invalid angles, negative physical values, insufficient data.
    """


class BaseDatosError(AppError):
    """Errors related to data storage or database operations.

    Examples: duplicate IDs, missing records, invalid experiment names.
    """


class AnguloInvalidoError(FisicaLabError):
    """Raised when an angle value provided by the user is invalid.

    Attributes:
        angulo (float): The invalid angle value supplied by the user.
    """

    def __init__(self, angulo: float) -> None:
        self.angulo: float = angulo
        super().__init__(f"Ángulo inválido: el valor {angulo}° no es aceptable.")


class DatoNegativoError(FisicaLabError):
    """Raised when a numeric value that must be non-negative is negative.

    Attributes:
        numero (float): The negative number provided by the user.
    """

    def __init__(self, numero: float) -> None:
        self.numero: float = numero
        super().__init__(f"Valor inválido: {numero} — se esperaba un valor no negativo.")


class DivisionPorCeroFisicaError(FisicaLabError):
    """Raised when a physics calculation would divide by zero.

    Attributes:
        magnitud (str): The quantity attempted to be calculated (e.g. 'tiempo').
    """

    def __init__(self, magnitud: str):
        self.magnitud = magnitud
        super().__init__(f"Error matemático: imposible calcular '{magnitud}' con divisor igual a cero.")


class DatosInsuficientesError(FisicaLabError):
    """Raised when there are not enough input values to perform a calculation.

    Attributes:
        cantidad_faltante (int): Number of missing values required to compute the result.
    """

    def __init__(self, cantidad_faltante: int = 1) -> None:
        self.cantidad_faltante: int = cantidad_faltante
        plural = "dato" if cantidad_faltante == 1 else "datos"
        super().__init__(f"Datos insuficientes: faltan {cantidad_faltante} {plural} para completar el cálculo.")


class ExperimentoNoExistenteError(BaseDatosError):
    """Raised when a referenced experiment identifier is invalid or not found.

    Attributes:
        id (int): The identifier supplied by the caller.
    """

    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__(f"Identificador inválido: el id {id} no corresponde a ningún experimento.")


class NombreExperimentoIncorrecto(BaseDatosError):
    """Raised when the supplied experiment name is not recognized.

    Attributes:
        nombre (str): The invalid experiment name provided by the user.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        super().__init__(f"Nombre de experimento inválido: '{nombre}' no es un ensayo válido.")


class IdExistente(BaseDatosError):
    """Raised when attempting to create a record with an identifier that already exists.

    Attributes:
        id (int): The duplicated identifier.
    """

    def __init__(self, id: int):
        self.id: int = id
        super().__init__(f"Identificador duplicado: el id {id} ya existe en la base de datos.")