from src.storage.experiment_repository import ExperimentRepository
from src.core.exceptions import ErrorDivisionPorCeroFisica, ErrorDiscriminanteNegativo
from src.schemas.mrua import MRUASchema

class PhysicsService:
    def __init__(self):
        self.repository = ExperimentRepository()

    def _division_segura(self, num: float, den: float, magnitud: str) -> float:
        if den == 0: raise ErrorDivisionPorCeroFisica(magnitud)
        return num / den

    def resolver_y_guardar_mru(self, nombre: str, datos: MRUASchema):
        # Rescatamos tu lógica de resolución:
        if datos.distancia is None:
            datos.distancia = datos.velocidad * datos.tiempo
        elif datos.tiempo is None:
            datos.tiempo = self._division_segura(datos.distancia, datos.velocidad, "tiempo")
        elif datos.velocidad is None:
            datos.velocidad = self._division_segura(datos.distancia, datos.tiempo, "velocidad")
        
        # Ahora usamos el repositorio para guardar en Supabase (dos tablas a la vez)
        return self.repository.create_mru_experiment(nombre, datos)


    def _resolver_tiempo_cuadratico(self, a, vi, xi, xf):
        coef_a = 0.5 * a
        coef_b = vi
        coef_c = xi - xf
        discriminante = coef_b**2 - 4 * coef_a * coef_c
        
        if discriminante < 0:
            raise ErrorDiscriminanteNegativo(discriminante)
        
        return (-coef_b + (discriminante**0.5)) / (2 * coef_a)

    def resolver_y_guardar_mrua(self, nombre: str, m: MRUASchema):
        # Aplicamos tus reglas de resolución
        if m.aceleracion is None:
            m.aceleracion = (m.velocidad_final - m.velocidad_inicial) / m.tiempo
        
        if m.posicion_final is None:
            m.posicion_final = m.posicion_inicial + (m.velocidad_inicial * m.tiempo) + (0.5 * m.aceleracion * m.tiempo**2)
            
        if m.velocidad_final is None:
            m.velocidad_final = m.velocidad_inicial + (m.aceleracion * m.tiempo)
            
        if m.tiempo is None:
            m.tiempo = self._resolver_tiempo_cuadratico(m.aceleracion, m.velocidad_inicial, m.posicion_inicial, m.posicion_final)

        # Guardar en la BD
        return self.repository.create_mrua_experiment(nombre, m.model_dump())
