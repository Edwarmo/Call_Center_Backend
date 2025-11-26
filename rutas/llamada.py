"""
Endpoints para el modelo Llamada.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modelos import get_db, Usuario
from esquemas import (
    LlamadaCreate,
    LlamadaUpdate,
    LlamadaResponse,
)
from crud import (
    crear_llamada,
    obtener_llamada,
    obtener_llamadas,
    obtener_llamadas_por_usuario,
    actualizar_llamada,
    eliminar_llamada,
)
from auth import obtener_usuario_actual

router = APIRouter()


@router.post(
    "/",
    response_model=LlamadaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva llamada",
    description="Registra una nueva llamada en el sistema. Valida que el usuario_id exista."
)
def crear_llamada_endpoint(
    llamada: LlamadaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Crea una nueva llamada."""
    try:
        return crear_llamada(db, llamada)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[LlamadaResponse],
    summary="Obtener lista de llamadas",
    description="Obtiene una lista de llamadas con opciones de paginación y filtrado."
)
def obtener_llamadas_endpoint(
    skip: int = 0,
    limit: int = 100,
    usuario_id: Optional[int] = None,
    tipo: Optional[str] = None,
    resultado: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una lista de llamadas."""
    return obtener_llamadas(
        db,
        skip=skip,
        limit=limit,
        usuario_id=usuario_id,
        tipo=tipo,
        resultado=resultado
    )


@router.get(
    "/{llamada_id}",
    response_model=LlamadaResponse,
    summary="Obtener una llamada por ID",
    description="Obtiene los detalles de una llamada específica por su ID."
)
def obtener_llamada_endpoint(
    llamada_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una llamada por su ID."""
    llamada = obtener_llamada(db, llamada_id)
    if not llamada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Llamada con ID {llamada_id} no encontrada"
        )
    return llamada


@router.get(
    "/usuario/{usuario_id}",
    response_model=List[LlamadaResponse],
    summary="Obtener llamadas de un usuario",
    description="Obtiene todas las llamadas atendidas por un usuario específico."
)
def obtener_llamadas_por_usuario_endpoint(
    usuario_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene todas las llamadas de un usuario."""
    return obtener_llamadas_por_usuario(db, usuario_id, skip=skip, limit=limit)


@router.put(
    "/{llamada_id}",
    response_model=LlamadaResponse,
    summary="Actualizar una llamada",
    description="Actualiza los datos de una llamada existente. Solo se actualizan los campos proporcionados."
)
def actualizar_llamada_endpoint(
    llamada_id: int,
    llamada_update: LlamadaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza una llamada."""
    try:
        llamada = actualizar_llamada(db, llamada_id, llamada_update)
        if not llamada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Llamada con ID {llamada_id} no encontrada"
            )
        return llamada
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{llamada_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una llamada",
    description="Elimina una llamada del sistema."
)
def eliminar_llamada_endpoint(
    llamada_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Elimina una llamada."""
    eliminada = eliminar_llamada(db, llamada_id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Llamada con ID {llamada_id} no encontrada"
        )
    return None

