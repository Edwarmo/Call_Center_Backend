"""
Modelo para la tabla clasificacion_ia.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from modelos.database import Base


class ClasificacionIA(Base):
    """
    Modelo que representa la clasificación de una llamada realizada por IA.
    
    La confianza es un valor entre 0.0 y 1.0 (porcentaje).
    """
    __tablename__ = "clasificacion_ia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    llamada_id = Column(Integer, ForeignKey("llamadas.id"), nullable=False, unique=True)
    categoria = Column(String, nullable=False)  # venta / soporte / reclamo
    confianza = Column(Float, nullable=False)  # porcentaje 0.0 - 1.0
    recomendacion_agente = Column(String, nullable=True)

    # Relaciones
    llamada = relationship("Llamada", back_populates="clasificacion_ia")

    def __repr__(self):
        return f"<ClasificacionIA(id={self.id}, llamada_id={self.llamada_id}, categoria='{self.categoria}', confianza={self.confianza})>"

