import streamlit as st
import sqlite3
from menu import menu_with_redirect
menu_with_redirect()
def get_asignaturas(curso, carrera, año):
    conn = sqlite3.connect('evaluaciones.db')
    
    c = conn.cursor()
    c.execute('SELECT asignatura FROM evaluaciones WHERE curso = ? AND carrera = ? AND año = ?', (curso, carrera, año))
    asignaturas = [row[0] for row in c.fetchall()]
    conn.close()
    return asignaturas
def get_carreras(conn):
    c = conn.cursor()
    c.execute("SELECT DISTINCT carrera FROM evaluaciones")
    carreras = [row[0] for row in c.fetchall()]
    return carreras

def get_cursos(conn, carrera):
    cursos = [] # Inicializa cursos como una lista vacía
    try:
        c = conn.cursor()
        c.execute("SELECT DISTINCT curso FROM evaluaciones WHERE carrera = ?", (carrera,))
        cursos = [row[0] for row in c.fetchall()]
    except Exception as e:
        st.write(f"Error al obtener cursos para la carrera seleccionada: {e}")
    return cursos


def get_años(conn,carrera,curso):
    try:
        c = conn.cursor()
        c.execute("SELECT DISTINCT año FROM evaluaciones Where carrera = ? AND curso = ?",(carrera,curso))
        años = [row[0] for row in c.fetchall()]
    except :
        st.write("No hay años para el curso seleccionado en la carrera seleccionada")
    return años

def app():
    db_file="evaluaciones.db"
    conn = sqlite3.connect(db_file)
    carreras = get_carreras(conn)
    
    
    # Llenar los selectboxes con los valores únicos
    carrera = st.selectbox("Selecciona la carrera:", carreras, key='carrera_seleccionada')
    cursos = get_cursos(conn,carrera)
   
    curso = st.selectbox("Selecciona el curso:", cursos, key='curso')
    años = get_años(conn,carrera,curso)
    año = st.selectbox("Selecciona el año:", años, key='año_seleccionado')
        
    asignaturas = get_asignaturas(curso, carrera, año)
    
    for asignatura in asignaturas:
        clasificacion = st.slider(f"Diga la carga de trabajo para {asignatura}:", 1, 10)
        if st.button(f"Guardar carga de trabajo para {asignatura}"):
            conn = sqlite3.connect('usuario_clasificaciones.db')
            c = conn.cursor()

            # Verificar si ya existe una calificación para el usuario, curso, carrera y año
            c.execute('''SELECT COUNT(*) FROM usuario_clasificaciones 
                         WHERE usuario = ? AND curso = ? AND carrera = ? AND año = ? AND asignatura = ?''', 
                       (st.session_state.username, curso, carrera, año, asignatura))
            count = c.fetchone()[0]

            if count > 0:
                # Si existe, actualizar la calificación
                c.execute('''UPDATE usuario_clasificaciones 
                             SET clasificacion = ? 
                             WHERE usuario = ? AND curso = ? AND carrera = ? AND año = ? AND asignatura = ?''', 
                           (clasificacion, st.session_state.username, curso, carrera, año, asignatura))
                st.success(f"Carga de trabajo de {asignatura} actualizada exitosamente.")
            else:
                # Si no existe, insertar una nueva calificación
                c.execute('''INSERT INTO usuario_clasificaciones (usuario, curso, carrera, año, asignatura, clasificacion)
                             VALUES (?, ?, ?, ?, ?, ?)''', 
                           (st.session_state.username, curso, carrera, año, asignatura, clasificacion))
                st.success(f"Carga de trabaja de {asignatura} guardada exitosamente.")

            conn.commit()
            conn.close()

app()