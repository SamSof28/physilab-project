"""
Excepciones de dominio de la aplicación.

Estas excepciones representan errores de negocio y son independientes
de FastAPI, Supabase o cualquier otro framework. Los routers las capturan
y las convierten en respuestas HTTP apropiadas.

Jerarquia:
    AppError (base)
    |- NotFoundError    -> HTTP 404
    |- DuplicateError   -> HTTP 409
    |- ValidationError  -> HTTP 422
    +- StorageError     -> HTTP 502
"""


class AppError(Exception):
    """Clase base para todas las excepciones de dominio."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """El recurso solicitado no existe en la base de datos.

    Args:
        resource: Nombre del recurso (ej: "User", "Product").
        identifier: Identificador buscado.
    """

    def __init__(self, resource: str, identifier: int | str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} con id={identifier!r} no encontrado.")


class DuplicateError(AppError):
    """Se intenta crear un recurso que ya existe (violacion de unicidad).

    Args:
        resource: Nombre del recurso (ej: "User").
        field: Campo que viola la unicidad (ej: "email").
        value: Valor duplicado.
    """

    def __init__(self, resource: str, field: str, value: str) -> None:
        self.resource = resource
        self.field = field
        self.value = value
        super().__init__(f"{resource} con {field}={value!r} ya existe.")


class ValidationError(AppError):
    """Los datos de entrada no cumplen las reglas de negocio.

    Distinta de pydantic.ValidationError: esta refleja reglas de
    negocio (ej: precio negativo), no de formato de datos.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class StorageError(AppError):
    """Error al comunicarse con la capa de persistencia (Supabase).

    Se lanza cuando el SDK de Supabase retorna un error inesperado.
    """

    def __init__(self, operation: str, detail: str) -> None:
        self.operation = operation
        self.detail = detail
        super().__init__(
            f"Error de almacenamiento en operacion '{operation}': {detail}"
        )

# Heredamos de ValidationError porque son errores de "reglas de negocio"
class ErrorFisica(ValidationError):
    """Base para errores de cálculo físico."""
    pass

class ErrorValorNegativo(ErrorFisica):
    def __init__(self, valor: float):
        super().__init__(f"Valor inválido: {valor}. Se esperaba un valor no negativo.")

class ErrorDivisionPorCeroFisica(ErrorFisica):
    def __init__(self, magnitud: str):
        super().__init__(f"Imposible calcular '{magnitud}' con divisor cero.")

class ErrorDiscriminanteNegativo(ErrorFisica):
    def __init__(self, desc: float):
        super().__init__(f"Imposible resolver: discriminante negativo ({desc}).")