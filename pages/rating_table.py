import sqlite3
from sqlite3 import Error
def create_clasificaciones_table():
    conn=sqlite3.connect('usuario_clasificaciones.db')
    try:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS usuario_clasificaciones (
                                        id integer PRIMARY KEY,
                                        usuario text NOT NULL,
                                        curso text NOT NULL,
                                        carrera text NOT NULL,
                                        año integer NOT NULL,
                                        asignatura text NOT NULL,
                                        clasificacion integer NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_table)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
create_clasificaciones_table()