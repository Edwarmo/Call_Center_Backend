"""
Modelo para la tabla llamadas.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from modelos.database import Base


class Llamada(Base):
    """
    Modelo que representa una llamada atendida en el call center.
    
    Tipos permitidos: 'venta', 'soporte', 'reclamo'
    Resultados permitidos: 'atendida', 'colgada', 'resuelta', 'escalada'
    """
    __tablename__ = "llamadas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    numero_cliente = Column(String, nullable=False)
    duracion_segundos = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)  # venta, soporte, reclamo
    resultado = Column(String, nullable=False)  # atendida, colgada, resuelta, escalada
    fecha_hora = Column(String, nullable=False)  # formato ISO 8601

    # Relaciones
    usuario = relationship("Usuario", back_populates="llamadas")
    clasificacion_ia = relationship("ClasificacionIA", back_populates="llamada", uselist=False)

    def __repr__(self):
        return f"<Llamada(id={self.id}, usuario_id={self.usuario_id}, tipo='{self.tipo}', resultado='{self.resultado}')>"

