-- ==========================================
-- BASE DE DATOS CALL CENTER (SQLite)
-- DATOS DE PRUEBA COMPLETOS
-- ==========================================

PRAGMA foreign_keys = ON;

-- -------------------------
-- Tabla de usuarios (ya creada por ti)
-- -------------------------
--INSERT INTO usuarios (nombre, email, password, rol)
--VALUES
--('Agente 1', 'agente1@example.com', '123456', 'agente'),
--('Supervisor', 'sup@example.com', '123456', 'supervisor'),
--('Administrador', 'admin@example.com', '123456', 'admin');

-- -------------------------
-- TABLA: llamadas
-- -------------------------
INSERT INTO llamadas (usuario_id, numero_cliente, duracion_segundos, tipo, resultado, fecha_hora)
VALUES
(1, '3204567890', 180, 'venta', 'resuelta', '2025-01-12T09:15:00'),
(1, '3112345678', 95, 'soporte', 'atendida', '2025-01-12T10:22:00'),
(1, '3156789098', 210, 'reclamo', 'escalada', '2025-01-12T11:05:00'),
(2, '3229988776', 300, 'venta', 'resuelta', '2025-01-13T08:40:00'),
(1, '3001122334', 45, 'soporte', 'colgada', '2025-01-13T14:21:00'),
(2, '3045566778', 130, 'reclamo', 'resuelta', '2025-01-14T16:02:00'),
(1, '3118899001', 260, 'venta', 'resuelta', '2025-01-15T09:55:00'),
(1, '3224455667', 190, 'soporte', 'escalada', '2025-01-15T10:33:00');

-- -------------------------
-- TABLA: clasificacion_ia
-- (IDs de llamadas asumidos del 1 al 8)
-- -------------------------
INSERT INTO clasificacion_ia (llamada_id, categoria, confianza, recomendacion_agente)
VALUES
(1, 'venta', 0.92, 'Ofrecer plan premium con descuento del 10%'),
(2, 'soporte', 0.88, 'Guiar al cliente a reiniciar el módem de Claro'),
(3, 'reclamo', 0.81, 'Escalar a supervisor por tono alterado'),
(4, 'venta', 0.95, 'Enviar enlace de pago por WhatsApp'),
(5, 'soporte', 0.77, 'Verificar cobertura en zona rural de Pitalito'),
(6, 'reclamo', 0.89, 'Registrar PQR y confirmar número de radicado'),
(7, 'venta', 0.93, 'Cerrar venta con oferta 2x1 en datos'),
(8, 'soporte', 0.85, 'Solicitar captura de pantalla del error');

-- -------------------------
-- TABLA: metricas
-- -------------------------
INSERT INTO metricas (fecha, total_llamadas, promedio_duracion, satisfaccion_cliente)
VALUES
('2025-01-12', 35, 145.3, 4.2),
('2025-01-13', 28, 162.8, 3.9),
('2025-01-14', 31, 150.1, 4.5),
('2025-01-15', 40, 170.6, 4.1),
('2025-01-16', 22, 120.4, 3.8);

-- -------------------------
-- TABLA: reportes
-- (generado_por corresponde a supervisor=2 o admin=3)
-- -------------------------
INSERT INTO reportes (generado_por, fecha_generado, descripcion)
VALUES
(2, '2025-01-15T18:30:00', 'Reporte diario de desempeño – turno mañana'),
(3, '2025-01-16T08:45:00', 'Resumen de métricas semanales'),
(2, '2025-01-17T17:20:00', 'Análisis de reclamos por ciudades: Bogotá, Medellín y Cali'),
(3, '2025-01-18T09:10:00', 'Informe de ventas cerradas por agentes'),
(2, '2025-01-18T19:40:00', 'Consolidado de llamadas críticas del día');
