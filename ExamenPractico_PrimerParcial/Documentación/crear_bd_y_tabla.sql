-- ==========================================================
-- SCRIPT SQL - ESTRUCTURA BASE DE DATOS: examen_practico
-- ==========================================================
-- Autor: Randy
-- Proyecto: Sistema de Autenticación (Examen Práctico)
-- Base de datos: MySQL
-- ==========================================================

-- 1️⃣ Crear la base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS examen_practico
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

-- 2️⃣ Usar la base creada
USE examen_practico;

-- 3️⃣ Crear tabla "usuarios"
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- 4️⃣ Insertar algunos usuarios de ejemplo (contraseñas con bcrypt)
-- ⚠️ Los hashes son de ejemplo. Sustitúyelos por los tuyos si quieres probar login real.
INSERT INTO usuarios (username, email, password_hash, activo)
VALUES
('randy_admin', 'randy_admin@example.com', '$2b$12$8kH6J2D6Ih5I0K7OjxqQMeqj8oF9k4cdkPgG9cf1hV0Dl4U9qLgHu', TRUE),
('admin02', 'admin02@example.com', '$2b$12$6sF1x9KQWUZpECP1d6A8deH7Eo7C5YxJZs5hQfH/j/CMV5r8qU7nS', TRUE),
('backup_admin', 'backup@example.com', '$2b$12$dCbe9Yoxn64cdkUu4m2nK.Ol2Z7Eo4hYF3S4z0K2rQZ8C0ZKf9vPq', TRUE);

-- 5️⃣ Verificar estructura y datos
-- Ejecuta esto en MySQL Workbench para comprobar:
-- SHOW TABLES;
-- DESCRIBE usuarios;
-- SELECT * FROM usuarios;

-- ==========================================================
-- FIN DEL SCRIPT
-- ==========================================================