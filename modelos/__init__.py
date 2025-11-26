"""
Modelos para la base de datos del Call Center.
"""

from modelos.database import Base, engine, SessionLocal, get_db
from modelos.usuario import Usuario
from modelos.llamada import Llamada
from modelos.clasificacion_ia import ClasificacionIA
from modelos.metrica import Metrica
from modelos.reporte import Reporte

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "Usuario",
    "Llamada",
    "ClasificacionIA",
    "Metrica",
    "Reporte",
]

