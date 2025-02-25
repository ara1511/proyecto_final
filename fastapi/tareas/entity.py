import uuid
from typing import Optional
from datetime import date
from sqlalchemy.orm import relationship
from default.defaultmodel import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String, ForeignKey('usuarios.id'))
    tarea = Column(String(100))  
    fecha = Column(Date)
    id_estado = Column(Integer, ForeignKey('estados_tareas.id'))

usuario = relationship("Usuario", back_populates="tareas")

estado = relationship("Estado", back_populates="tareas")