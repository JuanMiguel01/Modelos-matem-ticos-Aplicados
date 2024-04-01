
import streamlit as st
import sqlite3
def obtener_asignaturas(carrera, año, curso):
    
    con = sqlite3.connect("mi_base_de_datos.db") 
    cur = con.cursor()
    
    cur.execute('''SELECT asignatura, fecha_inicio, fecha_fin 
                   FROM evaluaciones 
                   WHERE carrera = ? AND año = ? AND curso = ?''', 
                (carrera, año, curso))
    
    asignaturas = cur.fetchall()
    con.close()
    
    return asignaturas
def app():
    st.title("Selecciona tu Calendario")

    carreras = ["Ciencias de la Computación", "Ciencia de Datos", "Matemática"]
    años = list(range(1, 6)) # Ajusta el rango según sea necesario
    cursos = ["2000-2001", "2001-2002", "2002-2003", "2003-2004", "2004-2005", "2005-2006", "2006-2007", "2007-2008", "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026", "2026-2027"]

    carrera_seleccionada = st.selectbox("Selecciona la carrera:", carreras)
    año_seleccionado = st.selectbox("Selecciona el año:", años)
    curso_seleccionado = st.selectbox("Selecciona el curso:", cursos)

    if st.button("Mostrar Calendario"):
        asignaturas = obtener_asignaturas(carrera_seleccionada, año_seleccionado, curso_seleccionado)
       
        if asignaturas:
            st.markdown(f"## Calendario para {carrera_seleccionada} {año_seleccionado}")
            # Crear una lista de listas para usar en st.table
            data = [[asignatura, fecha_inicio, fecha_fin] for asignatura, fecha_inicio, fecha_fin in asignaturas]
            # Mostrar la tabla sin el argumento 'headers'
            st.table(data)
        else:
            st.write("No se encontraron asignaturas para la selección.")