"""
Módulo de autenticación con JWT.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from modelos import get_db, Usuario

SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion"  # En producción, usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/usuarios/login",
    scheme_name="Bearer"
)


def verificar_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada (string o bytes)
        
    Returns:
        True si coinciden, False en caso contrario
    """
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    
    return bcrypt.checkpw(plain_password, hashed_password)


def obtener_password_hash(password: str) -> str:
    """
    Genera el hash de una contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash de la contraseña como string
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    
    return hashed.decode('utf-8')


def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT de acceso.
    
    Args:
        data: Datos a incluir en el token (normalmente usuario_id, email, rol)
        expires_delta: Tiempo de expiración del token. Si es None, usa el valor por defecto.
        
    Returns:
        Token JWT codificado como string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Asegurarse de que siempre retorne un string
    if isinstance(encoded_jwt, bytes):
        return encoded_jwt.decode('utf-8')
    return encoded_jwt


def verificar_token(token: str) -> dict:
    """
    Verifica y decodifica un token JWT.
    
    Args:
        token: Token JWT a verificar
        
    Returns:
        Payload del token decodificado
        
    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    try:
        # Asegurarse de que el token sea un string
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: claims incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido. Inicie sesión nuevamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia de FastAPI para obtener el usuario actual autenticado.
    
    Esta función se puede usar como dependencia en los endpoints para proteger rutas.
    
    Args:
        token: Token JWT obtenido del header Authorization
        db: Sesión de base de datos
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    payload = verificar_token(token)
    usuario_id_str = payload.get("sub")
    
    if usuario_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        usuario_id = int(usuario_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: ID de usuario inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return usuario


def obtener_usuario_actual_opcional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    """
    Dependencia opcional para obtener el usuario actual.
    Útil cuando algunas rutas pueden funcionar con o sin autenticación.
    
    Args:
        token: Token JWT (opcional)
        db: Sesión de base de datos
        
    Returns:
        Usuario si está autenticado, None en caso contrario
    """
    try:
        if token:
            return obtener_usuario_actual(token, db)
    except HTTPException:
        pass
    return None

