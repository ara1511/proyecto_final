from pydantic import BaseModel, Field
from typing import Optional

class UsuarioDTO(BaseModel):
    id: str
    nombre: str
    edad: int
    correo: str

class UsuarioCreateDTO(BaseModel):
    nombre: str
    edad: int
    correo: str = Field(alias="email")  # Acepta "email" como alias de "correo"

class UsuarioUpdateDTO(BaseModel):
    nombre: Optional[str]
    edad: Optional[int]
    correo: Optional[str] = Field(alias="email")  # También en la actualización

class DeleteUsuarioDTO(BaseModel):
    id: str
