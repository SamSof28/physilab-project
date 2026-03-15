"""Capa de servicios con la lógica de negocio del laboratorio.

Este módulo contiene la clase `LaboratorioService` que valida entradas,
realiza cálculos físicos (p. ej. MRU) y delega la persistencia a
`JSONStorage`.
"""

from .exceptions import (
    ExperimentNotFoundError,
    DuplicateIdError,
    InsufficientDataError,
    PhysicsDivisionByZeroError,
    NegativeDiscriminantError,
)
from .models.mru import UniformRectilinearMotion
from .models.mrua import UniformlyAcceleratedRectilinearMotion

from .storage import JsonStorage

class LaboratoryService:
    """Servicio principal del dominio del laboratorio.

    La clase concentra la lógica de negocio para validar datos de entrada,
    resolver variables físicas faltantes (MRU y MRUA) y delegar el guardado
    de ensayos en la capa de persistencia.

    Attributes:
        storage (JsonStorage): Implementación de persistencia encargada de
            cargar y guardar la colección de ensayos.
    """

    def __init__(self, storage: JsonStorage):
        """Inicializa el servicio con la implementación de almacenamiento.

        Args:
            storage (JsonStorage): Objeto que implementa la persistencia.

        Returns:
            None: Este constructor solo inicializa el estado interno.
        """
        self.storage: JsonStorage = storage

    def _verify_unique_id(self, experiment_id: int) -> None:
        """Valida que el `ensayo_id` no exista en la base de datos.

        Args:
            experiment_id (int): Identificador del ensayo a validar.

        Raises:
            DuplicateIdError: Si el id ya existe en la base de datos.
            ExperimentNotFoundError: Si el id es inválido (<= 0).
        """
        if experiment_id <= 0:
            raise ExperimentNotFoundError(experiment_id)

        experiments = self.storage.load()
        if any(experiment.id == experiment_id for experiment in experiments):
            raise DuplicateIdError(experiment_id)
        
    def _save_experiment(self, experiment: object) -> None:
        """Agrega un ensayo a la colección persistida y guarda los cambios.

        Args:
            experiment (object): Ensayo a persistir en la base de
                datos JSON.

        Returns:
            None: El método realiza una operación de guardado sin retorno.
        """
        experiments = self.storage.load()
        experiments.append(experiment)
        self.storage.save(experiments)
            
    def _safe_divide(self, numerator: float, denominator: float, variable_name: str) -> float:
        """Realiza una división segura para fórmulas físicas.

        Args:
            numerator (float): Valor del numerador de la operación.
            denominator (float): Valor del denominador de la operación.
            variable_name (str): Nombre de la variable física que se está
                calculando; se usa para enriquecer el mensaje de error.

        Returns:
            float: Resultado de la división ``numerator / denominator``.

        Raises:
            PhysicsDivisionByZeroError: Si ``denominator`` es igual a 0.
        """
        if denominator == 0:
            raise PhysicsDivisionByZeroError(variable_name)
        
        return numerator / denominator

            
    def _solve_mru(self, mru: UniformRectilinearMotion) -> UniformRectilinearMotion:
        """Resuelve la variable faltante del MRU.

        Args:
            mru (UniformRectilinearMotion): Instancia con los parámetros
                del ensayo; uno de los campos de movimiento puede ser None.

        Returns:
            UniformRectilinearMotion: La misma instancia `mru` con el
            campo calculado completado.
        """
        if mru.distancia is None:
            mru.distancia = mru.velocidad * mru.tiempo
        elif mru.tiempo is None:
            mru.tiempo = self._safe_divide(mru.distancia, mru.velocidad, "tiempo")
        elif mru.velocidad is None:
            mru.velocidad = self._safe_divide(mru.distancia, mru.tiempo, "velocidad")
        return mru

    def calculate_mru(self, mru: UniformRectilinearMotion) -> UniformRectilinearMotion:
        """Valida, resuelve y persiste un ensayo de MRU.

        Args:
            mru (UniformRectilinearMotion): Ensayo de MRU con una variable
                faltante (distancia, tiempo o velocidad) para ser calculada.

        Returns:
            UniformRectilinearMotion: Ensayo con la variable faltante
            resuelta y persistida.

        Raises:
            ExperimentNotFoundError: Si el id del ensayo es inválido
                (menor o igual a 0).
            DuplicateIdError: Si el id del ensayo ya existe en la base.
            InsufficientDataError: Si faltan dos o más variables del MRU.
            PhysicsDivisionByZeroError: Si una fórmula requiere dividir por 0.
        """
        self._verify_unique_id(mru.id)
        
        if [mru.distancia, mru.tiempo, mru.velocidad].count(None) > 1:
            raise InsufficientDataError(1)

        mru = self._solve_mru(mru)
        
        self._save_experiment(mru)
        return mru
    
    def _solve_mrua_time(self, mrua: UniformlyAcceleratedRectilinearMotion) -> float:
        """Calcula el tiempo en un ensayo de MRUA.

        La resolución prioriza la ecuación lineal de velocidad
        (``vf = vi + a*t``). Si no se puede aplicar, utiliza la ecuación de
        posición y resuelve el caso cuadrático.

        Args:
            mrua (UniformlyAcceleratedRectilinearMotion): Ensayo de MRUA con
                información suficiente para inferir el tiempo.

        Returns:
            float: Tiempo calculado para el ensayo.

        Raises:
            NegativeDiscriminantError: Si el discriminante de la
                ecuación cuadrática es negativo.
            ZeroDivisionError: Si la forma cuadrática produce un denominador
                nulo al resolver ``2*A``.
        """
        if (mrua.velocidad_final is not None)  and (mrua.velocidad_inicial is not None) and mrua.aceleracion != 0:
            mrua.tiempo = (mrua.velocidad_final - mrua.velocidad_inicial) / mrua.aceleracion
            return mrua.tiempo

        return self._solve_quadratic_time(mrua.aceleracion, mrua.velocidad_inicial, mrua.posicion_inicial, mrua.posicion_final)
    
    def _solve_quadratic_time(self, a: float, v0: float, x0: float, xf: float) -> float:
        """Resuelve el tiempo a partir de la ecuación cuadrática de MRUA.

        Parte de la forma:
        ``xf = x0 + v0*t + 0.5*a*t^2``.

        Args:
            a (float): Aceleración del movimiento.
            v0 (float): Velocidad inicial.
            x0 (float): Posición inicial.
            xf (float): Posición final.

        Returns:
            float: Una raíz real de la ecuación (rama positiva del signo ``+``).

        Raises:
            NegativeDiscriminantError: Si el discriminante es
                menor que 0 y no existen raíces reales.
            ZeroDivisionError: Si ``A`` es 0 y la expresión divide por ``2*A``.
        """
        A = 0.5 * a
        B = v0
        C = x0 - xf

        discriminant = B**2 - 4*A*C
        if discriminant < 0:
            raise NegativeDiscriminantError(discriminant)
        
        return (-B + (discriminant ** 0.5)) / (2*A)
    
    def _solve_mrua_acceleration(self, mrua: UniformlyAcceleratedRectilinearMotion) -> float:
        """Calcula la aceleración usando velocidades y tiempo de MRUA.

        Args:
            mrua (UniformlyAcceleratedRectilinearMotion): Ensayo con tiempo,
                velocidad inicial y velocidad final disponibles.

        Returns:
            float: Aceleración calculada como ``(vf - vi) / t``.

        Raises:
            PhysicsDivisionByZeroError: Si el tiempo es 0.
        """
        if mrua.tiempo == 0:
            raise PhysicsDivisionByZeroError(mrua.tiempo)
        
        return (mrua.velocidad_final - mrua.velocidad_inicial) / mrua.tiempo

    def solve_mrua(self, mrua: UniformlyAcceleratedRectilinearMotion) -> UniformlyAcceleratedRectilinearMotion:
        """Completa variables faltantes de un ensayo MRUA in-place.

        Evalúa cada magnitud relevante y calcula solo aquellas que estén en
        ``None``: aceleración, posición final, velocidad final y tiempo.

        Args:
            mrua (UniformlyAcceleratedRectilinearMotion): Ensayo a resolver.

        Returns:
            None: Este método muta el objeto recibido directamente.

        Raises:
            PhysicsDivisionByZeroError: Si se intenta calcular aceleración con
                tiempo igual a 0.
            NegativeDiscriminantError: Si al resolver tiempo por
                cuadrática el discriminante no permite solución real.
            ZeroDivisionError: Si la resolución cuadrática divide por 0.
        """
        if mrua.aceleracion is None:
            mrua.aceleracion = self._solve_mrua_acceleration(mrua)
        if mrua.posicion_final is None:
            mrua.posicion_final = mrua.posicion_inicial + (mrua.velocidad_inicial * mrua.tiempo) + (0.5 * mrua.aceleracion * (mrua.tiempo**2))
        if mrua.velocidad_final is None:
            mrua.velocidad_final = mrua.velocidad_inicial + (mrua.aceleracion * mrua.tiempo)
        if mrua.tiempo is None:
            mrua.tiempo = self._solve_mrua_time(mrua)
        return mrua

    def _solve_mrua(self, mrua: UniformlyAcceleratedRectilinearMotion) -> UniformlyAcceleratedRectilinearMotion:
        return self.solve_mrua(mrua)


    def calculate_mrua(self, mrua: UniformlyAcceleratedRectilinearMotion) -> UniformlyAcceleratedRectilinearMotion:
        """Valida, resuelve y persiste un ensayo de MRUA.

        Args:
            mrua (UniformlyAcceleratedRectilinearMotion): Ensayo de MRUA con
                los datos necesarios para completar las variables faltantes.

        Returns:
            UniformlyAcceleratedRectilinearMotion: Ensayo resuelto y guardado.

        Raises:
            PhysicsDivisionByZeroError: Si alguna ecuación implica división
                por cero.
            NegativeDiscriminantError: Si la ecuación cuadrática
                de tiempo no tiene solución real.
            ExperimentNotFoundError: Si el id es inválido según la lógica
                de validación previa.
            DuplicateIdError: Si el id del ensayo ya existe en almacenamiento.
        """
 
        self._validate_existence_and_non_negative(mrua)

        mrua = self._solve_mrua(mrua)

        self._save_experiment(mrua)
        return mrua


    def delete_experiment(self, experiment_id: int) -> None:
        """Elimina un ensayo identificado por `ensayo_id`.

        Si no existe un ensayo con el id suministrado se lanza
        `ExperimentoNoExistenteError`.

        Args:
            experiment_id (int): Identificador del ensayo a eliminar.

        Returns:
            None: El método actualiza la base persistida sin retorno.

        Raises:
            ExperimentNotFoundError: Si no existe un ensayo con el id
                proporcionado.
        """
        experiments = self.storage.load()
        new_experiments = [experiment for experiment in experiments if experiment.id != experiment_id]

        if len(new_experiments) == len(experiments):
            raise ExperimentNotFoundError(experiment_id)

        self.storage.save(new_experiments)

