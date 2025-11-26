# 📞 Call Center Backend API

Sistema de gestión para call centers con **FastAPI**, **SQLite** e **Inteligencia Artificial** para clasificación automática de llamadas.

## ⚡ Inicio Rápido

```bash
# 1. Clonar repositorio
git clone <url-repositorio>
cd Call_Center_Backend

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar aplicación
uvicorn main:app --reload

# 4. Acceder a la API
# http://localhost:8000/docs
```

## 🏗️ Organización del Proyecto

```
Call_Center_Backend/
├── crud/           # Operaciones CRUD (Create, Read, Update, Delete)
├── data/           # Base de datos SQLite + scripts SQL
├── esquemas/       # Validación de datos con Pydantic
├── modelos/        # Modelos de base de datos (SQLAlchemy)
├── rutas/          # Endpoints de la API REST
├── servicios/      # Lógica de negocio (IA, clasificación)
├── test/           # Pruebas y ejemplos
├── auth.py         # Autenticación JWT
├── main.py         # Aplicación principal
└── requirements.txt
```

## 🎯 Funcionalidades Específicas

### 🤖 Clasificación IA de Llamadas
- **Categorías**: Venta, Soporte, Reclamo
- **Confianza**: Nivel de certeza (0.0 - 1.0)
- **Recomendaciones**: Sugerencias automáticas para agentes
- **Fallback**: Sistema de respaldo en caso de errores

### 🔐 Sistema de Autenticación
- **JWT Tokens**: Autenticación stateless
- **Roles**: Agente, Supervisor, Admin
- **Seguridad**: Contraseñas hasheadas con bcrypt

### 📞 Gestión de Llamadas
- **Registro completo**: Duración, tipo, resultado
- **Seguimiento**: Historial por agente y cliente
- **Métricas**: Estadísticas en tiempo real

### 📊 Dashboard y Reportes
- **KPIs**: Total llamadas, duración promedio, satisfacción
- **Análisis**: Distribución por categorías
- **Exportación**: Generación automática de reportes

## 🛠️ Tecnologías

- **FastAPI**: Framework web Python
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **OpenAI API**: Modelos de lenguaje para IA
- **JWT**: Autenticación segura
- **Pydantic**: Validación de datos

## 📚 API Endpoints

### 🌐 Documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 🔐 Autenticación
```bash
# Login
POST /api/usuarios/login

# Usar token en headers
Authorization: Bearer <token-jwt>
```

### 📞 Endpoints Principales

**Usuarios**
- `GET /api/usuarios/` - Listar usuarios
- `POST /api/usuarios/` - Crear usuario
- `POST /api/usuarios/login` - Iniciar sesión

**Llamadas**
- `GET /api/llamadas/` - Listar llamadas
- `POST /api/llamadas/` - Registrar llamada
- `GET /api/llamadas/{id}` - Obtener llamada

**Clasificación IA**
- `POST /api/clasificaciones-ia/` - Clasificar llamada
- `POST /api/clasificaciones-ia/texto` - Clasificar texto

**Métricas y Reportes**
- `GET /api/metricas/` - Obtener métricas
- `GET /api/reportes/` - Listar reportes

## 🧪 Datos de Prueba

**Usuarios incluidos:**
- **Agente**: `agente1@example.com` / `123456`
- **Supervisor**: `sup@example.com` / `123456`
- **Admin**: `admin@example.com` / `123456`

**Probar IA:**
```bash
cd test
python prueba_llm.py
```

## ⚙️ Configuración IA (Opcional)

```bash
# Variables de entorno para LM Studio
export OPENAI_BASE_URL="http://127.0.0.1:1234/v1"
export OPENAI_API_KEY="lmstudio"
export OPENAI_MODEL="openai/gpt-oss-20b"
```

## 📊 Base de Datos

**Tablas:**
- `usuarios` - Gestión de usuarios y roles
- `llamadas` - Registro de llamadas
- `clasificacion_ia` - Resultados de IA
- `metricas` - Datos del dashboard
- `reportes` - Reportes generados