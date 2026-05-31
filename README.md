
# 🌐 MundoChip - Web Sales App

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-11.x-orange.svg)](https://mariadb.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://github.com/tuusuario/mundochip)

**Complete web app for sales management with secure authentication and persistence in MariaDB.**

## 🚀 Demo
```
Login → Sales Form → Saved with order_id → Database Persistence
```
- **Login**: Users with scrypt hash (Werkzeug)
- **Sales**: Actual MariaDB products, lines grouped by order_id
- **Security**: Flask sessions, FK validation, parameterized queries

## 🛠️ Tech Stack
```
Frontend: HTML5/CSS3/JavaScript (estilo retro-pixel)
Backend: Flask 3.0 + Werkzeug Security
Database: MariaDB 11.x (mundoChip schema)
Deployment: Nginx + UFW + Cloudflared (Ubuntu 24.04)
```

## 📁 Structure
```
web/
├── index.html           # Login screen
├── formularios.html     # Sales form
├── back_end/
│   ├── .env.example     # Template for environment variables
│   ├── back_end.py      # Flask API + auth
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
pip install flask werkzeug mariadb python-dotenv
```

2. **Configure Environment Variables**
Copy the template `.env.example` file to `.env` in the `back_end/` directory and configure your credentials:
```bash
cp back_end/.env.example back_end/.env
```
Inside `back_end/.env`, fill in your database and Flask configuration:
```ini
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_DATABASE=mundoChip
FLASK_SECRET_KEY=your_secure_session_key
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