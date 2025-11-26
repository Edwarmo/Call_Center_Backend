"""
Operaciones CRUD para el modelo Usuario.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos import Usuario
from esquemas import UsuarioCreate, UsuarioUpdate
from auth import obtener_password_hash

def crear_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        db: Sesión de base de datos
        usuario: Datos del usuario a crear
        
    Returns:
        Usuario creado
        
    Raises:
        IntegrityError: Si el email ya existe
    """
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=obtener_password_hash(usuario.password),
        rol=usuario.rol
    )
    db.add(db_usuario)
    try:
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        raise ValueError(f"El email {usuario.email} ya está registrado")


def obtener_usuario(db: Session, usuario_id: int) -> Optional[Usuario]:
    """
    Obtiene un usuario por su ID.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario
        
    Returns:
        Usuario si existe, None en caso contrario
    """
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def obtener_usuario_por_email(db: Session, email: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por su email.
    
    Args:
        db: Sesión de base de datos
        email: Email del usuario
        
    Returns:
        Usuario si existe, None en caso contrario
    """
    return db.query(Usuario).filter(Usuario.email == email).first()


def obtener_usuarios(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    rol: Optional[str] = None
) -> List[Usuario]:
    """
    Obtiene una lista de usuarios con opciones de paginación y filtrado.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        rol: Filtrar por rol (opcional)
        
    Returns:
        Lista de usuarios
    """
    query = db.query(Usuario)
    
    if rol:
        query = query.filter(Usuario.rol == rol)
    
    return query.offset(skip).limit(limit).all()


def actualizar_usuario(
    db: Session,
    usuario_id: int,
    usuario_update: UsuarioUpdate
) -> Optional[Usuario]:
    """
    Actualiza un usuario existente.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario a actualizar
        usuario_update: Datos a actualizar (solo campos proporcionados)
        
    Returns:
        Usuario actualizado si existe, None en caso contrario
    """
    db_usuario = obtener_usuario(db, usuario_id)
    if not db_usuario:
        return None
    
    # Actualizar solo los campos proporcionados
    update_data = usuario_update.model_dump(exclude_unset=True)
    # Si se actualiza la contraseña, hashearla
    if "password" in update_data:
        from auth import obtener_password_hash
        update_data["password"] = obtener_password_hash(update_data["password"])
    for field, value in update_data.items():
        setattr(db_usuario, field, value)
    
    try:
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al actualizar el usuario (posible email duplicado)")


def eliminar_usuario(db: Session, usuario_id: int) -> bool:
    """
    Elimina un usuario de la base de datos.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario a eliminar
        
    Returns:
        True si se eliminó correctamente, False si no existe
    """
    db_usuario = obtener_usuario(db, usuario_id)
    if not db_usuario:
        return False
    
    db.delete(db_usuario)
    db.commit()
    return True

