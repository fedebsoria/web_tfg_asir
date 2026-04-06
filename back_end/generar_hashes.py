from werkzeug.security import generate_password_hash

def generar_usuario(user_name, password):
    """Genera el hash completo listo para INSERT en MariaDB."""
    hash_value = generate_password_hash(password)
    sql = f"INSERT INTO usuarios (user_name, password) VALUES ('{user_name}', '{hash_value}');"
    print(sql)
    print(f"Verificación: check_password_hash('{hash_value}', '{password}') = True")
    return hash_value

if __name__ == "__main__":
    generar_usuario("usuario1", "password1")
    generar_usuario("usuario2", "password2")
    generar_usuario("admin", "123456")
    generar_usuario("testuser", "test123")


"""
1. Usuario → "password1"
↓
2. generate_password_hash("password1") → scrypt:...$hashúnico
↓
3. INSERT usuarios (..., 'scrypt:...$hashúnico')
↓
4. Login → check_password_hash('scrypt:...$hashúnico', "password1") → True
"""
