import streamlit as st
from menu import menu_with_redirect
import sqlite3
from pages.auth import hash_password
# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.role not in ["super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is available to super-admins")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")

# Formulario para añadir un nuevo admin
with st.form(key='add_admin_form'):
    username = st.text_input("Nombre de usuario del nuevo admin")
    password = st.text_input("Contraseña (opcional, se usará 'admin' por defecto)")
    submit_button = st.form_submit_button(label="Añadir admin")

if submit_button:
    if not password:
        password = "admin" # Contraseña por defecto si no se proporciona
    hashed_password = hash_password(password) # Hashear la contraseña
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO users (username, password, role)
                     VALUES (?, ?, ?)''', (username, hashed_password, "admin"))
        conn.commit()
        st.success(f"Admin {username} añadido exitosamente.")
    except sqlite3.IntegrityError:
        st.error(f"El nombre de usuario {username} ya existe.")
    conn.close()
