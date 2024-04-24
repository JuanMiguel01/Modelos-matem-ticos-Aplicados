
import streamlit as st
import sqlite3
from sqlite3 import Error
from menu import menu_with_redirect
menu_with_redirect()
import streamlit as st

def app():
    st.title("¿Estás seguro de que quieres salir?")
    st.write("Al salir, perderás tu sesión actual.")
    
    if st.button("Sí, salir"):
        # Aquí se ejecuta el código de logout
        st.session_state.role = None
        st.session_state.username = None
        # Redirigir al usuario a la página principal
        st.experimental_rerun()
app()