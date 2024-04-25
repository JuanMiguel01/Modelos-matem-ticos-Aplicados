import sqlite3
import os
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from pages.problem import Problem
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
        if len(fechas_excluidas) != len(rangos_fechas):
            print(f"Error en la asignatura {asignatura}: fechas excluidas y rangos de fechas no coinciden.")
            continue
        
        # Procesar cada evaluación individualmente
        for i in range(len(fechas_excluidas)):
            evaluacion_individual = (asignatura,fechas_excluidas[i], rangos_fechas[i], duracion_curso)
            evaluaciones_procesadas.append(evaluacion_individual)
    
    return evaluaciones_procesadas
#
#










#
#ver lo de las fechas excluidas que no se estan poniendo como una lista delisat s

def preprocesar_datos(detalles,calificaciones):
    fechas_excluidas=[]
    plazos_examen_total=[]
    calificaciones_por_asignatura=[]
    duracion_cursos=[]
    inicio_cursos=[]
    asignaturas=[]
    for clave, evaluaciones in detalles.items():
        # Extraer y procesar las fechas
        
        fechas_excluidas_locales = []
        
        for i in range(len(evaluaciones)): 
            asignaturas.append(evaluaciones[i][0])
            fechas_excluidas_locales.append(evaluaciones[i][1].split('/'))
        
        for i in range(len(fechas_excluidas_locales)):
            for j in range(len(fechas_excluidas_locales[i])):
                if fechas_excluidas_locales[i][j]=='':
                    fechas_excluidas_locales[i].remove(fechas_excluidas_locales[i][j])
                else:
                    
                    fechas_excluidas_locales[i][j]=datetime.strptime(fechas_excluidas_locales[i][j], '%d-%m-%Y')
        fechas_excluidas.append(fechas_excluidas_locales) 
            
        fechas_examen = []
        for evaluacion in evaluaciones:
            # Separar las fechas de inicio y fin del examen
            inicio_fin_examen = evaluacion[2].split('/')
            inicio_examen = datetime.strptime(inicio_fin_examen[0], '%Y-%m-%d')
            fin_examen = datetime.strptime(inicio_fin_examen[1], '%Y-%m-%d')
            fechas_examen.append((inicio_examen, fin_examen))
        plazos_examen =[]
        duracion_curso=0
        for evaluacion in evaluaciones:

            inicio_curso = datetime.strptime(evaluacion[3].split('/')[0], '%Y-%m-%d')
            fin_curso = datetime.strptime(evaluacion[3].split('/')[1], '%Y-%m-%d')


            duracion_curso = fin_curso - inicio_curso
        inicio_cursos.append(inicio_curso)

        duracion_cursos.append(duracion_curso.days)
        for i in range(len(fechas_examen)):

                plazos_examen.append((fechas_examen[i][0]-inicio_curso, fechas_examen[i][1]-inicio_curso))
        for i in range (len(plazos_examen)):
            plazos_examen[i] = (plazos_examen[i][0].days, plazos_examen[i][1].days)
        plazos_examen_total.append(plazos_examen)
        calificacion=[]
        for evaluacion in evaluaciones:
            asignatura = evaluacion[0]
            clave_=(asignatura,clave[0],clave[1],clave[2])
            calificacion.append(calificaciones[clave_])
        
        calificaciones_por_asignatura.append(calificacion)
    
    for i in range(len(fechas_excluidas)):
        for j in range(len(fechas_excluidas[i])):
            for k in range(len(fechas_excluidas[i][j])):
                fechas_excluidas[i][j][k] = fechas_excluidas[i][j][k]-inicio_curso
                fechas_excluidas[i][j][k] = fechas_excluidas[i][j][k].days
    
    # Calcular F, V, K, Di
    F = fechas_excluidas
    V = plazos_examen_total
    
    K = calificaciones_por_asignatura
    Di = duracion_cursos
    cursos=[]
    pre_calendario=[]
    for i in range(len(plazos_examen_total)):
        cursos.append(Curso(len(plazos_examen_total[i]),F[i],V[i],K[i],Di[i]))
        
        pre_calendario.append(cursos[i].fit_to_date(inicio_cursos[i]))
        
    calendario ={}
    i=0
    j=0
    for clave, evaluaciones in detalles.items():
        
        clave_=(clave[0],clave[1],clave[2])
        for element in pre_calendario[i]:
                calendario[clave[0],clave[1],clave[2],j] = (element,asignaturas[j])
                
                
                j+=1
            
        i+=1
    
    return calendario
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
    print(calendario_procesado)
    process_data_and_save(calendario_procesado,"calendarios_optimizados.db")
def run_app():
    st.title('Optimización de Calendario Académico')
    if st.button('Optimizar Calendario'):
        main()

if __name__ == "__main__":
    
    run_app()
