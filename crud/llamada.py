"""
Operaciones CRUD para el modelo Llamada.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from modelos import Llamada, Usuario
from esquemas import LlamadaCreate, LlamadaUpdate


def crear_llamada(db: Session, llamada: LlamadaCreate) -> Llamada:
    """
    Crea una nueva llamada en la base de datos.
    
    Args:
        db: Sesión de base de datos
        llamada: Datos de la llamada a crear
        
    Returns:
        Llamada creada
        
    Raises:
        ValueError: Si el usuario_id no existe
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == llamada.usuario_id).first()
    if not usuario:
        raise ValueError(f"El usuario con ID {llamada.usuario_id} no existe")
    
    db_llamada = Llamada(
        usuario_id=llamada.usuario_id,
        numero_cliente=llamada.numero_cliente,
        duracion_segundos=llamada.duracion_segundos,
        tipo=llamada.tipo,
        resultado=llamada.resultado,
        fecha_hora=llamada.fecha_hora
    )
    db.add(db_llamada)
    db.commit()
    db.refresh(db_llamada)
    return db_llamada


def obtener_llamada(db: Session, llamada_id: int) -> Optional[Llamada]:
    """
    Obtiene una llamada por su ID.
    
    Args:
        db: Sesión de base de datos
        llamada_id: ID de la llamada
        
    Returns:
        Llamada si existe, None en caso contrario
    """
    return db.query(Llamada).filter(Llamada.id == llamada_id).first()


def obtener_llamadas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    usuario_id: Optional[int] = None,
    tipo: Optional[str] = None,
    resultado: Optional[str] = None
) -> List[Llamada]:
    """
    Obtiene una lista de llamadas con opciones de paginación y filtrado.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        usuario_id: Filtrar por usuario (opcional)
        tipo: Filtrar por tipo de llamada (opcional)
        resultado: Filtrar por resultado (opcional)
        
    Returns:
        Lista de llamadas
    """
    query = db.query(Llamada)
    
    if usuario_id:
        query = query.filter(Llamada.usuario_id == usuario_id)
    if tipo:
        query = query.filter(Llamada.tipo == tipo)
    if resultado:
        query = query.filter(Llamada.resultado == resultado)
    
    return query.order_by(Llamada.fecha_hora.desc()).offset(skip).limit(limit).all()


def obtener_llamadas_por_usuario(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Llamada]:
    """
    Obtiene todas las llamadas de un usuario específico.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        
    Returns:
        Lista de llamadas del usuario
    """
    return obtener_llamadas(db, skip=skip, limit=limit, usuario_id=usuario_id)


def actualizar_llamada(
    db: Session,
    llamada_id: int,
    llamada_update: LlamadaUpdate
) -> Optional[Llamada]:
    """
    Actualiza una llamada existente.
    
    Args:
        db: Sesión de base de datos
        llamada_id: ID de la llamada a actualizar
        llamada_update: Datos a actualizar (solo campos proporcionados)
        
    Returns:
        Llamada actualizada si existe, None en caso contrario
        
    Raises:
        ValueError: Si el usuario_id proporcionado no existe
    """
    db_llamada = obtener_llamada(db, llamada_id)
    if not db_llamada:
        return None
    
    # Verificar que el usuario existe si se está actualizando usuario_id
    if llamada_update.usuario_id is not None:
        usuario = db.query(Usuario).filter(Usuario.id == llamada_update.usuario_id).first()
        if not usuario:
            raise ValueError(f"El usuario con ID {llamada_update.usuario_id} no existe")
    
    # Actualizar solo los campos proporcionados
    update_data = llamada_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_llamada, field, value)
    
    db.commit()
    db.refresh(db_llamada)
    return db_llamada


def eliminar_llamada(db: Session, llamada_id: int) -> bool:
    """
    Elimina una llamada de la base de datos.
    
    Args:
        db: Sesión de base de datos
        llamada_id: ID de la llamada a eliminar
        
    Returns:
        True si se eliminó correctamente, False si no existe
    """
    db_llamada = obtener_llamada(db, llamada_id)
    if not db_llamada:
        return False
    
    db.delete(db_llamada)
    db.commit()
    return True

