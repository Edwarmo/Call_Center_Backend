"""
Operaciones CRUD para el modelo ClasificacionIA.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos import ClasificacionIA, Llamada
from esquemas import ClasificacionIACreate, ClasificacionIAUpdate


def crear_clasificacion_ia(
    db: Session,
    clasificacion: ClasificacionIACreate
) -> ClasificacionIA:
    """
    Crea una nueva clasificación IA en la base de datos.
    
    Args:
        db: Sesión de base de datos
        clasificacion: Datos de la clasificación a crear
        
    Returns:
        ClasificacionIA creada
        
    Raises:
        ValueError: Si la llamada no existe o ya tiene una clasificación
    """
    # Verificar que la llamada existe
    llamada = db.query(Llamada).filter(Llamada.id == clasificacion.llamada_id).first()
    if not llamada:
        raise ValueError(f"La llamada con ID {clasificacion.llamada_id} no existe")
    
    # Verificar que la llamada no tenga ya una clasificación
    existe = obtener_clasificacion_ia_por_llamada(db, clasificacion.llamada_id)
    if existe:
        raise ValueError(f"La llamada con ID {clasificacion.llamada_id} ya tiene una clasificación IA")
    
    db_clasificacion = ClasificacionIA(
        llamada_id=clasificacion.llamada_id,
        categoria=clasificacion.categoria,
        confianza=clasificacion.confianza,
        recomendacion_agente=clasificacion.recomendacion_agente
    )
    db.add(db_clasificacion)
    try:
        db.commit()
        db.refresh(db_clasificacion)
        return db_clasificacion
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al crear la clasificación IA (posible llamada_id duplicado)")


def obtener_clasificacion_ia(
    db: Session,
    clasificacion_id: int
) -> Optional[ClasificacionIA]:
    """
    Obtiene una clasificación IA por su ID.
    
    Args:
        db: Sesión de base de datos
        clasificacion_id: ID de la clasificación
        
    Returns:
        ClasificacionIA si existe, None en caso contrario
    """
    return db.query(ClasificacionIA).filter(ClasificacionIA.id == clasificacion_id).first()


def obtener_clasificacion_ia_por_llamada(
    db: Session,
    llamada_id: int
) -> Optional[ClasificacionIA]:
    """
    Obtiene la clasificación IA de una llamada específica.
    
    Args:
        db: Sesión de base de datos
        llamada_id: ID de la llamada
        
    Returns:
        ClasificacionIA si existe, None en caso contrario
    """
    return db.query(ClasificacionIA).filter(ClasificacionIA.llamada_id == llamada_id).first()


def obtener_clasificaciones_ia(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    confianza_minima: Optional[float] = None
) -> List[ClasificacionIA]:
    """
    Obtiene una lista de clasificaciones IA con opciones de paginación y filtrado.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        categoria: Filtrar por categoría (opcional)
        confianza_minima: Filtrar por confianza mínima (opcional)
        
    Returns:
        Lista de clasificaciones IA
    """
    query = db.query(ClasificacionIA)
    
    if categoria:
        query = query.filter(ClasificacionIA.categoria == categoria)
    if confianza_minima is not None:
        query = query.filter(ClasificacionIA.confianza >= confianza_minima)
    
    return query.order_by(ClasificacionIA.confianza.desc()).offset(skip).limit(limit).all()


def actualizar_clasificacion_ia(
    db: Session,
    clasificacion_id: int,
    clasificacion_update: ClasificacionIAUpdate
) -> Optional[ClasificacionIA]:
    """
    Actualiza una clasificación IA existente.
    
    Args:
        db: Sesión de base de datos
        clasificacion_id: ID de la clasificación a actualizar
        clasificacion_update: Datos a actualizar (solo campos proporcionados)
        
    Returns:
        ClasificacionIA actualizada si existe, None en caso contrario
        
    Raises:
        ValueError: Si la llamada_id proporcionada no existe
    """
    db_clasificacion = obtener_clasificacion_ia(db, clasificacion_id)
    if not db_clasificacion:
        return None
    
    # Verificar que la llamada existe si se está actualizando llamada_id
    if clasificacion_update.llamada_id is not None:
        llamada = db.query(Llamada).filter(Llamada.id == clasificacion_update.llamada_id).first()
        if not llamada:
            raise ValueError(f"La llamada con ID {clasificacion_update.llamada_id} no existe")
    
    # Actualizar solo los campos proporcionados
    update_data = clasificacion_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_clasificacion, field, value)
    
    try:
        db.commit()
        db.refresh(db_clasificacion)
        return db_clasificacion
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al actualizar la clasificación IA (posible llamada_id duplicado)")


def eliminar_clasificacion_ia(db: Session, clasificacion_id: int) -> bool:
    """
    Elimina una clasificación IA de la base de datos.
    
    Args:
        db: Sesión de base de datos
        clasificacion_id: ID de la clasificación a eliminar
        
    Returns:
        True si se eliminó correctamente, False si no existe
    """
    db_clasificacion = obtener_clasificacion_ia(db, clasificacion_id)
    if not db_clasificacion:
        return False
    
    db.delete(db_clasificacion)
    db.commit()
    return True

