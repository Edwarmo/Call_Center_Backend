"""
Esquemas Pydantic para el modelo Reporte.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator


class ReporteBase(BaseModel):
    """Esquema base para Reporte."""
    descripcion: Optional[str] = Field(None, description="Descripción del reporte")


class ReporteCreate(ReporteBase):
    """Esquema para crear un nuevo reporte."""
    generado_por: int = Field(..., gt=0, description="ID del usuario que genera el reporte")
    fecha_generado: Optional[str] = Field(
        None,
        description="Fecha de generación en formato ISO 8601. Si no se proporciona, se usa la fecha actual"
    )

    @model_validator(mode='after')
    def validar_fecha_generado(self):
        """Valida o establece la fecha_generado."""
        if self.fecha_generado is None:
            # Si no se proporciona, usar la fecha actual en formato ISO 8601
            self.fecha_generado = datetime.now().isoformat()
        else:
            # Validar que sea un formato ISO 8601 válido
            try:
                datetime.fromisoformat(self.fecha_generado.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("fecha_generado debe estar en formato ISO 8601 (ej: 2025-01-20T10:30:00)")
        return self


class ReporteUpdate(BaseModel):
    """Esquema para actualizar un reporte (todos los campos son opcionales)."""
    generado_por: Optional[int] = Field(None, gt=0)
    fecha_generado: Optional[str] = None
    descripcion: Optional[str] = None

    @field_validator('fecha_generado')
    @classmethod
    def validar_fecha_generado(cls, v: Optional[str]) -> Optional[str]:
        """Valida que la fecha_generado sea un formato ISO 8601 válido."""
        if v is None:
            return v
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("fecha_generado debe estar en formato ISO 8601 (ej: 2025-01-20T10:30:00)")
        return v


class ReporteResponse(ReporteBase):
    """Esquema para la respuesta de un reporte."""
    id: int
    generado_por: int
    fecha_generado: str

    class Config:
        from_attributes = True

