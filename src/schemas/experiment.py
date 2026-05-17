from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# 1. Base: Atributos comunes
class ExperimentBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre descriptivo del ensayo")
    tipo: str = Field(..., pattern="^(MRU|MRUA)$", description="Solo se permite MRU o MRUA")

# 2. Request: Lo que entra a la API (POST)
class ExperimentCreate(ExperimentBase):
    pass 

# 3. Response: Lo que sale de la API (GET) 
class ExperimentResponse(ExperimentBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True # Clave para que Pydantic entienda los datos de Supabase

# 4. Update: Para el método PATCH
class ExperimentUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)