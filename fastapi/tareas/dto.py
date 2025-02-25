from pydantic import BaseModel
from typing import Optional
from datetime import date

class TareaDTO(BaseModel):
    id: str
    usuario_id: str
    tarea: str
    fecha: date
    id_estado: int

class TareaCreateDTO(BaseModel):
    usuario_id: Optional[str]
    tarea: str
    fecha: date
    id_estado: Optional[int]

class TareaUpdateDTO(BaseModel):
    usuario_id: Optional[str]
    tarea: Optional[str]
    fecha: Optional[date]
    id_estado: Optional[int]

class DeleteTareaDTO(BaseModel):
    id: str