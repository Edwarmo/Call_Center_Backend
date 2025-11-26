"""
Endpoints para el modelo ClasificacionIA.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modelos import get_db, Usuario
from esquemas import (
    ClasificacionIACreate,
    ClasificacionIACreateAuto,
    ClasificacionIAUpdate,
    ClasificacionIAResponse,
    ClasificacionTextoRequest,
    ClasificacionTextoResponse,
)
from crud import (
    crear_clasificacion_ia,
    obtener_clasificacion_ia,
    obtener_clasificacion_ia_por_llamada,
    obtener_clasificaciones_ia,
    actualizar_clasificacion_ia,
    eliminar_clasificacion_ia,
)
from crud.llamada import obtener_llamada
from auth import obtener_usuario_actual
from servicios.clasificacion_ia import clasificar_llamada_con_ia, clasificar_texto_llamada

router = APIRouter()


@router.post(
    "/clasificar-texto",
    response_model=ClasificacionTextoResponse,
    summary="Clasificar una llamada por descripción textual",
    description="Clasifica una llamada basándose únicamente en su descripción textual. No guarda la clasificación en la base de datos, solo retorna el resultado."
)
def clasificar_texto_endpoint(
    request: ClasificacionTextoRequest,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Clasifica una llamada basándose en su descripción textual usando IA.
    Esta función no guarda la clasificación, solo la retorna.
    """
    try:
        resultado = clasificar_texto_llamada(request.descripcion)
        
        return ClasificacionTextoResponse(
            categoria=resultado["categoria"],
            confianza=resultado["confianza"],
            recomendacion_agente=resultado["recomendacion_agente"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al clasificar el texto: {str(e)}"
        )


@router.post(
    "/",
    response_model=ClasificacionIAResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva clasificación IA automáticamente",
    description="Clasifica automáticamente una llamada usando IA. Solo requiere el ID de la llamada. La clasificación se genera automáticamente basándose en las características de la llamada."
)
def crear_clasificacion_ia_endpoint(
    clasificacion_auto: ClasificacionIACreateAuto,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Crea una nueva clasificación IA automáticamente usando el LLM.
    Solo requiere el llamada_id, el resto se genera automáticamente.
    """
    try:
        # Obtener la llamada
        llamada = obtener_llamada(db, clasificacion_auto.llamada_id)
        if not llamada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La llamada con ID {clasificacion_auto.llamada_id} no existe"
            )
        
        # Verificar que la llamada no tenga ya una clasificación
        existe = obtener_clasificacion_ia_por_llamada(db, clasificacion_auto.llamada_id)
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La llamada con ID {clasificacion_auto.llamada_id} ya tiene una clasificación IA"
            )
        
        # Clasificar usando IA
        resultado_ia = clasificar_llamada_con_ia(
            tipo_llamada=llamada.tipo,
            resultado_llamada=llamada.resultado,
            numero_cliente=llamada.numero_cliente,
            duracion_segundos=llamada.duracion_segundos
        )
        
        # Crear la clasificación con los resultados de la IA
        clasificacion = ClasificacionIACreate(
            llamada_id=clasificacion_auto.llamada_id,
            categoria=resultado_ia["categoria"],
            confianza=resultado_ia["confianza"],
            recomendacion_agente=resultado_ia["recomendacion_agente"]
        )
        
        return crear_clasificacion_ia(db, clasificacion)
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al clasificar la llamada: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[ClasificacionIAResponse],
    summary="Obtener lista de clasificaciones IA",
    description="Obtiene una lista de clasificaciones IA con opciones de paginación y filtrado."
)
def obtener_clasificaciones_ia_endpoint(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    confianza_minima: Optional[float] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una lista de clasificaciones IA."""
    return obtener_clasificaciones_ia(
        db,
        skip=skip,
        limit=limit,
        categoria=categoria,
        confianza_minima=confianza_minima
    )


@router.get(
    "/{clasificacion_id}",
    response_model=ClasificacionIAResponse,
    summary="Obtener una clasificación IA por ID",
    description="Obtiene los detalles de una clasificación IA específica por su ID."
)
def obtener_clasificacion_ia_endpoint(
    clasificacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una clasificación IA por su ID."""
    clasificacion = obtener_clasificacion_ia(db, clasificacion_id)
    if not clasificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clasificación IA con ID {clasificacion_id} no encontrada"
        )
    return clasificacion


@router.get(
    "/llamada/{llamada_id}",
    response_model=ClasificacionIAResponse,
    summary="Obtener clasificación IA de una llamada",
    description="Obtiene la clasificación IA asociada a una llamada específica."
)
def obtener_clasificacion_ia_por_llamada_endpoint(
    llamada_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene la clasificación IA de una llamada."""
    clasificacion = obtener_clasificacion_ia_por_llamada(db, llamada_id)
    if not clasificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clasificación IA para la llamada con ID {llamada_id} no encontrada"
        )
    return clasificacion


@router.put(
    "/{clasificacion_id}",
    response_model=ClasificacionIAResponse,
    summary="Actualizar una clasificación IA",
    description="Actualiza los datos de una clasificación IA existente. Solo se actualizan los campos proporcionados."
)
def actualizar_clasificacion_ia_endpoint(
    clasificacion_id: int,
    clasificacion_update: ClasificacionIAUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza una clasificación IA."""
    try:
        clasificacion = actualizar_clasificacion_ia(db, clasificacion_id, clasificacion_update)
        if not clasificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clasificación IA con ID {clasificacion_id} no encontrada"
            )
        return clasificacion
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{clasificacion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una clasificación IA",
    description="Elimina una clasificación IA del sistema."
)
def eliminar_clasificacion_ia_endpoint(
    clasificacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Elimina una clasificación IA."""
    eliminada = eliminar_clasificacion_ia(db, clasificacion_id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clasificación IA con ID {clasificacion_id} no encontrada"
        )
    return None

