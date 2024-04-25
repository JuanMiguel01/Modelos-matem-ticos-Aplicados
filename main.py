import streamlit as st
from menu import menu
from pages.auth import check_credentials ,get_user_role

if "role" not in st.session_state:
    st.session_state.role = None



# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role

def get_session():
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None
    return st.session_state

def login():
    session = get_session()
    
    st.title("Inicio de sesión de nuestra aplicacion para la creacion de calendarios de prueba")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if check_credentials(username, password):
            session["username"] = username
            session["role"] = get_user_role(username)
            st.success("Inicio de sesión exitoso.")
        else:
            st.error("Nombre de usuario o contraseña incorrectos.")

def main():
    session = get_session()
    if session["username"] is None:
        login()
    else:
        # Aquí puedes llamar a las funciones protegidas por roles
        if session["role"] == "admin":
            st.write("Bienvenido, administrador!")
            set_role
        elif session["role"] == "super-admin":
            st.write("Bienvenido, super administrador!")
            set_role
        else:
            st.write("Bienvenido, usuario!")
            st.write("Bienvenido ,usuario")

if __name__ == "__main__":
    main()


menu() # Render the dynamic menu!