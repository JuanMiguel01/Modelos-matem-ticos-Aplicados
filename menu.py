import streamlit as st


def authenticated_menu():
    st.sidebar.page_link("pages/salir.py", label="Salir")
    st.sidebar.page_link("pages/user.py", label="Your profile")
    st.sidebar.page_link("pages/calendario.py", label="Calendario")
    st.sidebar.page_link("pages/calificacion.py", label="Calificacion")
    if st.session_state.role in [ "super-admin"]:
        st.sidebar.page_link("pages/crear_calendario.py", label="Crear los calendarios")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage users")
        st.sidebar.page_link("pages/planificacion.py", label="Planificacion")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )
    



def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("main.py", label="Log in")



def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("main.py")
    menu()