from pydantic import BaseModel, field_validator
from src.core.exceptions import ErrorValorNegativo

class MRUSchema(BaseModel):
    distancia: float | None = None
    velocidad: float | None = None
    tiempo: float | None = None

    @field_validator("distancia", "velocidad", "tiempo")
    @classmethod
    def validar_no_negativos(cls, v):
        if v is not None and v < 0:
            raise ErrorValorNegativo(v)
        return v