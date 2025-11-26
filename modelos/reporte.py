"""
Modelo para la tabla reportes.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from modelos.database import Base


class Reporte(Base):
    """
    Modelo que representa un reporte generado por un supervisor o administrador.
    """
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    generado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_generado = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    # Relaciones
    generado_por_usuario = relationship("Usuario", back_populates="reportes")

    def __repr__(self):
        return f"<Reporte(id={self.id}, generado_por={self.generado_por}, fecha_generado='{self.fecha_generado}')>"

