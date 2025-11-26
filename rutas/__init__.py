"""
Rutas/Endpoints de la API del Call Center.
"""

from fastapi import APIRouter
from rutas import usuario, llamada, clasificacion_ia, metrica, reporte

# Crear el router principal
api_router = APIRouter()

# Incluir todos los routers
api_router.include_router(usuario.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(llamada.router, prefix="/llamadas", tags=["llamadas"])
api_router.include_router(
    clasificacion_ia.router,
    prefix="/clasificaciones-ia",
    tags=["clasificaciones-ia"]
)
api_router.include_router(metrica.router, prefix="/metricas", tags=["metricas"])
api_router.include_router(reporte.router, prefix="/reportes", tags=["reportes"])

