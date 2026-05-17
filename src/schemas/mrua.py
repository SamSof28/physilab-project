from pydantic import BaseModel, field_validator
from typing import Optional
from src.core.exceptions import ErrorValorNegativo

class MRUASchema(BaseModel):
    posicion_inicial: Optional[float] = 0.0
    posicion_final: Optional[float] = None
    aceleracion: Optional[float] = None
    tiempo: Optional[float] = None
    velocidad_inicial: Optional[float] = None
    velocidad_final: Optional[float] = None

    # Ahora incluimos TODOS los campos numéricos en el validador
    @field_validator("posicion_inicial", "posicion_final", "aceleracion", 
                     "tiempo", "velocidad_inicial", "velocidad_final")
    @classmethod
    def validar_no_negativos(cls, v):
        if v is not None and v < 0:
            raise ErrorValorNegativo(v)
        return v