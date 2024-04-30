from datetime import datetime, timedelta
from pages.problem import Problem
from typing import List, Tuple
import sqlite3
import streamlit as st

def create_new_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS calendarios')
    c.execute('''CREATE TABLE IF NOT EXISTS calendarios
                 (carrera TEXT, año INTEGER, curso TEXT, asignatura TEXT, fecha_examen TEXT)''')
    conn.commit()
    return conn


def read_distinct_data(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Seleccionar todos los valores únicos por carrera, año y curso
    c.execute('SELECT DISTINCT carrera, año, curso FROM evaluaciones')
    data = c.fetchall()
    conn.close()
    return data
def get_detalles_por_curso(db_name, carrera, año, curso):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Seleccionar todas las asignaturas y detalles para un curso específico
    c.execute('''SELECT asignatura, duracion_curso ,evaluacion, rangos_fechas,fechas_excluidas
                 FROM evaluaciones 
                 WHERE carrera = ? AND año = ? AND curso = ?''', (carrera, año, curso))
    detalles = c.fetchall()
    conn.close()
    return detalles

def get_asignaturas_por_curso(db_name, carrera, año, curso):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Seleccionar todas las asignaturas para un curso específico
    c.execute('SELECT DISTINCT asignatura FROM evaluaciones WHERE carrera = ? AND año = ? AND curso = ?', (carrera, año, curso))
    asignaturas = c.fetchall()
    conn.close()
    return asignaturas
def procesar_evaluaciones(detalles):
    evaluaciones_procesadas = []
    for asignatura, duracion_curso, evaluacion, rangos_fechas, fechas_excluidas in detalles:
        # Dividir las fechas de excluídas y los rangos de fechas
        fechas_excluidas = fechas_excluidas.split('///')

        rangos_fechas = rangos_fechas.split('//')
        
        # Asegurarse de que haya la misma cantidad de fechas excluidas y rangos de fechas
        
        if (fechas_excluidas== '//'):
            fechas_excluidas=[]
        
        # Procesar cada evaluación individualmente
        for i in range(len(fechas_excluidas)):
            evaluacion_individual = (asignatura,fechas_excluidas[i], rangos_fechas[i], duracion_curso)
            evaluaciones_procesadas.append(evaluacion_individual)
    
    return evaluaciones_procesadas

def preprocesar_datos(detalles,calificaciones):

    j = 0

    calendar = { }

    for (course_name, grade, year), subjects in detalles.items ():

        F: List[List[int]] = []
        V: List[Tuple[int, int]] = []
        K: List[int] = []
        Di: int = 0

        for i, (subject_name, excluded, range_, length) in enumerate (subjects):

            excluded_dates: List[datetime]

            if excluded == '//':

                excluded_dates = []

            else:

                excluded_dates = excluded.split ('/')

                while True:

                    try:
                        excluded_dates.remove ('')
                    except ValueError:
                        break

                excluded_dates = [ datetime.strptime (d, '%d-%m-%Y') for d in excluded_dates ]

            begin_date, end_date = (datetime.strptime (d, '%Y-%m-%d') for d in range_.split ('/'))
            begin_course, end_course = (datetime.strptime (d, '%Y-%m-%d') for d in length.split ('/'))

            F.append ([ (d - begin_course).days for d in excluded_dates ])
            V.append (((begin_date - begin_course).days, (end_date - begin_course).days))
            K.append (calificaciones.get ((subject_name, course_name, grade, year), 5))
            Di = max (Di, (end_course - begin_course).days)

        course = Curso (len (F), F, V, K, Di).fit_to_date (begin_course)

        for d, (subject_name, excluded, range_, length) in zip (course, subjects):

            calendar[course_name, grade, year, j] = (d, subject_name)
            j += 1

    return calendar

def process_data_and_save(data, new_db_name):
    new_db_conn = create_new_database(new_db_name)
    c = new_db_conn.cursor()
    
    for key, value in data.items():
        carrera, año, curso, asignatura, _ = key
        fecha_examen = value.strftime('%Y-%m-%d %H:%M:%S') # Convertir datetime a string
        c.execute('INSERT INTO calendarios VALUES (?, ?, ?, ?, ?)', (carrera, año, curso, asignatura, fecha_examen))
    new_db_conn.commit()
    new_db_conn.close()
class Curso (Problem):
    def fit (self):
        x, val = self.optimize ()
        return x[0]
    def fit_to_date (self, base_date: datetime):
        x = self.fit ()
        x = [ base_date + timedelta (days = int (day)) for day in x ]
        return x
    def __init__ (self, N, F, V, K, Di):
        super ().__init__ (1, N, [F], [V], [K], [Di])

def calculate_workload(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Suponiendo que quieres calcular la carga de trabajo basada en la media de las calificaciones
    c.execute('''
        SELECT asignatura,carrera,curso,año, AVG(clasificacion) as media_calificacion
        FROM usuario_clasificaciones
        GROUP BY asignatura ,carrera , año , curso
    ''')
    workloads = c.fetchall()
    
    # Convertir los resultados en un diccionario para facilitar el acceso
    workload_dict = {(asignatura, carrera, año, curso): media for asignatura, carrera, curso, año, media in workloads}
    
    # Ahora, asigna estos valores a K. Suponiendo que K es una matriz de tamaño Nx1, donde N es el número de asignaturas
    # y que el orden de las asignaturas en K coincide con el orden en el que las obtienes de la base de datos
    
    
    return workload_dict

# Uso de la función
db_name = 'usuario_clasificaciones.db'
K = calculate_workload(db_name)

def main():
    db_name = 'evaluaciones.db'
    # Leer todos los valores únicos por carrera, año y curso
    data = read_distinct_data(db_name)
    
    # Diccionario para almacenar los detalles indexados
    detalles_indexados = {}
    
    for carrera, año, curso in data:
        # Obtener todos los detalles para cada asignatura de un curso específico
        detalles = get_detalles_por_curso(db_name, carrera, año, curso)
        
        # Guardar los detalles en la estructura indexada
        clave = (carrera, año, curso)
        detalles_indexados[clave] = detalles
    detalles_procesados = {}
    for clave, detalles in detalles_indexados.items():
        detalles_procesados[clave] = procesar_evaluaciones(detalles)
    calificaciones=calculate_workload('usuario_clasificaciones.db')
    calendario=preprocesar_datos(detalles_procesados,calificaciones)
    
    calendario_procesado ={ }
    llaves=calendario.keys()
    valores=calendario.values()
    for element in calendario.keys():
        calendario_procesado[element[0],element[1],element[2],calendario[element][1],element[3]]=calendario[element][0]
    
    process_data_and_save(calendario_procesado,"calendarios_optimizados.db")

def run_app():
    st.title('Optimización de Calendario Académico')
    if st.button('Optimizar Calendario'):
        main()

if __name__ == "__main__":
    
    run_app()
