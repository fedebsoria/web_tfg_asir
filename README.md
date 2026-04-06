```
# 🌐 MundoChip - Web Sales App

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-11.x-orange.svg)](https://mariadb.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/tuusuario/mundochip)

**App web completa para gestión de ventas con autenticación segura y persistencia en MariaDB.**

## 🚀 Demo
```
Login → Formulario ventas → Guardado con pedido_id → Persistencia BD
```
- **Login**: Usuarios con hash scrypt (Werkzeug)
- **Ventas**: Productos reales de MariaDB, líneas agrupadas por pedido_id
- **Seguridad**: Sesiones Flask, validación FK, queries parametrizadas

## 🛠️ Tech Stack
```
Frontend: HTML5/CSS3/JavaScript (estilo retro-pixel)
Backend: Flask 3.0 + Werkzeug Security
Database: MariaDB 11.x (mundoChip schema)
Deployment: Nginx + UFW + Cloudflared (Ubuntu 24.04)
```

## 📁 Estructura
```
web/
├── index.html           # Login screen
├── formularios.html     # Sales form
├── back_end/
│   └── back_end.py      # Flask API + auth
│   └── generar_hashes.py # Creates users with hashed password
├── style/               # CSS (retro theme)
├── script/              # JS (form handling)
├── img/                 # Assets
└── assets/fonts/        # Custom fonts
```

## 🗄️ Database Schema
```
usuarios: id, user_name, password (scrypt hashes)
productos: id, nombre_producto, precio_recomendado, activo
ventas: pedido_id, producto_id, cantidad, precio_unitario, usuario_id
```

## 🎯 Features
- ✅ Secure login (Werkzeug scrypt)
- ✅ Real-time product loading from DB
- ✅ Multi-line sales (pedido_id grouping)
- ✅ JSON API with validation
- ✅ Session protection
- ✅ Transaction safety (commit/rollback)
- ✅ Error handling

## 🚀 Quick Start (Dev)

1. **Install dependencies**
```bash
pip install flask werkzeug mariadb
```

2. **Config DB_CONFIG** (back_end.py)
```python
DB_CONFIG = {
    "user": "DB_USER",
    "password": "DB_PASSWORD",
    "database": "DB_NAME"
}
```

3. **Run**
```bash
cd web
python back_end/back_end.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🖥️ Production Deployment
```
Ubuntu 24.04 → Nginx → Flask (gunicorn) → MariaDB → UFW → Cloudflared
```

## 🔧 Fixed Issues
- Jinja rendering (Flask only)
- Duplicate login() function
- Session management
- DB credentials
- Werkzeug hash truncation
- Static file serving

## 📈 Commit History
```
feat: complete Flask + MariaDB backend
feat: secure login with scrypt hashes
fix: static routes (style/script/img)
```

## 📄 License
MIT License - see [LICENSE](LICENSE)

---