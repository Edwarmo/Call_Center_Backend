"""
Operaciones CRUD para interactuar con los modelos de la base de datos.
"""

from crud.usuario import (
    crear_usuario,
    obtener_usuario,
    obtener_usuario_por_email,
    obtener_usuarios,
    actualizar_usuario,
    eliminar_usuario,
)
from crud.llamada import (
    crear_llamada,
    obtener_llamada,
    obtener_llamadas,
    obtener_llamadas_por_usuario,
    actualizar_llamada,
    eliminar_llamada,
)
from crud.clasificacion_ia import (
    crear_clasificacion_ia,
    obtener_clasificacion_ia,
    obtener_clasificacion_ia_por_llamada,
    obtener_clasificaciones_ia,
    actualizar_clasificacion_ia,
    eliminar_clasificacion_ia,
)
from crud.metrica import (
    crear_metrica,
    obtener_metrica,
    obtener_metrica_por_fecha,
    obtener_metricas,
    actualizar_metrica,
    eliminar_metrica,
)
from crud.reporte import (
    crear_reporte,
    obtener_reporte,
    obtener_reportes,
    obtener_reportes_por_usuario,
    actualizar_reporte,
    eliminar_reporte,
)

__all__ = [
    # Usuario
    "crear_usuario",
    "obtener_usuario",
    "obtener_usuario_por_email",
    "obtener_usuarios",
    "actualizar_usuario",
    "eliminar_usuario",
    # Llamada
    "crear_llamada",
    "obtener_llamada",
    "obtener_llamadas",
    "obtener_llamadas_por_usuario",
    "actualizar_llamada",
    "eliminar_llamada",
    # ClasificacionIA
    "crear_clasificacion_ia",
    "obtener_clasificacion_ia",
    "obtener_clasificacion_ia_por_llamada",
    "obtener_clasificaciones_ia",
    "actualizar_clasificacion_ia",
    "eliminar_clasificacion_ia",
    # Metrica
    "crear_metrica",
    "obtener_metrica",
    "obtener_metrica_por_fecha",
    "obtener_metricas",
    "actualizar_metrica",
    "eliminar_metrica",
    # Reporte
    "crear_reporte",
    "obtener_reporte",
    "obtener_reportes",
    "obtener_reportes_por_usuario",
    "actualizar_reporte",
    "eliminar_reporte",
]

