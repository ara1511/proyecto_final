from default.defaultmodel import Base
from sqlalchemy import Column, Integer, String


class Estado(Base):
    __tablename__ = 'estados_tareas'
    id = Column(Integer, primary_key=True)
    estado = Column(String(50))
