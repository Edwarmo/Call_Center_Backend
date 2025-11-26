"""
Modelo para la tabla usuarios.
"""

from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from modelos.database import Base


class Usuario(Base):
    """
    Modelo que representa un usuario del sistema.
    
    Roles permitidos: 'agente', 'supervisor', 'admin'
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(
        String,
        nullable=False,
        # CheckConstraint se puede agregar a nivel de tabla si es necesario
    )

    # Relaciones
    llamadas = relationship("Llamada", back_populates="usuario")
    reportes = relationship("Reporte", back_populates="generado_por_usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}', rol='{self.rol}')>"

