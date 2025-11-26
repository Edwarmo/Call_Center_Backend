"""
Endpoints para el modelo Metrica.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modelos import get_db, Usuario
from esquemas import (
    MetricaCreate,
    MetricaUpdate,
    MetricaResponse,
)
from crud import (
    crear_metrica,
    obtener_metrica,
    obtener_metrica_por_fecha,
    obtener_metricas,
    actualizar_metrica,
    eliminar_metrica,
)
from auth import obtener_usuario_actual

router = APIRouter()


@router.post(
    "/",
    response_model=MetricaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva métrica",
    description="Crea una nueva métrica diaria. Valida que no exista ya una métrica para esa fecha."
)
def crear_metrica_endpoint(
    metrica: MetricaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Crea una nueva métrica."""
    try:
        return crear_metrica(db, metrica)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[MetricaResponse],
    summary="Obtener lista de métricas",
    description="Obtiene una lista de métricas con opciones de paginación y filtrado por rango de fechas."
)
def obtener_metricas_endpoint(
    skip: int = 0,
    limit: int = 100,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una lista de métricas."""
    return obtener_metricas(
        db,
        skip=skip,
        limit=limit,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )


@router.get(
    "/{metrica_id}",
    response_model=MetricaResponse,
    summary="Obtener una métrica por ID",
    description="Obtiene los detalles de una métrica específica por su ID."
)
def obtener_metrica_endpoint(
    metrica_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una métrica por su ID."""
    metrica = obtener_metrica(db, metrica_id)
    if not metrica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Métrica con ID {metrica_id} no encontrada"
        )
    return metrica


@router.get(
    "/fecha/{fecha}",
    response_model=MetricaResponse,
    summary="Obtener una métrica por fecha",
    description="Obtiene la métrica de una fecha específica (formato: YYYY-MM-DD)."
)
def obtener_metrica_por_fecha_endpoint(
    fecha: str,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una métrica por su fecha."""
    metrica = obtener_metrica_por_fecha(db, fecha)
    if not metrica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Métrica para la fecha {fecha} no encontrada"
        )
    return metrica


@router.put(
    "/{metrica_id}",
    response_model=MetricaResponse,
    summary="Actualizar una métrica",
    description="Actualiza los datos de una métrica existente. Solo se actualizan los campos proporcionados."
)
def actualizar_metrica_endpoint(
    metrica_id: int,
    metrica_update: MetricaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza una métrica."""
    try:
        metrica = actualizar_metrica(db, metrica_id, metrica_update)
        if not metrica:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Métrica con ID {metrica_id} no encontrada"
            )
        return metrica
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{metrica_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una métrica",
    description="Elimina una métrica del sistema."
)
def eliminar_metrica_endpoint(
    metrica_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Elimina una métrica."""
    eliminada = eliminar_metrica(db, metrica_id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Métrica con ID {metrica_id} no encontrada"
        )
    return None

