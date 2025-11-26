"""
Esquemas Pydantic para el modelo ClasificacionIA.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ClasificacionIABase(BaseModel):
    """Esquema base para ClasificacionIA."""
    categoria: str = Field(..., description="Categoría: venta, soporte o reclamo")
    confianza: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza entre 0.0 y 1.0")
    recomendacion_agente: Optional[str] = Field(None, description="Recomendación generada por IA para el agente")

    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v: str) -> str:
        """Valida que la categoría sea una de las permitidas."""
        categorias_permitidas = ['venta', 'soporte', 'reclamo']
        if v.lower() not in categorias_permitidas:
            raise ValueError(f"La categoría debe ser una de: {', '.join(categorias_permitidas)}")
        return v.lower()


class ClasificacionIACreate(ClasificacionIABase):
    """Esquema para crear una nueva clasificación IA."""
    llamada_id: int = Field(..., gt=0, description="ID de la llamada asociada")


class ClasificacionIACreateAuto(BaseModel):
    """Esquema para crear una clasificación IA automáticamente (solo requiere llamada_id)."""
    llamada_id: int = Field(..., gt=0, description="ID de la llamada a clasificar automáticamente")


class ClasificacionIAUpdate(BaseModel):
    """Esquema para actualizar una clasificación IA (todos los campos son opcionales)."""
    llamada_id: Optional[int] = Field(None, gt=0)
    categoria: Optional[str] = None
    confianza: Optional[float] = Field(None, ge=0.0, le=1.0)
    recomendacion_agente: Optional[str] = None

    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v: Optional[str]) -> Optional[str]:
        """Valida que la categoría sea una de las permitidas."""
        if v is None:
            return v
        categorias_permitidas = ['venta', 'soporte', 'reclamo']
        if v.lower() not in categorias_permitidas:
            raise ValueError(f"La categoría debe ser una de: {', '.join(categorias_permitidas)}")
        return v.lower()


class ClasificacionIAResponse(ClasificacionIABase):
    """Esquema para la respuesta de una clasificación IA."""
    id: int
    llamada_id: int

    class Config:
        from_attributes = True


class ClasificacionTextoRequest(BaseModel):
    """Esquema para clasificar una llamada por su descripción textual."""
    descripcion: str = Field(..., min_length=1, description="Descripción textual de la llamada a clasificar")


class ClasificacionTextoResponse(BaseModel):
    """Esquema para la respuesta de clasificación por texto (sin guardar en BD)."""
    categoria: str = Field(..., description="Categoría clasificada: venta, soporte o reclamo")
    confianza: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza de la clasificación")
    recomendacion_agente: Optional[str] = Field(None, description="Recomendación para el agente")
    
    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v: str) -> str:
        """Valida que la categoría sea una de las permitidas."""
        categorias_permitidas = ['venta', 'soporte', 'reclamo']
        if v.lower() not in categorias_permitidas:
            raise ValueError(f"La categoría debe ser una de: {', '.join(categorias_permitidas)}")
        return v.lower()
