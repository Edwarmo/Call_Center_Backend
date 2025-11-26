"""
Esquemas Pydantic para el modelo Usuario.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioBase(BaseModel):
    """Esquema base para Usuario."""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email único del usuario")
    rol: str = Field(..., description="Rol del usuario: agente, supervisor o admin")

    @field_validator('rol')
    @classmethod
    def validar_rol(cls, v: str) -> str:
        """Valida que el rol sea uno de los permitidos."""
        roles_permitidos = ['agente', 'supervisor', 'admin']
        if v.lower() not in roles_permitidos:
            raise ValueError(f"El rol debe ser uno de: {', '.join(roles_permitidos)}")
        return v.lower()


class UsuarioCreate(UsuarioBase):
    """Esquema para crear un nuevo usuario."""
    password: str = Field(..., min_length=6, description="Contraseña del usuario (mínimo 6 caracteres)")


class UsuarioUpdate(BaseModel):
    """Esquema para actualizar un usuario (todos los campos son opcionales)."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    rol: Optional[str] = None

    @field_validator('rol')
    @classmethod
    def validar_rol(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el rol sea uno de los permitidos."""
        if v is None:
            return v
        roles_permitidos = ['agente', 'supervisor', 'admin']
        if v.lower() not in roles_permitidos:
            raise ValueError(f"El rol debe ser uno de: {', '.join(roles_permitidos)}")
        return v.lower()


class UsuarioResponse(UsuarioBase):
    """Esquema para la respuesta de un usuario (sin incluir password)."""
    id: int

    class Config:
        from_attributes = True  # Permite crear desde ORM models (antes orm_mode)


class UsuarioLogin(BaseModel):
    """Esquema para el login de un usuario."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Esquema para la respuesta del login con token."""
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse

