import streamlit as st
import sqlite3
from sqlite3 import Error
from menu import menu_with_redirect
import uuid
from datetime import datetime
menu_with_redirect()
def fecha_excluida_component(key,fecha_inicio,fecha_fin):
    """
    Componente para manejar fechas excluidas.
    Permite agregar y eliminar fechas de manera dinámica.
    """
    if key not in st.session_state:
        st.session_state[key] = []

    with st.expander("Fechas excluidas"):
        # Opción para agregar una nueva fecha excluida
        if st.button("Agregar fecha excluida", key=f"{key}_agregar"):
            new_id = uuid.uuid4() # Genera un identificador único para la nueva fecha
            
            st.session_state[key].append({"id": new_id, "fecha": None})

        # Mostrar las fechas excluidas actuales
        for item in st.session_state[key]:
            if item is not None: # Asegura que item no sea None
                fecha_excluida = st.date_input(f"Fecha excluida ", value=item["fecha"], key=f"{key}_fecha_{item['id']}")
                if st.button(f"Eliminar fecha", key=f"{key}_eliminar_{item['id']}"):
                    # Encuentra y elimina el elemento por su id
                    st.session_state[key] = [fecha for fecha in st.session_state[key] if fecha['id'] != item['id']]
                    st.experimental_rerun()
                    break
                    

                # Actualizar la fecha excluida en el estado de la sesión
                item["fecha"] = fecha_excluida
                

        return st.session_state[key]

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql_create_table = """ CREATE TABLE evaluaciones (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 curso TEXT,
 duracion_curso TEXT,
 carrera TEXT,
 año INTEGER,
 asignatura TEXT,
 evaluacion TEXT,
 rangos_fechas TEXT,
 fechas_excluidas TEXT,
 UNIQUE(curso, carrera, año, asignatura)
);
 """
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

def insert_or_update_data(conn, data):
    # Asume que 'data' no incluye un 'id' para la inserción
    # y que 'id' se generará automáticamente
    sql_upsert = '''
INSERT INTO evaluaciones(curso, duracion_curso,carrera, año, asignatura, evaluacion, rangos_fechas,fechas_excluidas)
VALUES(?,?,?,?,?,?,?,?)
ON CONFLICT(curso, carrera, año, asignatura) DO UPDATE SET
duracion_curso=excluded.duracion_curso,
evaluacion = excluded.evaluacion,
rangos_fechas = excluded.rangos_fechas,
fechas_excluidas=excluded.fechas_excluidas
'''
    cur = conn.cursor()
    cur.execute(sql_upsert, data)
    
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
    if 'fecha_inicio_curso' not in st.session_state:
        fecha_inicio_curso=None
    if 'fecha_fin_curso' not in st.session_state:
        fecha_fin_curso=None
    if 'evaluacion' not in st.session_state:
        evaluacion = None
    if 'fecha_inicio' not in st.session_state:
        fecha_inicio = None
    if 'fecha_fin' not in st.session_state:
        fecha_fin = None
    if 'fechas_excluidas' not in st.session_state:
        st.session_state.fechas_excluidas = []
    # Opciones para seleccionar la carrera y el año
    carreras = ["Ciencias de la Computación", "Ciencia de Datos", "Matemática"]
    años = list(range(1,6)) # Ajusta el rango según sea necesario

    carrera_seleccionada = st.selectbox("Selecciona la carrera:", carreras, key='carrera_seleccionada')
    año_seleccionado = st.selectbox("Selecciona el año:", años, key='año_seleccionado')
    
    curso = st.text_input("Curso", key='curso')
    if type(curso) != str:
        st.warning("El valor ingresado debe ser un texto")
        curso = None
    fecha_inicio_curso = st.date_input(f"Fecha de inicio curso", key=f"fecha_inicio_curso")
    fecha_fin_curso = st.date_input(f"Fecha de término curso", key=f"fecha_fin_curso")
    
    asignatura = st.text_input("Asignatura", key='asignatura')
    if type(asignatura) != str:
        st.warning("El valor ingresado debe ser un texto")
        asignatura = None
   
    evaluacion = st.text_input("Evaluación", key='evaluacion')
    if evaluacion=="":
        pass
    else:
        try:
            evaluacion = int(evaluacion)
                
            rangos_fechas = []
            fechas_excluidas = []
            for i in range(evaluacion):
                
                fecha_inicio = st.date_input(f"Fecha de inicio Evaluación {i+1}", key=f"fecha_inicio_{i}")
                fecha_fin = st.date_input(f"Fecha de término Evaluación {i+1}", key=f"fecha_fin_{i}")
                fecha_excluida=fecha_excluida_component(f"fechas_excluidas {i}",fecha_fin,fecha_fin)
                
                if fecha_inicio and fecha_fin  :
                    rangos_fechas.append(f"{fecha_inicio}/{fecha_fin}")
                concat=""
                for element in fecha_excluida:
                    if element["fecha"] is not None:
                        concat = concat  + element["fecha"].strftime("%d-%m-%Y") +"/"
                fechas_excluidas.append(concat)    
        except ValueError:
                    st.warning("El valor ingresado debe ser un número entero")
                    evaluacion = None
        
        
    
    if st.button("Guardar"):
        if not asignatura or not evaluacion:
            st.warning("Por favor, ingrese todos los datos o revise si tienen el formato correcto")
        else:
            
            for i in range(evaluacion):

                fecha_inicio, fecha_fin = rangos_fechas[i].split('/')
                if fecha_inicio and fecha_fin and fecha_inicio <= fecha_fin:
                    continue
                else:
                    st.warning("La fecha de inicio debe ser anterior a la fecha de término")
                    rangos_fechas = []
                    break
            if fecha_inicio_curso and fecha_fin_curso and fecha_inicio_curso <= fecha_fin_curso:
                    pass
            else:
                    st.warning("La fecha de inicio de curso debe ser anterior a la fecha de término")
                    fecha_inicio_curso=None
                    fecha_fin_curso=None
                    
            
            if rangos_fechas and fecha_fin_curso:
                db_file = "evaluaciones.db" 
                conn = create_connection(db_file) 
                
                
                duracion_curso=(f"{fecha_inicio_curso}/{fecha_fin_curso}")
                
                if conn is not None:
                    create_table(conn)
                    
                    data = (curso,duracion_curso, carrera_seleccionada, año_seleccionado, asignatura, evaluacion, '//'.join(rangos_fechas), '//'.join(fechas_excluidas))
                    insert_or_update_data(conn, data)
                    conn.commit()

                    st.success("Datos guardados correctamente")
                else:
                    st.error("Error al conectar con la base de datos")

app()