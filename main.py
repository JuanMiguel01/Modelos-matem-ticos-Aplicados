import streamlit as st
from pages import bienvenida, planificacion, calendario

PAGES = {
    "Bienvenida": bienvenida.app,
    "Planificación de Evaluaciones": planificacion.app,
    "Calendario de Exámenes": calendario.app,
}

def main():
    st.sidebar.title('Navegación')
    selection = st.sidebar.radio("Ir a", list(PAGES.keys()))
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()
