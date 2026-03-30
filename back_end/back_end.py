from flask import Flask, request, jsonify
import mariadb

app = Flask(__name__)

def get_connection():
    return mariadb.connect(
        host="localhost",
        port=3306,
        user="tu_usuario",
        password="tu_password",
        database="mundoChip"
    )

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('user_name', '').strip()
    password = data.get('password', '')

    if not user_name or not password:
        return jsonify({
            'ok': False,
            'message': 'Debes completar usuario y contraseña'
        }), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, user_name, password FROM usuarios WHERE user_name = ?",
        (user_name,)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({
            'ok': False,
            'message': 'Usuario no encontrado'
        }), 401

    if user['password'] != password:
        return jsonify({
            'ok': False,
            'message': 'Contraseña incorrecta'
        }), 401

    return jsonify({
        'ok': True,
        'message': 'Login correcto',
        'redirect': '/formularios.html',
        'user_id': user['id'],
        'user_name': user['user_name']
    })