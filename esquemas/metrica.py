"""
Esquemas Pydantic para el modelo Metrica.
"""

from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, field_validator


class MetricaBase(BaseModel):
    """Esquema base para Metrica."""
    fecha: str = Field(..., description="Fecha en formato YYYY-MM-DD")
    total_llamadas: int = Field(..., ge=0, description="Total de llamadas del día")
    promedio_duracion: float = Field(..., ge=0.0, description="Promedio de duración en segundos")
    satisfaccion_cliente: Optional[float] = Field(
        None,
        ge=1.0,
        le=5.0,
        description="Puntuación de satisfacción del cliente (1-5)"
    )

    @field_validator('fecha')
    @classmethod
    def validar_fecha(cls, v: str) -> str:
        """Valida que la fecha esté en formato YYYY-MM-DD."""
        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD (ej: 2025-01-20)")
        return v


class MetricaCreate(MetricaBase):
    """Esquema para crear una nueva métrica."""
    pass


class MetricaUpdate(BaseModel):
    """Esquema para actualizar una métrica (todos los campos son opcionales)."""
    fecha: Optional[str] = None
    total_llamadas: Optional[int] = Field(None, ge=0)
    promedio_duracion: Optional[float] = Field(None, ge=0.0)
    satisfaccion_cliente: Optional[float] = Field(None, ge=1.0, le=5.0)

    @field_validator('fecha')
    @classmethod
    def validar_fecha(cls, v: Optional[str]) -> Optional[str]:
        """Valida que la fecha esté en formato YYYY-MM-DD."""
        if v is None:
            return v
        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD (ej: 2025-01-20)")
        return v


class MetricaResponse(MetricaBase):
    """Esquema para la respuesta de una métrica."""
    id: int

    class Config:
        from_attributes = True

