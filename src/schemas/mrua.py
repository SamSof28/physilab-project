from pydantic import BaseModel, field_validator
from src.core.exceptions import ErrorValorNegativo

class MRUASchema(BaseModel):
    posicion_inicial: float | None = 0.0
    posicion_final: float | None = None
    aceleracion: float | None = None
    tiempo: float | None = None
    velocidad_inicial: float | None = None
    velocidad_final: float | None = None

    @field_validator("posicion_inicial", "posicion_final", "tiempo")
    @classmethod
    def validar_no_negativos(cls, v):
        if v is not None and v < 0:
            raise ErrorValorNegativo(v)
        return v