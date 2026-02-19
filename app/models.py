from sqlalchemy import Column, Integer, String
from .database import Base

class Incidencia(Base):
    __tablename__ = "incidencias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100))
    descripcion = Column(String(255)) # <-- Asegúrate que NO tenga tilde
    prioridad = Column(String(50))
    estado = Column(String(50))