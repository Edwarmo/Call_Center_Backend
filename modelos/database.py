"""
Configuración de la base de datos SQLite.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ruta a la base de datos
DATABASE_URL = "sqlite:///./data/db.db"

# Crear el motor de la base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite
    echo=False  # Cambiar a True para ver las consultas SQL
)

# Crear la clase base para los modelos
Base = declarative_base()

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Generador de dependencias para obtener una sesión de base de datos.
    Útil para FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

