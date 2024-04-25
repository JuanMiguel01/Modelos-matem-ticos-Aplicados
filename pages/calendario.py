
import streamlit as st
import sqlite3
import pandas as pd
from menu import menu_with_redirect

menu_with_redirect()

def obtener_asignaturas(carrera, año, curso):
    
    con = sqlite3.connect("evaluaciones.db") 
    cur = con.cursor()
    
    cur.execute('''SELECT asignatura, fecha_inicio, fecha_fin 
                   FROM evaluaciones 
                   WHERE carrera = ? AND año = ? AND curso = ?''', 
                (carrera, año, curso))
    
    asignaturas = cur.fetchall()
    con.close()
    
    return asignaturas
def get_carreras(conn):
    c = conn.cursor()
    c.execute("SELECT DISTINCT carrera FROM calendarios")
    carreras = [row[0] for row in c.fetchall()]
    return carreras

def get_cursos(conn, carrera):
    cursos = [] # Inicializa cursos como una lista vacía
    try:
        c = conn.cursor()
        c.execute("SELECT DISTINCT curso FROM calendarios WHERE carrera = ?", (carrera,))
        cursos = [row[0] for row in c.fetchall()]
    except Exception as e:
        st.write(f"Error al obtener cursos para la carrera seleccionada: {e}")
    return cursos


def get_años(conn,carrera,curso):
    try:
        c = conn.cursor()
        c.execute("SELECT DISTINCT año FROM calendarios Where carrera = ? AND curso = ?",(carrera,curso))
        años = [row[0] for row in c.fetchall()]
    except :
        st.write("No hay años para el curso seleccionado en la carrera seleccionada")
    return años
def app():
    st.title("Selecciona tu Calendario")
    db_file="calendarios_optimizados.db"
    conn = sqlite3.connect(db_file)
    carreras = get_carreras(conn)
    
    
    # Llenar los selectboxes con los valores únicos
    carrera = st.selectbox("Selecciona la carrera:", carreras, key='carrera_seleccionada')
    cursos = get_cursos(conn,carrera)
   
    curso = st.selectbox("Selecciona el curso:", cursos, key='curso')
    años = get_años(conn,carrera,curso)
    año = st.selectbox("Selecciona el año:", años, key='año_seleccionado')
        
    if st.button("Mostrar Calendario"):
        conn = sqlite3.connect('calendarios_optimizados.db')
        c = conn.cursor()
        
        # Realizar la consulta a la base de datos
        c.execute('''
            SELECT asignatura, fecha_examen
            FROM calendarios
            WHERE carrera = ? AND año = ? AND curso = ?
        ''', (carrera, año, curso))
        resultados = c.fetchall()
        
        if resultados:
            st.markdown(f"## Calendario para {carrera} {año}")
            # Convertir los resultados a un DataFrame de pandas
            df = pd.DataFrame(resultados, columns=['Asignatura', 'Fecha de Examen'])
            # Mostrar la tabla con pandas
            st.table(df)
        else:
            st.write("No se encontraron asignaturas para la selección.")
        
        conn.close()

app()