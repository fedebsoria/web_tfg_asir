from flask import Flask, render_template, request, jsonify
import mariadb
from pathlib import Path
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR),
    static_folder=str(BASE_DIR)
)

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "tu_usuario",
    "password": "tu_password",
    "database": "mundoChip"
}

def get_connection():
    return mariadb.connect(**DB_CONFIG)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/formularios")
def formularios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, nombre_producto, precio_recomendado
            FROM productos
            WHERE activo = 1
            ORDER BY nombre_producto
        """)
        productos = cursor.fetchall()
        return render_template("formularios.html", productos=productos)
    finally:
        cursor.close()
        conn.close()

@app.post("/api/ventas")
def guardar_venta():
    data = request.get_json(silent=True)

    if not data or "productos" not in data:
        return jsonify({"ok": False, "mensaje": "Datos no válidos"}), 400

    productos = data["productos"]
    comentarios = (data.get("comentarios") or "").strip()
    usuario_id = data.get("usuario_id")

    if not productos:
        return jsonify({"ok": False, "mensaje": "Debes enviar al menos un producto"}), 400

    pedido_id = str(uuid4())

    conn = None
    cursor = None

    try:
        conn = get_connection()
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)

        for item in productos:
            producto_id = item.get("producto_id")
            cantidad = item.get("cantidad")
            precio_unitario = item.get("precio_unitario")

            try:
                producto_id = int(producto_id)
                cantidad = int(cantidad)
                precio_unitario = float(precio_unitario)
            except (TypeError, ValueError):
                raise ValueError("Hay una línea de producto con datos inválidos.")

            if cantidad < 1 or precio_unitario < 0:
                raise ValueError("Cantidad o precio fuera de rango.")

            cursor.execute("""
                SELECT id
                FROM productos
                WHERE id = ? AND activo = 1
            """, (producto_id,))
            producto_db = cursor.fetchone()

            if not producto_db:
                raise ValueError(f"El producto con id {producto_id} no existe o está inactivo.")

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

        conn.commit()

        return jsonify({
            "ok": True,
            "mensaje": "Venta guardada correctamente",
            "pedido_id": pedido_id
        }), 201

    except ValueError as e:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": str(e)}), 400

    except mariadb.Error as e:
        if conn:
            conn.rollback()
        return jsonify({"ok": False, "mensaje": f"Error de base de datos: {e}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()