"""
Modelo para la tabla metricas.
"""

from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from modelos.database import Base


class Metrica(Base):
    """
    Modelo que representa las métricas diarias del call center.
    
    La satisfacción del cliente es una puntuación simulada entre 1-5.
    """
    __tablename__ = "metricas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(String, nullable=False)  # formato: '2025-10-20'
    total_llamadas = Column(Integer, nullable=False)
    promedio_duracion = Column(Float, nullable=False)
    satisfaccion_cliente = Column(Float, nullable=True)  # puntuación 1-5

    # Constraint único para la fecha
    __table_args__ = (
        UniqueConstraint('fecha', name='uq_metricas_fecha'),
    )

    def __repr__(self):
        return f"<Metrica(id={self.id}, fecha='{self.fecha}', total_llamadas={self.total_llamadas})>"

