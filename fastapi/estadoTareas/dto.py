from pydantic import BaseModel
from typing import Optional

class EstadoTareaUpdate(BaseModel):
    id_estado: int  

class EstadoTareaOut(BaseModel):
    id_estado: int
    estado: str  