"""
Esquemas Pydantic para el modelo Llamada.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator


class LlamadaBase(BaseModel):
    """Esquema base para Llamada."""
    numero_cliente: str = Field(..., min_length=1, description="Número de teléfono del cliente")
    duracion_segundos: int = Field(..., gt=0, description="Duración de la llamada en segundos")
    tipo: str = Field(..., description="Tipo de llamada: venta, soporte o reclamo")
    resultado: str = Field(..., description="Resultado: atendida, colgada, resuelta o escalada")

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        """Valida que el tipo sea uno de los permitidos."""
        tipos_permitidos = ['venta', 'soporte', 'reclamo', 'consulta', 'técnico', 'logistica']
        if v.lower() not in tipos_permitidos:
            raise ValueError(f"El tipo debe ser uno de: {', '.join(tipos_permitidos)}")
        return v.lower()

    @field_validator('resultado')
    @classmethod
    def validar_resultado(cls, v: str) -> str:
        """Valida que el resultado sea uno de los permitidos."""
        resultados_permitidos = ['atendida', 'colgada', 'resuelta', 'escalada', 'pendiente', 'fallida']
        if v.lower() not in resultados_permitidos:
            raise ValueError(f"El resultado debe ser uno de: {', '.join(resultados_permitidos)}")
        return v.lower()


class LlamadaCreate(LlamadaBase):
    """Esquema para crear una nueva llamada."""
    usuario_id: int = Field(..., gt=0, description="ID del agente que atendió la llamada")
    fecha_hora: Optional[str] = Field(
        None,
        description="Fecha y hora en formato ISO 8601. Si no se proporciona, se usa la fecha actual"
    )

    @model_validator(mode='after')
    def validar_fecha_hora(self):
        """Valida o establece la fecha_hora."""
        if self.fecha_hora is None:
            # Si no se proporciona, usar la fecha actual en formato ISO 8601
            self.fecha_hora = datetime.now().isoformat()
        else:
            # Validar que sea un formato ISO 8601 válido
            try:
                datetime.fromisoformat(self.fecha_hora.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("fecha_hora debe estar en formato ISO 8601 (ej: 2025-01-20T10:30:00)")
        return self


class LlamadaUpdate(BaseModel):
    """Esquema para actualizar una llamada (todos los campos son opcionales)."""
    usuario_id: Optional[int] = Field(None, gt=0)
    numero_cliente: Optional[str] = Field(None, min_length=1)
    duracion_segundos: Optional[int] = Field(None, gt=0)
    tipo: Optional[str] = None
    resultado: Optional[str] = None
    fecha_hora: Optional[str] = None

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el tipo sea uno de los permitidos."""
        if v is None:
            return v
        tipos_permitidos = ['venta', 'soporte', 'reclamo']
        if v.lower() not in tipos_permitidos:
            raise ValueError(f"El tipo debe ser uno de: {', '.join(tipos_permitidos)}")
        return v.lower()

    @field_validator('resultado')
    @classmethod
    def validar_resultado(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el resultado sea uno de los permitidos."""
        if v is None:
            return v
        resultados_permitidos = ['atendida', 'colgada', 'resuelta', 'escalada']
        if v.lower() not in resultados_permitidos:
            raise ValueError(f"El resultado debe ser uno de: {', '.join(resultados_permitidos)}")
        return v.lower()

    @field_validator('fecha_hora')
    @classmethod
    def validar_fecha_hora(cls, v: Optional[str]) -> Optional[str]:
        """Valida que la fecha_hora sea un formato ISO 8601 válido."""
        if v is None:
            return v
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("fecha_hora debe estar en formato ISO 8601 (ej: 2025-01-20T10:30:00)")
        return v


class LlamadaResponse(LlamadaBase):
    """Esquema para la respuesta de una llamada."""
    id: int
    usuario_id: int
    fecha_hora: str

    class Config:
        from_attributes = True

