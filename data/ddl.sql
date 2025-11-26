-- ==========================================
-- BASE DE DATOS CALL CENTER (SQLite)
-- Versión simple para estudiantes
-- ==========================================

PRAGMA foreign_keys = ON;

-- -------------------------
-- Tabla de usuarios
-- -------------------------
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('agente', 'supervisor', 'admin'))
);

-- -------------------------
-- Tabla de llamadas
-- -------------------------
CREATE TABLE llamadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,          -- agente que atendió la llamada
    numero_cliente TEXT NOT NULL,
    duracion_segundos INTEGER NOT NULL,
    tipo TEXT NOT NULL,                   -- venta, soporte, reclamo
    resultado TEXT NOT NULL,              -- atendida, colgada, resuelta, escalada
    fecha_hora TEXT NOT NULL,             -- formato ISO 8601

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- -------------------------
-- Tabla de clasificación con IA
-- -------------------------
CREATE TABLE clasificacion_ia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    llamada_id INTEGER NOT NULL,
    categoria TEXT NOT NULL,             -- venta / soporte / reclamo
    confianza REAL NOT NULL,             -- porcentaje 0.0 - 1.0
    recomendacion_agente TEXT,           -- sugerencia generada por IA

    FOREIGN KEY (llamada_id) REFERENCES llamadas(id)
);

-- -------------------------
-- Tabla de métricas (dashboard)
-- -------------------------
CREATE TABLE metricas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,                 -- ejemplo: '2025-10-20'
    total_llamadas INTEGER NOT NULL,
    promedio_duracion REAL NOT NULL,
    satisfaccion_cliente REAL,           -- puntuación simulada 1-5

    UNIQUE (fecha)
);

-- -------------------------
-- Tabla para reportes generados
-- -------------------------
CREATE TABLE reportes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generado_por INTEGER NOT NULL,       -- supervisor o admin
    fecha_generado TEXT NOT NULL,
    descripcion TEXT,

    FOREIGN KEY (generado_por) REFERENCES usuarios(id)
);

-- DATOS DE PRUEBA
INSERT INTO usuarios (nombre, email, password, rol)
VALUES
('Agente 1', 'agente1@example.com', '123456', 'agente'),
('Supervisor', 'sup@example.com', '123456', 'supervisor'),
('Administrador', 'admin@example.com', '123456', 'admin');
