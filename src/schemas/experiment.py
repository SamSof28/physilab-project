from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Modelo base para lo que se guarda en la tabla 'experimentos'
class ExperimentBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    tipo: str  # 'MRU' o 'MRUA'

class ExperimentCreate(ExperimentBase):
    pass # Lo que enviamos desde Streamlit para crear

class Experiment(ExperimentBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True # Permite leer datos desde diccionarios de Supabase