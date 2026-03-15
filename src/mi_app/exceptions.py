class AppError(Exception):
    """Base class for all custom exceptions in PhysiLab.

    Use this as the root exception so higher-level code can catch
    application-specific errors uniformly.
    """


class PhysicsLabError(AppError):
    """Errors related to physics computations or input validation.

    Examples: invalid angles, negative physical values, insufficient data.
    """


class DatabaseError(AppError):
    """Errors related to data storage or database operations.

    Examples: duplicate IDs, missing records, invalid experiment names.
    """


class InvalidAngleError(PhysicsLabError):
    """Raised when an angle value provided by the user is invalid.

    Attributes:
        angulo (float): The invalid angle value supplied by the user.
    """

    def __init__(self, angle: float) -> None:
        self.angle: float = angle
        super().__init__(f"Ángulo inválido: el valor {angle}° no es aceptable.")


class NegativeValueError(PhysicsLabError):
    """Raised when a numeric value that must be non-negative is negative.

    Attributes:
        numero (float): The negative number provided by the user.
    """

    def __init__(self, value: float) -> None:
        self.value: float = value
        super().__init__(f"Valor inválido: {value} — se esperaba un valor no negativo.")


class PhysicsDivisionByZeroError(PhysicsLabError):
    """Raised when a physics calculation would divide by zero.

    Attributes:
        magnitud (str): The quantity attempted to be calculated (e.g. 'tiempo').
    """

    def __init__(self, quantity: float):
        self.quantity = quantity
        super().__init__(f"Error matemático: imposible calcular '{quantity}' con divisor igual a cero.")

class NegativeDiscriminantError(PhysicsLabError):
    """It is generated when a physical calculation of the discriminant is less than zero.

    Attributes:
        magnitud (float): The quantity attempted to be calculated (e.g. 'discriminante').
    """

    def __init__(self, discriminant: float):
        self.discriminant: float = discriminant
        super().__init__(f"Error matematico: Imposible calcular '{discriminant}' con disciminante menor a cero")


class InsufficientDataError(PhysicsLabError):
    """Raised when there are not enough input values to perform a calculation.

    Attributes:
        cantidad_faltante (int): Number of missing values required to compute the result.
    """

    def __init__(self, missing_count: int = 1) -> None:
        self.missing_count: int = missing_count
        plural = "dato" if missing_count == 1 else "datos"
        super().__init__(f"Datos insuficientes: faltan {missing_count} {plural} para completar el cálculo.")


class ExperimentNotFoundError(DatabaseError):
    """Raised when a referenced experiment identifier is invalid or not found.

    Attributes:
        id (int): The identifier supplied by the caller.
    """

    def __init__(self, experiment_id: int) -> None:
        self.experiment_id = experiment_id
        super().__init__(f"Identificador inválido: el id {experiment_id} no corresponde a ningún experimento.")


class InvalidExperimentNameError(DatabaseError):
    """Raised when the supplied experiment name is not recognized.

    Attributes:
        nombre (str): The invalid experiment name provided by the user.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        super().__init__(f"Nombre de experimento inválido: '{name}' no es un ensayo válido.")


class DuplicateIdError(DatabaseError):
    """Raised when attempting to create a record with an identifier that already exists.

    Attributes:
        id (int): The duplicated identifier.
    """

    def __init__(self, duplicate_id: int):
        self.duplicate_id: int = duplicate_id
        super().__init__(f"Identificador duplicado: el id {duplicate_id} ya existe en la base de datos.")


# Backward-compatible aliases for existing Spanish API usage.
FisicaLabError = PhysicsLabError
BaseDatosError = DatabaseError
AnguloInvalidoError = InvalidAngleError
DatoNegativoError = NegativeValueError
DivisionPorCeroFisicaError = PhysicsDivisionByZeroError
DiscriminanteMenorIgualCeroFisicaError = NegativeDiscriminantError
DatosInsuficientesError = InsufficientDataError
ExperimentoNoExistenteError = ExperimentNotFoundError
NombreExperimentoIncorrecto = InvalidExperimentNameError
IdExistente = DuplicateIdError