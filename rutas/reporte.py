"""
Endpoints para el modelo Reporte.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modelos import get_db, Usuario
from esquemas import (
    ReporteCreate,
    ReporteUpdate,
    ReporteResponse,
)
from crud import (
    crear_reporte,
    obtener_reporte,
    obtener_reportes,
    obtener_reportes_por_usuario,
    actualizar_reporte,
    eliminar_reporte,
)
from auth import obtener_usuario_actual

router = APIRouter()


@router.post(
    "/",
    response_model=ReporteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo reporte",
    description="Crea un nuevo reporte. Valida que el usuario que genera el reporte exista."
)
def crear_reporte_endpoint(
    reporte: ReporteCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Crea un nuevo reporte."""
    try:
        return crear_reporte(db, reporte)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[ReporteResponse],
    summary="Obtener lista de reportes",
    description="Obtiene una lista de reportes con opciones de paginación y filtrado."
)
def obtener_reportes_endpoint(
    skip: int = 0,
    limit: int = 100,
    generado_por: Optional[int] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una lista de reportes."""
    return obtener_reportes(
        db,
        skip=skip,
        limit=limit,
        generado_por=generado_por,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )


@router.get(
    "/{reporte_id}",
    response_model=ReporteResponse,
    summary="Obtener un reporte por ID",
    description="Obtiene los detalles de un reporte específico por su ID."
)
def obtener_reporte_endpoint(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene un reporte por su ID."""
    reporte = obtener_reporte(db, reporte_id)
    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte con ID {reporte_id} no encontrado"
        )
    return reporte


@router.get(
    "/usuario/{usuario_id}",
    response_model=List[ReporteResponse],
    summary="Obtener reportes de un usuario",
    description="Obtiene todos los reportes generados por un usuario específico."
)
def obtener_reportes_por_usuario_endpoint(
    usuario_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene todos los reportes de un usuario."""
    return obtener_reportes_por_usuario(db, usuario_id, skip=skip, limit=limit)


@router.put(
    "/{reporte_id}",
    response_model=ReporteResponse,
    summary="Actualizar un reporte",
    description="Actualiza los datos de un reporte existente. Solo se actualizan los campos proporcionados."
)
def actualizar_reporte_endpoint(
    reporte_id: int,
    reporte_update: ReporteUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza un reporte."""
    try:
        reporte = actualizar_reporte(db, reporte_id, reporte_update)
        if not reporte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reporte con ID {reporte_id} no encontrado"
            )
        return reporte
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{reporte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un reporte",
    description="Elimina un reporte del sistema."
)
def eliminar_reporte_endpoint(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Elimina un reporte."""
    eliminado = eliminar_reporte(db, reporte_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reporte con ID {reporte_id} no encontrado"
        )
    return None

