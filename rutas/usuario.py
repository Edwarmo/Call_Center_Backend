"""
Endpoints para el modelo Usuario.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from modelos import get_db, Usuario
from esquemas import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioLogin,
    TokenResponse,
)
from crud import (
    crear_usuario,
    obtener_usuario,
    obtener_usuario_por_email,
    obtener_usuarios,
    actualizar_usuario,
    eliminar_usuario,
)
from auth import (
    verificar_password,
    crear_access_token,
    obtener_usuario_actual,
)

router = APIRouter()


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Crea un nuevo usuario en el sistema. El email debe ser único."
)
def crear_usuario_endpoint(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo usuario."""
    try:
        return crear_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[UsuarioResponse],
    summary="Obtener lista de usuarios",
    description="Obtiene una lista de usuarios con opciones de paginación y filtrado por rol. Requiere autenticación."
)
def obtener_usuarios_endpoint(
    skip: int = 0,
    limit: int = 100,
    rol: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene una lista de usuarios."""
    return obtener_usuarios(db, skip=skip, limit=limit, rol=rol)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Obtener un usuario por ID",
    description="Obtiene los detalles de un usuario específico por su ID. Requiere autenticación."
)
def obtener_usuario_endpoint(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene un usuario por su ID."""
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    return usuario


@router.get(
    "/email/{email}",
    response_model=UsuarioResponse,
    summary="Obtener un usuario por email",
    description="Obtiene los detalles de un usuario específico por su email. Requiere autenticación."
)
def obtener_usuario_por_email_endpoint(
    email: str,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Obtiene un usuario por su email."""
    usuario = obtener_usuario_por_email(db, email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con email {email} no encontrado"
        )
    return usuario


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Actualizar un usuario",
    description="Actualiza los datos de un usuario existente. Solo se actualizan los campos proporcionados. Requiere autenticación."
)
def actualizar_usuario_endpoint(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza un usuario."""
    try:
        usuario = actualizar_usuario(db, usuario_id, usuario_update)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
    description="Elimina un usuario del sistema. Requiere autenticación."
)
def eliminar_usuario_endpoint(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Elimina un usuario."""
    eliminado = eliminar_usuario(db, usuario_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    return None


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login de usuario",
    description="Autentica un usuario con email y contraseña. Retorna un token JWT para usar en las siguientes peticiones. Usa el formato OAuth2 estándar (username=email, password=contraseña)."
)
def login_usuario(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica un usuario y retorna un token JWT.
    
    Nota: En Swagger UI, usa 'username' para el email y 'password' para la contraseña.
    """
    # OAuth2PasswordRequestForm usa 'username' en lugar de 'email'
    usuario = obtener_usuario_por_email(db, form_data.username)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    if not verificar_password(form_data.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    access_token = crear_access_token(data={"sub": str(usuario.id), "email": usuario.email, "rol": usuario.rol})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        usuario=UsuarioResponse.model_validate(usuario)
    )

