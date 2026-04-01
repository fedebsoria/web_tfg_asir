from flask import Flask, render_template, request, jsonify, redirect, url_for
import mariadb
from pathlib import Path
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR),
    static_folder=str(BASE_DIR),
    static_url_path=""
)

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "TU_USUARIO_MARIADB",
    "password": "TU_PASSWORD_MARIADB",
    "database": "mundoChip"
}

def get_connection():
    return mariadb.connect(**DB_CONFIG)

def obtener_productos_activos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nombre_producto, precio_recomendado
            FROM productos
            WHERE activo = 1
            ORDER BY nombre_producto
        """)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.get("/")
def home():
    return redirect(url_for("login"))

@app.get("/index.html")
def login():
    return render_template("index.html")

@app.get("/formularios")
def formularios():
    productos = obtener_productos_activos()
    return render_template("formularios.html", productos=productos)

@app.post("/api/ventas")
def guardar_venta():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"ok": False, "mensaje": "No se recibieron datos JSON."}), 400

    productos = data.get("productos", [])
    comentarios = (data.get("comentarios") or "").strip()
    usuario_id = data.get("usuario_id")

    if not isinstance(productos, list) or not productos:
        return jsonify({"ok": False, "mensaje": "Debes enviar al menos un producto válido."}), 400

    if usuario_id in ("", None):
        usuario_id = None

    if usuario_id is not None:
        try:
            usuario_id = int(usuario_id)
        except (TypeError, ValueError):
            return jsonify({"ok": False, "mensaje": "El usuario_id no es válido."}), 400

    pedido_id = str(uuid4())

    conn = None
    cursor = None

    try:
        conn = get_connection()
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)

        if usuario_id is not None:
            cursor.execute("""
                SELECT id
                FROM usuarios
                WHERE id = ?
            """, (usuario_id,))
            usuario_db = cursor.fetchone()

            if not usuario_db:
                return jsonify({"ok": False, "mensaje": "El usuario indicado no existe."}), 400

        lineas_guardadas = []
        total_pedido = 0

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

            cursor.execute("""
                SELECT id, nombre_producto, activo
                FROM productos
                WHERE id = ?
            """, (producto_id,))
            producto_db = cursor.fetchone()

            if not producto_db:
                raise ValueError(f"El producto de la línea {index} no existe.")

            if int(producto_db["activo"]) != 1:
                raise ValueError(f"El producto de la línea {index} está inactivo.")

            cursor.execute("""
                INSERT INTO ventas
                (pedido_id, producto_id, cantidad, precio_unitario, comentarios, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pedido_id,
                producto_id,
                cantidad,
                precio_unitario,
                comentarios if comentarios else None,
                usuario_id
            ))

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
            "total_pedido": round(total_pedido, 2)
        }), 201

    except ValueError as e:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": str(e)}), 400

    except mariadb.Error as e:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": f"Error de base de datos: {e}"}), 500

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": f"Error interno: {e}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)