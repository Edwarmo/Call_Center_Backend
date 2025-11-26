"""
Operaciones CRUD para el modelo Reporte.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from modelos import Reporte, Usuario
from esquemas import ReporteCreate, ReporteUpdate


def crear_reporte(db: Session, reporte: ReporteCreate) -> Reporte:
    """
    Crea un nuevo reporte en la base de datos.
    
    Args:
        db: Sesión de base de datos
        reporte: Datos del reporte a crear
        
    Returns:
        Reporte creado
        
    Raises:
        ValueError: Si el usuario_id no existe
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == reporte.generado_por).first()
    if not usuario:
        raise ValueError(f"El usuario con ID {reporte.generado_por} no existe")
    
    db_reporte = Reporte(
        generado_por=reporte.generado_por,
        fecha_generado=reporte.fecha_generado,
        descripcion=reporte.descripcion
    )
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte


def obtener_reporte(db: Session, reporte_id: int) -> Optional[Reporte]:
    """
    Obtiene un reporte por su ID.
    
    Args:
        db: Sesión de base de datos
        reporte_id: ID del reporte
        
    Returns:
        Reporte si existe, None en caso contrario
    """
    return db.query(Reporte).filter(Reporte.id == reporte_id).first()


def obtener_reportes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    generado_por: Optional[int] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None
) -> List[Reporte]:
    """
    Obtiene una lista de reportes con opciones de paginación y filtrado.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        generado_por: Filtrar por usuario que generó el reporte (opcional)
        fecha_desde: Filtrar desde esta fecha (opcional, formato ISO 8601)
        fecha_hasta: Filtrar hasta esta fecha (opcional, formato ISO 8601)
        
    Returns:
        Lista de reportes ordenados por fecha descendente
    """
    query = db.query(Reporte)
    
    if generado_por:
        query = query.filter(Reporte.generado_por == generado_por)
    if fecha_desde:
        query = query.filter(Reporte.fecha_generado >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Reporte.fecha_generado <= fecha_hasta)
    
    return query.order_by(Reporte.fecha_generado.desc()).offset(skip).limit(limit).all()


def obtener_reportes_por_usuario(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Reporte]:
    """
    Obtiene todos los reportes generados por un usuario específico.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        
    Returns:
        Lista de reportes del usuario
    """
    return obtener_reportes(db, skip=skip, limit=limit, generado_por=usuario_id)


def actualizar_reporte(
    db: Session,
    reporte_id: int,
    reporte_update: ReporteUpdate
) -> Optional[Reporte]:
    """
    Actualiza un reporte existente.
    
    Args:
        db: Sesión de base de datos
        reporte_id: ID del reporte a actualizar
        reporte_update: Datos a actualizar (solo campos proporcionados)
        
    Returns:
        Reporte actualizado si existe, None en caso contrario
        
    Raises:
        ValueError: Si el usuario_id proporcionado no existe
    """
    db_reporte = obtener_reporte(db, reporte_id)
    if not db_reporte:
        return None
    
    # Verificar que el usuario existe si se está actualizando generado_por
    if reporte_update.generado_por is not None:
        usuario = db.query(Usuario).filter(Usuario.id == reporte_update.generado_por).first()
        if not usuario:
            raise ValueError(f"El usuario con ID {reporte_update.generado_por} no existe")
    
    # Actualizar solo los campos proporcionados
    update_data = reporte_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reporte, field, value)
    
    db.commit()
    db.refresh(db_reporte)
    return db_reporte


def eliminar_reporte(db: Session, reporte_id: int) -> bool:
    """
    Elimina un reporte de la base de datos.
    
    Args:
        db: Sesión de base de datos
        reporte_id: ID del reporte a eliminar
        
    Returns:
        True si se eliminó correctamente, False si no existe
    """
    db_reporte = obtener_reporte(db, reporte_id)
    if not db_reporte:
        return False
    
    db.delete(db_reporte)
    db.commit()
    return True

