
import streamlit as st
import sqlite3
from sqlite3 import Error
from menu import menu_with_redirect
menu_with_redirect()
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file) # Ahora apunta a un archivo de base de datos en disco
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS evaluaciones (
                                        id integer PRIMARY KEY,
                                        curso text NOT NULL,
                                        carrera text NOT NULL,
                                        año integer NOT NULL,
                                        asignatura text NOT NULL,
                                        evaluacion integer NOT NULL,
                                        fecha_inicio text NOT NULL,
                                        fecha_fin text NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

def insert_data(conn, data):
    # Definir los criterios para la eliminación
    sql_delete = '''
    DELETE FROM evaluaciones
    WHERE carrera = ? AND año = ? AND asignatura = ? AND curso = ?
    '''
    cur = conn.cursor()
    cur.execute(sql_delete, (data[1], data[2], data[3], data[0])) # Asegúrate de que los índices de data coincidan con los campos correctos

    # Insertar el nuevo registro
    sql_insert = '''
    INSERT INTO evaluaciones(curso, carrera, año, asignatura, evaluacion, fecha_inicio, fecha_fin)
    VALUES(?,?,?,?,?,?,?)
    '''
    cur.execute(sql_insert, data)

    conn.commit()
    return cur.lastrowid



def app():
    st.title("Planificación de Evaluaciones")
    if 'carrera_seleccionada' not in st.session_state:
        carrera_seleccionada = None
    if 'año_seleccionado' not in st.session_state:
        año_seleccionado = None
    if 'asignatura' not in st.session_state:
        asignatura = None
    if 'curso' not in st.session_state:
        curso = None
    if 'evaluacion' not in st.session_state:
        evaluacion = None
    if 'fecha_inicio' not in st.session_state:
        fecha_inicio = None
    if 'fecha_fin' not in st.session_state:
        fecha_fin = None
    # Opciones para seleccionar la carrera y el año
    carreras = ["Ciencias de la Computación", "Ciencia de Datos", "Matemática"]
    años = list(range(1,6)) # Ajusta el rango según sea necesario

    carrera_seleccionada = st.selectbox("Selecciona la carrera:", carreras, key='carrera_seleccionada')
    año_seleccionado = st.selectbox("Selecciona el año:", años, key='año_seleccionado')

    asignatura = st.text_input("Asignatura", key='asignatura')
    if type(asignatura) != str:
        st.warning("El valor ingresado debe ser un texto")
        asignatura = None
    curso=["2000-2001","2001-20002","2002-2003","2003-2004","2004-2005","2005-2006","2006-2007","2007-2008","2008-2009","2009-2010","2010-2011","2011-2012","2012-2013","2013-2014","2014-2015","2015-2016","2016-2017","2017-2018","2018-2019","2019-2020","2020-2021","2021-2022","2022-2023","2023-2024","2024-2025","2025-2026","2026-2027"]    
    curso = st.selectbox("Curso", curso, key='curso')
    
    evaluacion = st.text_input("Evaluación", key='evaluacion')
    if evaluacion=="":
        pass
    else:
        try:
            evaluacion = int(evaluacion)
        except ValueError:
            st.warning("El valor ingresado debe ser un número entero")
            evaluacion = None
        
    
    
    fecha_inicio = st.date_input("Fecha de inicio",key="fecha_inicio")
    fecha_fin = st.date_input("Fecha de término",key="fecha_fin")
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        st.warning("La fecha de inicio debe ser anterior a la fecha de término")
        fecha_inicio = None
        fecha_fin = None

    if st.button("Guardar"):
        if not asignatura or not evaluacion or not fecha_inicio or not fecha_fin:
            st.warning("Por favor, ingrese todos los datos o revise si tienen el formato correcto")
        else:
            db_file = "mi_base_de_datos.db" 
            conn = create_connection(db_file) 
            if conn is not None:
                create_table(conn)
                data = (curso,carrera_seleccionada, año_seleccionado, asignatura, evaluacion, fecha_inicio, fecha_fin)
                insert_data(conn, data)
                conn.commit()
                
                st.success("Datos guardados correctamente")
            else:
                st.error("Error al conectar con la base de datos")

app()