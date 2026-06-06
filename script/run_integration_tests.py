import requests
import sys

# URL base del servidor. Puedes cambiarla si tu servidor usa otra IP o puerto.
BASE_URL = "http://192.168.10.80"  # O "http://127.0.0.1:5000" si se ejecuta en local

def print_separator(title):
    print("\n" + "="*60)
    print(f" {title.upper()} ")
    print("="*60)

def test_integration():
    session = requests.Session()
    
    # ---------------------------------------------------------
    # PRUEBA 1: Autenticación de Usuarios
    # ---------------------------------------------------------
    print_separator("Prueba 1: Autenticación de Usuarios")
    
    # 1.1 Intento de login con credenciales incorrectas
    print("[1.1] Probando login con credenciales incorrectas...")
    payload_wrong = {"username": "admin", "password": "password_incorrecto"}
    response = session.post(f"{BASE_URL}/index.html", data=payload_wrong)
    if "Credenciales incorrectas" in response.text:
        print(" -> OK: El sistema denegó el acceso correctamente.")
    else:
        print(" -> ERROR: El sistema no mostró el mensaje de error de credenciales incorrectas.")

    # 1.2 Intento de login con credenciales correctas
    # Modifica 'admin' y '123456' si usas otros datos en tu BBDD
    username_valido = "admin"
    password_valida = "123456"
    print(f"[1.2] Probando login con credenciales válidas (Usuario: '{username_valido}')...")
    payload_correct = {"username": username_valido, "password": password_valida}
    # Allow redirects to follow to the forms page
    response = session.post(f"{BASE_URL}/index.html", data=payload_correct, allow_redirects=True)
    
    # Verificar si estamos en la página de formularios
    if "formularios" in response.url or "Gestión de Ventas" in response.text:
        print(" -> OK: Login exitoso. Redirección correcta a formularios.")
    else:
        print(" -> ERROR: No se pudo iniciar sesión o no se redirigió correctamente.")
        print(f"    URL actual: {response.url}")
        print("    Detén la ejecución si las credenciales en tu base de datos no coinciden.")

    # ---------------------------------------------------------
    # PRUEBA 2: Persistencia y Consistencia de Ventas
    # ---------------------------------------------------------
    print_separator("Prueba 2: Persistencia de Ventas (API JSON)")
    
    # 2.1 Envío de venta válida multi-línea
    # (Asegúrate de que los IDs de producto 1 y 2 existan y estén activos en tu BBDD)
    venta_valida = {
        "productos": [
            {"producto_id": 1, "cantidad": 2, "precio_unitario": 450.00},
            {"producto_id": 2, "cantidad": 1, "precio_unitario": 89.99}
        ],
        "comentarios": "Pedido de prueba de integración de hardware."
    }
    
    print("[2.1] Enviando payload de venta multi-línea válido...")
    response_venta = session.post(f"{BASE_URL}/api/ventas", json=venta_valida)
    print(f"      Código de Estado HTTP: {response_venta.status_code}")
    
    try:
        res_json = response_venta.json()
        if response_venta.status_code == 201 and res_json.get("ok") is True:
            print(" -> OK: Venta registrada exitosamente.")
            print(f"    Pedido ID (UUID): {res_json.get('pedido_id')}")
            print(f"    Total calculado por el backend: {res_json.get('total_pedido')} €")
            for linea in res_json.get("lineas", []):
                print(f"      - {linea['producto']} x{linea['cantidad']}: {linea['subtotal']} €")
        else:
            print(f" -> ERROR: No se pudo guardar la venta. Mensaje: {res_json.get('mensaje')}")
    except Exception as e:
        print(f" -> ERROR al parsear respuesta JSON de ventas: {e}")
        print(f"    Response text: {response_venta.text}")

    # 2.2 Envío de datos inválidos (cantidad negativa) para validar control ACID/Errores
    venta_invalida = {
        "productos": [
            {"producto_id": 1, "cantidad": -5, "precio_unitario": 450.00}
        ],
        "comentarios": "Esto debe fallar."
    }
    print("[2.2] Enviando payload inválido (cantidad negativa) para verificar validaciones...")
    response_invalida = session.post(f"{BASE_URL}/api/ventas", json=venta_invalida)
    print(f"      Código de Estado HTTP: {response_invalida.status_code}")
    try:
        res_invalida_json = response_invalida.json()
        if response_invalida.status_code == 400 and res_invalida_json.get("ok") is False:
            print(" -> OK: El backend rechazó la petición con código 400 y mensaje adecuado.")
            print(f"    Mensaje del backend: '{res_invalida_json.get('mensaje')}'")
        else:
            print(f" -> ERROR: El backend aceptó la petición o no devolvió 400. Respuesta: {res_invalida_json}")
    except Exception as e:
        print(f" -> ERROR al parsear respuesta JSON de validación: {e}")

    # ---------------------------------------------------------
    # PRUEBA 3: Inyección SQL y Robustez
    # ---------------------------------------------------------
    print_separator("Prueba 3: Robustez frente a Inyección SQL")
    
    # 3.1 Intento de bypass de login con SQL Injection en el campo de usuario
    print("[3.1] Intentando bypass de login mediante inyección SQL en 'username'...")
    payload_sqli = {"username": "admin' OR '1'='1", "password": "any_password"}
    response_sqli = session.post(f"{BASE_URL}/index.html", data=payload_sqli)
    if "Credenciales incorrectas" in response_sqli.text:
        print(" -> OK: El ataque de inyección SQL en el login falló. Acceso denegado.")
    else:
        print(" -> ERROR: Posible bypass de autenticación detectado o comportamiento inesperado.")

    # 3.2 Envío de payload SQL malicioso en comentarios de ventas
    venta_sqli = {
        "productos": [
            {"producto_id": 1, "cantidad": 1, "precio_unitario": 450.00}
        ],
        # Inyección SQL que intentaría alterar la tabla o cerrar la consulta
        "comentarios": "Normal comment'); DROP TABLE ventas; --"
    }
    print("[3.2] Enviando venta con inyección SQL en el campo 'comentarios'...")
    response_sqli_venta = session.post(f"{BASE_URL}/api/ventas", json=venta_sqli)
    print(f"      Código de Estado HTTP: {response_sqli_venta.status_code}")
    try:
        res_sqli_json = response_sqli_venta.json()
        if response_sqli_venta.status_code == 201 and res_sqli_json.get("ok") is True:
            print(" -> OK: La venta se registró normalmente. El payload se guardó como texto plano.")
            print("        Las consultas preparadas (paramétricas) neutralizaron la inyección SQL.")
        else:
            print(f" -> ERROR o Fallo al registrar venta: {res_sqli_json.get('mensaje')}")
    except Exception as e:
        print(f" -> ERROR al parsear respuesta JSON: {e}")

    # 3.3 Cerrar sesión
    print_separator("Cierre de Sesión")
    session.get(f"{BASE_URL}/logout")
    print("Pruebas completadas. Revisa ahora las tablas de MariaDB para confirmar la persistencia.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    
    print(f"Iniciando pruebas de integración sobre: {BASE_URL}")
    print("Asegúrate de que el servidor Flask esté corriendo.")
    try:
        test_integration()
    except requests.exceptions.ConnectionError:
        print(f"\nERROR: No se pudo conectar al servidor en {BASE_URL}.")
        print("Verifica que la dirección IP sea correcta y que el servicio esté activo.")
