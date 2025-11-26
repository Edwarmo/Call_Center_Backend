"""
Esquemas Pydantic para validación y serialización de datos.
"""

from esquemas.usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioLogin,
    TokenResponse,
)
from esquemas.llamada import (
    LlamadaBase,
    LlamadaCreate,
    LlamadaUpdate,
    LlamadaResponse,
)
from esquemas.clasificacion_ia import (
    ClasificacionIABase,
    ClasificacionIACreate,
    ClasificacionIACreateAuto,
    ClasificacionIAUpdate,
    ClasificacionIAResponse,
    ClasificacionTextoRequest,
    ClasificacionTextoResponse,
)
from esquemas.metrica import (
    MetricaBase,
    MetricaCreate,
    MetricaUpdate,
    MetricaResponse,
)
from esquemas.reporte import (
    ReporteBase,
    ReporteCreate,
    ReporteUpdate,
    ReporteResponse,
)

__all__ = [
    # Usuario
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuarioLogin",
    "TokenResponse",
    # Llamada
    "LlamadaBase",
    "LlamadaCreate",
    "LlamadaUpdate",
    "LlamadaResponse",
    # ClasificacionIA
    "ClasificacionIABase",
    "ClasificacionIACreate",
    "ClasificacionIACreateAuto",
    "ClasificacionIAUpdate",
    "ClasificacionIAResponse",
    "ClasificacionTextoRequest",
    "ClasificacionTextoResponse",
    # Metrica
    "MetricaBase",
    "MetricaCreate",
    "MetricaUpdate",
    "MetricaResponse",
    # Reporte
    "ReporteBase",
    "ReporteCreate",
    "ReporteUpdate",
    "ReporteResponse",
]

