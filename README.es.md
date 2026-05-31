# web_tfg_asir

Proyecto Final de ASIR: inicio de sesión web seguro y gestión de formularios con backend en Python.

## Descripción general

Este proyecto es una aplicación web desarrollada como proyecto final de ASIR.  
Incluye una pantalla de inicio de sesión, una segunda pantalla para la gestión de formularios, un frontend construido con HTML, CSS y JavaScript, y un backend desarrollado en Python.

## Características principales

- Interfaz de inicio de sesión
- Página de formularios tras la autenticación
- Estructura frontend separada por páginas, estilos y scripts
- Backend en Python para la lógica de la aplicación
- Proyecto organizado para facilitar mantenimiento y futuras mejoras

## Estructura del proyecto

```text
WEB/
├── README.md
├── README.es.md
├── index.html
├── formularios.html
├── img/
├── script/
│   ├── script.js
│   └── formularios.js
├── style/
│   ├── style.css
│   └── formularios.css
└── back_end/
    ├── .env.example
    ├── back_end.py
    └── generar_hashes.py
```

## Tecnologías

- HTML5
- CSS3
- JavaScript
- Python (Flask, Werkzeug, MariaDB Connector, python-dotenv)

## Configuración de variables de entorno

1. **Instalar dependencias**:
   ```bash
   pip install flask werkzeug mariadb python-dotenv
   ```

2. **Configurar el archivo `.env`**:
   Copia el archivo de plantilla `.env.example` en la carpeta `back_end/` y nómbralo `.env`:
   ```bash
   cp back_end/.env.example back_end/.env
   ```
   Abre el archivo `.env` recién creado y configura tus datos de conexión a MariaDB y la clave secreta de Flask:
   ```ini
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_USER=usuario_bd
   DB_PASSWORD=contraseña_bd
   DB_DATABASE=mundoChip
   FLASK_SECRET_KEY=tu_clave_secreta_segura
   ```

## Páginas

- `index.html`: pantalla de inicio de sesión
- `formularios.html`: pantalla de gestión de formularios tras iniciar sesión

## Objetivo

El objetivo de este proyecto es construir una aplicación web estructurada y funcional como parte del proyecto final de ASIR, aplicando conceptos de desarrollo frontend y backend.

## Estado

Proyecto en desarrollo.

## Notas

Este repositorio puede seguir evolucionando con nuevas funcionalidades, mejoras de validación, integración del backend y mejoras en la interfaz.