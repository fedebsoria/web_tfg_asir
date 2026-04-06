from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from werkzeug.security import check_password_hash
import mariadb
from pathlib import Path
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR),
    static_folder=None
)

# Secret key for session signing during development.
# I can move this to an environment variable later for production.
app.secret_key = "clave_super_segura_para_sesiones_2026"

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "DB_USER", # < --- CHANGE THIS. PUT THE ACTUAL USER OF THE DB.
    "database": "DB_USER_PASSWORD" # < -- CHANGE THIS. PUT THE USER'S DB PASSWORD.
}


def get_connection():
    # Open a new MariaDB connection every time I need database access.
    return mariadb.connect(**DB_CONFIG)


def fetch_active_products():
    # Load only active products so the form never shows disabled items.
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nombre_producto, precio_recomendado
            FROM productos
            WHERE activo = 1
            ORDER BY nombre_producto
            """
        )
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def verify_user(user_name, password):
    # Check if the username exists and validate the Werkzeug hash.
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, user_name, password
            FROM usuarios
            WHERE user_name = ?
            LIMIT 1
            """,
            (user_name,)
        )
        user = cursor.fetchone()

        if not user:
            return None

        if check_password_hash(user["password"], password):
            return {
                "id": user["id"],
                "user_name": user["user_name"]
            }

        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def login_required():
    # Simple helper to keep protected routes behind a valid session.
    return "user_id" in session


@app.route("/style/<path:filename>")
def style_files(filename):
    return send_from_directory(BASE_DIR / "style", filename)


@app.route("/script/<path:filename>")
def script_files(filename):
    return send_from_directory(BASE_DIR / "script", filename)


@app.route("/img/<path:filename>")
def img_files(filename):
    return send_from_directory(BASE_DIR / "img", filename)


@app.route("/assets/<path:filename>")
def assets_files(filename):
    return send_from_directory(BASE_DIR / "assets", filename)


@app.get("/")
def home():
    # Send the root URL to the login screen.
    return redirect(url_for("login"))


@app.route("/index", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def login():
    # Handle both the login form render and the login submit in one place.
    if request.method == "POST":
        user_name = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not user_name or not password:
            return render_template("index.html", error="Usuario y contraseña requeridos")

        user = verify_user(user_name, password)

        if not user:
            return render_template("index.html", error="Credenciales incorrectas")

        session["user_id"] = user["id"]
        session["user_name"] = user["user_name"]
        return redirect(url_for("formularios"))

    return render_template("index.html")


@app.get("/logout")
def logout():
    # Clear the current session and go back to the login page.
    session.clear()
    return redirect(url_for("login"))


@app.get("/formularios")
def formularios():
    # Block direct access if the user is not logged in yet.
    if not login_required():
        return redirect(url_for("login"))

    productos = fetch_active_products()
    return render_template(
        "formularios.html",
        productos=productos,
        user_id=session.get("user_id"),
        user_name=session.get("user_name")
    )


@app.post("/api/ventas")
def guardar_venta():
    # Save one order with one or more product lines using the same pedido_id.
    if not login_required():
        return jsonify({"ok": False, "mensaje": "Sesión no válida."}), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"ok": False, "mensaje": "No se recibieron datos JSON."}), 400

    productos = data.get("productos", [])
    comentarios = (data.get("comentarios") or "").strip()
    usuario_id = session.get("user_id")

    if not isinstance(productos, list) or not productos:
        return jsonify({"ok": False, "mensaje": "Debes enviar al menos un producto válido."}), 400

    pedido_id = str(uuid4())
    conn = None
    cursor = None

    try:
        conn = get_connection()
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)

        lineas_guardadas = []
        total_pedido = 0.0

        for index, item in enumerate(productos, start=1):
            producto_id = item.get("producto_id")
            cantidad = item.get("cantidad")
            precio_unitario = item.get("precio_unitario")

            try:
                producto_id = int(producto_id)
                cantidad = int(cantidad)
                precio_unitario = float(precio_unitario)
            except (TypeError, ValueError):
                raise ValueError(f"Datos inválidos en la línea {index}.")

            if cantidad < 1:
                raise ValueError(f"La cantidad de la línea {index} debe ser mayor que cero.")

            if precio_unitario < 0:
                raise ValueError(f"El precio de la línea {index} no puede ser negativo.")

            cursor.execute(
                """
                SELECT id, nombre_producto, activo
                FROM productos
                WHERE id = ?
                """,
                (producto_id,)
            )
            producto_db = cursor.fetchone()

            if not producto_db:
                raise ValueError(f"El producto de la línea {index} no existe.")

            if int(producto_db["activo"]) != 1:
                raise ValueError(f"El producto de la línea {index} está inactivo.")

            cursor.execute(
                """
                INSERT INTO ventas
                (pedido_id, producto_id, cantidad, precio_unitario, comentarios, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    pedido_id,
                    producto_id,
                    cantidad,
                    precio_unitario,
                    comentarios if comentarios else None,
                    usuario_id
                )
            )

            subtotal = round(cantidad * precio_unitario, 2)
            total_pedido += subtotal

            lineas_guardadas.append({
                "producto_id": producto_id,
                "producto": producto_db["nombre_producto"],
                "cantidad": cantidad,
                "precio_unitario": round(precio_unitario, 2),
                "subtotal": subtotal
            })

        conn.commit()

        return jsonify({
            "ok": True,
            "mensaje": "Venta guardada correctamente.",
            "pedido_id": pedido_id,
            "lineas": lineas_guardadas,
            "total_pedido": round(total_pedido, 2),
            "user_name": session.get("user_name")
        }), 201

    except ValueError as error:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": str(error)}), 400

    except mariadb.Error as error:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": f"Error de base de datos: {error}"}), 500

    except Exception as error:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": f"Error interno: {error}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    # Debug mode is useful while I am still finishing the project.
    app.run(debug=True, host="127.0.0.1", port=5000)