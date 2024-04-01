import sqlite3
import os

def create_new_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calendarios
                 (carrera TEXT, año INTEGER, curso TEXT, asignatura TEXT, fecha_examen TEXT)''')
    conn.commit()
    return conn

def read_current_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT carrera, año, curso, asignatura, fecha_examen FROM evaluaciones')
    return c.fetchall()

def process_data_and_save(data, new_db_name):
    new_db_conn = create_new_database(new_db_name)
    c = new_db_conn.cursor()
    for carrera, año, curso, asignatura, fecha_examen in data:
        c.execute('INSERT INTO calendarios VALUES (?, ?, ?, ?, ?)', (carrera, año, curso, asignatura, fecha_examen))
    new_db_conn.commit()
    new_db_conn.close()

def main():
    current_db_name = 'mi_base_de_datos.db'
    new_db_name = 'calendarios_optimizados.db'
    create_new_database(new_db_name)
    # Leer la base de datos actual
    data = read_current_database(current_db_name)
    
    # Procesar los datos y guardar en la nueva base de datos
    process_data_and_save(data, new_db_name)
    
    print(f"Calendarios optimizados guardados en {new_db_name}")

if __name__ == "__main__":
    main()
