from src.storage.experiment_repository import ExperimentRepository
from src.core.exceptions import ErrorDivisionPorCeroFisica, ErrorDiscriminanteNegativo
from src.schemas.mru import MRUSchema
from src.schemas.mrua import MRUASchema
from src.schemas.experiment import ExperimentCreate

class PhysicsService:
    def __init__(self):
        # El servicio "contrata" al repositorio para persistir datos
        self.repository = ExperimentRepository()

    def _division_segura(self, num: float, den: float, magnitud: str) -> float:
        if den == 0: 
            raise ErrorDivisionPorCeroFisica(magnitud)
        return num / den

    def resolver_y_guardar_mru(self, nombre: str, datos: MRUSchema):
        # 1. Lógica de resolución física
        if datos.distancia is None:
            datos.distancia = datos.velocidad * datos.tiempo
        elif datos.tiempo is None:
            datos.tiempo = self._division_segura(datos.distancia, datos.velocidad, "tiempo")
        elif datos.velocidad is None:
            datos.velocidad = self._division_segura(datos.distancia, datos.tiempo, "velocidad")
        
        # 2. ALINEACIÓN: Creamos el contrato de "Experimento Maestro"
        # Esto soluciona el error que marcó Copilot
        exp_maestro = ExperimentCreate(nombre=nombre, tipo="MRU")
        
        # 3. Guardar enviando el objeto maestro y el diccionario de física
        return self.repository.create_mru_experiment(exp_maestro, datos.model_dump())

    def _resolver_tiempo_cuadratico(self, a, vi, xi, xf):
        coef_a = 0.5 * a
        coef_b = vi
        coef_c = xi - xf
        discriminante = coef_b**2 - 4 * coef_a * coef_c
        
        if discriminante < 0:
            raise ErrorDiscriminanteNegativo(discriminante)
        
        return (-coef_b + (discriminante**0.5)) / (2 * coef_a)

    def resolver_y_guardar_mrua(self, nombre: str, m: MRUASchema):
        # 1. Lógica de resolución MRUA
        if m.aceleracion is None and m.tiempo is not None:
            m.aceleracion = (m.velocidad_final - m.velocidad_inicial) / m.tiempo
        
        if m.posicion_final is None and m.tiempo is not None:
            m.posicion_final = m.posicion_inicial + (m.velocidad_inicial * m.tiempo) + (0.5 * m.aceleracion * m.tiempo**2)
            
        if m.velocidad_final is None and m.aceleracion is not None and m.tiempo is not None:
            m.velocidad_final = m.velocidad_inicial + (m.aceleracion * m.tiempo)
            
        if m.tiempo is None:
            m.tiempo = self._resolver_tiempo_cuadratico(m.aceleracion, m.velocidad_inicial, m.posicion_inicial, m.posicion_final)
            if m.velocidad_final is None and m.aceleracion is not None:
                m.velocidad_final = m.velocidad_inicial + (m.aceleracion * m.tiempo)

        # 2. Crear contrato maestro para MRUA
        exp_maestro = ExperimentCreate(nombre=nombre, tipo="MRUA")

        # 3. Guardar
        return self.repository.create_mrua_experiment(exp_maestro, m.model_dump())
    
    def list_all(self):
        return self.repository.get_all()

    def get_one(self, exp_id: int):
        return self.repository.get_by_id(exp_id)

    def remove_one(self, exp_id: int) -> bool:
        return self.repository.delete(exp_id)