# 🧩 Examen Práctico — Sistema de Autenticación

## 📘 Descripción General
Este proyecto implementa un **sistema de autenticación** en Python que utiliza **dos bases de datos**:
- **MySQL** (estructura relacional)
- **MongoDB Atlas** (base documental en la nube)

El sistema permite:
- Registrar usuarios
- Iniciar sesión
- Recuperar contraseñas
- Ver y modificar perfil
- Acceder a un **panel de administrador**
- Listar usuarios y logs de inicio de sesión

Fue desarrollado como parte del **Examen Práctico del Primer Parcial** de la asignatura *Base de Datos en la Nube*.

---

## ⚙️ Requisitos Previos
Antes de ejecutar el proyecto, asegúrate de tener instalado:

- 🐍 **Python 3.10 o superior**
- 🧠 **MongoDB Atlas** (o servidor local)
- 🐬 **MySQL Server + MySQL Workbench**
- 📦 Librerías Python requeridas:
  ```bash
  pip install bcrypt pymongo mysql-connector-python python-dotenv
  ```

---

## 📂 Estructura del Proyecto

```
ExamenPractico_PrimerParcial/
│
├── sistema_autenticacion.py   # Lógica principal (autenticación, conexión, login, registro, etc.)
├── menu_inicio.py             # Menú inicial del usuario
├── menu_principal.py          # Menú de usuario logueado
├── menu_admin.py              # Panel de administrador
│
├── crear_bd_y_tabla.sql       # Script SQL para MySQL
├── mongo_setup.js             # Script para MongoDB
├── .env.example               # Ejemplo de configuración
├── README.md                  # Documentación del proyecto
│
└── capturas/                  # Carpeta con evidencias gráficas
    ├── 01_mysql_create_db_table.png
    ├── 02_mysql_insert_users.png
    ├── 03_mongo_collections.png
    ├── 04_mongo_indexes.png
    ├── 05_app_registro.png
    ├── 06_app_login_user.png
    ├── 07_app_login_admin.png
    └── 08_app_menu_admin.png
```

---

## 🧰 Instalación y Configuración

1. **Clona o descarga el repositorio**
   ```bash
   git clone <tu_repositorio>
   cd ExamenPractico_PrimerParcial
   ```

2. **Crea y configura el archivo `.env`**
   Copia el archivo `.env.example` y renómbralo a `.env`:
   ```env
   # MongoDB Atlas
   MONGO_URI="mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net"
   MONGO_DB="examen_practico"

   # MySQL
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=tu_contraseña
   MYSQL_DATABASE=examen_practico
   ```

3. **Ejecuta los scripts de base de datos**
   - En **MySQL Workbench**: abre y ejecuta `crear_bd_y_tabla.sql`
   - En **MongoDB Atlas (Playground)**: pega y ejecuta `mongo_setup.js`

4. **Instala dependencias**
   ```bash
   pip install -r requirements.txt
   ```
   *(Si no tienes ese archivo, instala manualmente las librerías mencionadas arriba.)*

5. **Ejecuta la aplicación**
   ```bash
   python main.py
   ```

---

## 🧩 Estructura de la Base de Datos

### 🐬 MySQL — `examen_practico.usuarios`
| Campo | Tipo | Restricciones |
|--------|------|---------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| username | VARCHAR(50) | UNIQUE, NOT NULL |
| email | VARCHAR(100) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| fecha_registro | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| activo | BOOLEAN | DEFAULT TRUE |

### 🍃 MongoDB — Colección `usuarios`
```json
{
  "username": "randy123",
  "email": "randy@example.com",
  "password_hash": "$2b$12$...",
  "fecha_registro": ISODate("2025-11-10T00:00:00Z"),
  "activo": true
}
```

### 📜 Colección `logs`
Guarda los intentos de inicio de sesión (exitosos o fallidos):

```json
{
  "username": "randy123",
  "estado": "exitoso",
  "fecha": ISODate("2025-11-10T15:30:00Z")
}
```

---

## 💻 Funcionalidades Principales

### 🔐 **Menú de Inicio**
- **Iniciar sesión** (verifica usuario y contraseña)
- **Registrarse** (crea nuevo usuario con contraseña hasheada)
- **Recuperar contraseña** (simula envío de código `123456`)

### 👤 **Menú del Usuario**
- Ver su perfil
- Modificar nombre de usuario, correo o contraseña
- Volver al menú principal o cerrar sesión

### 🧑‍💼 **Menú del Administrador**
Acceso mediante código secreto `123456789`:
- Iniciar sesión con credenciales almacenadas en MySQL
- Listar usuarios (MongoDB)
- Listar administradores (MySQL)
- Ver logs de inicio de sesión

---

## 🧱 Decisiones de Diseño Tomadas

1. **Arquitectura híbrida**:  
   - MongoDB → usuarios y logs, por su flexibilidad y velocidad.  
   - MySQL → administradores, para mantener estructura y seguridad.

2. **Seguridad con bcrypt**:  
   Todas las contraseñas se almacenan en formato hasheado usando `bcrypt`.

3. **Separación de capas**:  
   - Lógica (`sistema_autenticacion.py`)  
   - Interfaz CLI (`menu_inicio.py`, `menu_admin.py`, `menu_principal.py`)  
   Esto mejora la mantenibilidad del código.

4. **Uso de `.env`**:  
   Mantiene las credenciales fuera del código fuente, cumpliendo buenas prácticas de seguridad.

5. **Índices únicos en MongoDB**:  
   Para garantizar unicidad de `username` y `email`.

---

## 🧩 Dificultades Encontradas y Soluciones

| Dificultad | Solución |
|-------------|-----------|
| `Database objects do not implement truth value testing` (MongoDB) | Cambiar `if mongo_db:` por `if mongo_db is not None:` |
| `KeyError: 'username'` | Se mezclaron campos `user` y `username`; se implementó migración en MongoDB y `.get()` en el código |
| Problemas con `getpass` | Usar `from getpass import getpass` y llamar `getpass()` directamente |
| `pip` no reconocido en Windows | Usar `python -m pip install bcrypt pymongo ...` |
| Contraseñas sin hash | Se implementó `hash_password()` con bcrypt |
| Evitar duplicados | Se agregaron índices únicos en MongoDB y restricciones UNIQUE en MySQL |

---

## 🧾 Capturas Requeridas (para el informe)

1. **Creación de BD y tabla en MySQL**
2. **Consulta `SELECT * FROM usuarios` mostrando registros**
3. **Colección `usuarios` en MongoDB Atlas**
4. **Índices únicos (`username`, `email`) en Atlas**
5. **Ejecución del registro en consola**
6. **Inicio de sesión exitoso**
7. **Inicio de sesión de administrador**
8. **Menú admin mostrando usuarios y logs**

Guárdalas en `/capturas` con nombres `01_...` a `08_...`.

---

## 🧠 Autor
**Randy Zamora**  
Estudiante — PUCE Manabí  
Asignatura: *Base de Datos en la Nube*  
Docente: *Miguelon*  

---

## 🏁 Versión
**v1.0 — Noviembre 2025**

---

> 💡 *“La seguridad no es un estado, es un proceso.”*  
> — Bruce Schneier
