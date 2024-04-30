
import streamlit as st
import sqlite3
from menu import menu_with_redirect
from pages.optimizar import main as run_main
menu_with_redirect()


# Función para ejecutar el script de optimización y mostrar los resultados
def run_optimization():
    
    run_main()
    
# Función principal de Streamlit
def main():
    st.title('Crear Calendario Académico para todos los cursos ')
    run_button = st.button('Ejecutar Optimización')
    
    if run_button:

        run_optimization()
        st.write ("Optimización completada")

if __name__ == "__main__":
    main()
