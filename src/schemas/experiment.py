from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ExperimentBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    tipo: str  # 'MRU' o 'MRUA'

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentResponse(ExperimentBase):
    id: int
    fecha_creacion: datetime

    # Corrección del Warning: Sintaxis moderna de Pydantic V2
    model_config = ConfigDict(from_attributes=True)