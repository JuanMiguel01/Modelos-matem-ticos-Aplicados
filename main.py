import streamlit as st
from pages import bienvenida, planificacion, calendario

pages = {
    "Bienvenida": bienvenida.app,
    "Planificación de Evaluaciones": planificacion.app,
    "Calendario de Exámenes": calendario.app,
}

page = st.sidebar.selectbox("Navegación", list(pages.keys()))

# Ejecuta la función correspondiente a la página seleccionada
pages[page]()