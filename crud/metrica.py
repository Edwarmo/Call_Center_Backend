"""
Operaciones CRUD para el modelo Metrica.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos import Metrica
from esquemas import MetricaCreate, MetricaUpdate


def crear_metrica(db: Session, metrica: MetricaCreate) -> Metrica:
    """
    Crea una nueva métrica en la base de datos.
    
    Args:
        db: Sesión de base de datos
        metrica: Datos de la métrica a crear
        
    Returns:
        Metrica creada
        
    Raises:
        ValueError: Si ya existe una métrica para esa fecha
    """
    # Verificar si ya existe una métrica para esa fecha
    existe = obtener_metrica_por_fecha(db, metrica.fecha)
    if existe:
        raise ValueError(f"Ya existe una métrica para la fecha {metrica.fecha}")
    
    db_metrica = Metrica(
        fecha=metrica.fecha,
        total_llamadas=metrica.total_llamadas,
        promedio_duracion=metrica.promedio_duracion,
        satisfaccion_cliente=metrica.satisfaccion_cliente
    )
    db.add(db_metrica)
    try:
        db.commit()
        db.refresh(db_metrica)
        return db_metrica
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe una métrica para la fecha {metrica.fecha}")


def obtener_metrica(db: Session, metrica_id: int) -> Optional[Metrica]:
    """
    Obtiene una métrica por su ID.
    
    Args:
        db: Sesión de base de datos
        metrica_id: ID de la métrica
        
    Returns:
        Metrica si existe, None en caso contrario
    """
    return db.query(Metrica).filter(Metrica.id == metrica_id).first()


def obtener_metrica_por_fecha(db: Session, fecha: str) -> Optional[Metrica]:
    """
    Obtiene una métrica por su fecha.
    
    Args:
        db: Sesión de base de datos
        fecha: Fecha en formato YYYY-MM-DD
        
    Returns:
        Metrica si existe, None en caso contrario
    """
    return db.query(Metrica).filter(Metrica.fecha == fecha).first()


def obtener_metricas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None
) -> List[Metrica]:
    """
    Obtiene una lista de métricas con opciones de paginación y filtrado.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        fecha_desde: Filtrar desde esta fecha (opcional, formato YYYY-MM-DD)
        fecha_hasta: Filtrar hasta esta fecha (opcional, formato YYYY-MM-DD)
        
    Returns:
        Lista de métricas ordenadas por fecha descendente
    """
    query = db.query(Metrica)
    
    if fecha_desde:
        query = query.filter(Metrica.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Metrica.fecha <= fecha_hasta)
    
    return query.order_by(Metrica.fecha.desc()).offset(skip).limit(limit).all()


def actualizar_metrica(
    db: Session,
    metrica_id: int,
    metrica_update: MetricaUpdate
) -> Optional[Metrica]:
    """
    Actualiza una métrica existente.
    
    Args:
        db: Sesión de base de datos
        metrica_id: ID de la métrica a actualizar
        metrica_update: Datos a actualizar (solo campos proporcionados)
        
    Returns:
        Metrica actualizada si existe, None en caso contrario
        
    Raises:
        ValueError: Si se intenta cambiar la fecha a una que ya existe
    """
    db_metrica = obtener_metrica(db, metrica_id)
    if not db_metrica:
        return None
    
    # Si se está actualizando la fecha, verificar que no exista otra métrica con esa fecha
    if metrica_update.fecha is not None and metrica_update.fecha != db_metrica.fecha:
        existe = obtener_metrica_por_fecha(db, metrica_update.fecha)
        if existe:
            raise ValueError(f"Ya existe una métrica para la fecha {metrica_update.fecha}")
    
    # Actualizar solo los campos proporcionados
    update_data = metrica_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_metrica, field, value)
    
    try:
        db.commit()
        db.refresh(db_metrica)
        return db_metrica
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al actualizar la métrica (posible fecha duplicada)")


def eliminar_metrica(db: Session, metrica_id: int) -> bool:
    """
    Elimina una métrica de la base de datos.
    
    Args:
        db: Sesión de base de datos
        metrica_id: ID de la métrica a eliminar
        
    Returns:
        True si se eliminó correctamente, False si no existe
    """
    db_metrica = obtener_metrica(db, metrica_id)
    if not db_metrica:
        return False
    
    db.delete(db_metrica)
    db.commit()
    return True

