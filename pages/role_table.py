import sqlite3
from auth import hash_password
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
    
    # Verificar si la tabla está vacía
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    
    # Si la tabla está vacía, insertar un superadmin por defecto
    if count == 0:
        # Asegúrate de hashear la contraseña antes de insertarla en la base de datos
        hashed_password = hash_password("super") # Asume que hash_password es una función que hashea la contraseña
        c.execute('''INSERT INTO users (username, password, role)
                     VALUES (?, ?, ?)''', ("superadmin", hashed_password, "super-admin"))
    
    conn.commit()
    conn.close()

# Crear la tabla de usuarios si no existe y posiblemente insertar un superadmin por defecto
create_users_table()
