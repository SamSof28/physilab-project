class ErrorAplicacion(Exception):
    """Excepción base para todos los errores del dominio."""


class ErrorFisicaLaboratorio(ErrorAplicacion):
    """Errores relacionados con cálculos físicos o validación de entradas."""


class ErrorBaseDatos(ErrorAplicacion):
    """Errores relacionados con operaciones de persistencia y registros."""


class ErrorAnguloInvalido(ErrorFisicaLaboratorio):
    """Se lanza cuando el ángulo ingresado no es válido."""

    def __init__(self, angulo: float) -> None:
        self.angulo: float = angulo
        super().__init__(f"Ángulo inválido: el valor {angulo}° no es aceptable.")


class ErrorValorNegativo(ErrorFisicaLaboratorio):
    """Se lanza cuando un valor que debe ser no negativo es negativo."""

    def __init__(self, valor: float) -> None:
        self.valor: float = valor
        super().__init__(f"Valor inválido: {valor}. Se esperaba un valor no negativo.")


class ErrorDivisionPorCeroFisica(ErrorFisicaLaboratorio):
    """Se lanza cuando un cálculo físico intentaría dividir por cero."""

    def __init__(self, magnitud: str):
        self.magnitud = magnitud
        super().__init__(f"Error matemático: imposible calcular '{magnitud}' con divisor igual a cero.")


class ErrorDiscriminanteNegativo(ErrorFisicaLaboratorio):
    """Se lanza cuando el discriminante de una ecuación es menor que cero."""

    def __init__(self, discriminante: float):
        self.discriminante: float = discriminante
        super().__init__(
            f"Error matemático: imposible resolver con discriminante menor a cero ({discriminante})."
        )


class ErrorDatosInsuficientes(ErrorFisicaLaboratorio):
    """Se lanza cuando no hay suficientes datos para realizar un cálculo."""

    def __init__(self, cantidad_faltante: int = 1) -> None:
        self.cantidad_faltante: int = cantidad_faltante
        plural = "dato" if cantidad_faltante == 1 else "datos"
        super().__init__(
            f"Datos insuficientes: faltan {cantidad_faltante} {plural} para completar el cálculo."
        )


class ErrorExperimentoNoEncontrado(ErrorBaseDatos):
    """Se lanza cuando el identificador no existe en los registros."""

    def __init__(self, id_experimento: int) -> None:
        self.id_experimento = id_experimento
        super().__init__(
            f"Identificador inválido: el id {id_experimento} no corresponde a ningún experimento."
        )


class ErrorNombreExperimentoInvalido(ErrorBaseDatos):
    """Se lanza cuando el tipo de experimento no es reconocido."""

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        super().__init__(f"Nombre de experimento inválido: '{nombre}' no es un ensayo válido.")


class ErrorIdDuplicado(ErrorBaseDatos):
    """Se lanza cuando se intenta registrar un ID que ya existe."""

    def __init__(self, id_duplicado: int):
        self.id_duplicado: int = id_duplicado
        super().__init__(f"Identificador duplicado: el id {id_duplicado} ya existe en la base de datos.")
