from pydantic import BaseModel, field_validator
from typing import Optional
from src.core.exceptions import ErrorValorNegativo

class MRUSchema(BaseModel):
    distancia: Optional[float] = None
    velocidad: Optional[float] = None
    tiempo: Optional[float] = None

    @field_validator("distancia", "velocidad", "tiempo")
    @classmethod
    def validar_no_negativos(cls, v):
        if v is not None and v < 0:
            raise ErrorValorNegativo(v)
        return v