import streamlit as st
from menu import menu_with_redirect
from pages.auth import hash_password
import sqlite3
# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("This page is available to all users")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")

# Formulario para modificar la cuenta del usuario
with st.form(key='update_account_form'):
    username = st.text_input("Nuevo nombre de usuario", value=st.session_state.username)
    password = st.text_input("Nueva contraseña", type="password")
    submit_button = st.form_submit_button(label="Actualizar cuenta")

if submit_button:
    if password:
        hashed_password = hash_password(password) # Hashear la nueva contraseña
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            # Actualizar el nombre de usuario y la contraseña
            c.execute('''UPDATE users SET username = ?, password = ? WHERE username = ?''',
                      (username, hashed_password, st.session_state.username))
            conn.commit()
            st.success("Cuenta actualizada exitosamente.")
            # Actualizar el estado de la sesión con el nuevo nombre de usuario
            st.session_state.username = username
        except sqlite3.Error as e:
            st.error(f"Error al actualizar la cuenta: {e}")
        conn.close()
    else:
        st.error("Por favor, ingrese una nueva contraseña.")
