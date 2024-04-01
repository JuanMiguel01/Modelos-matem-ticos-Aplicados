import hashlib
import os
import sqlite3
import streamlit as st
def hash_password(password):
    # Hash the password with a salt
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key

def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    if result:
        stored_password = result[0]
        salt = stored_password[:32]
        key = stored_password[32:]
        return key == hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return False
def get_user_role(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def requires_role(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if get_user_role(st.session_state.username) == role:
                return func(*args, **kwargs)
            else:
                st.error("No tienes permiso para acceder a esta página.")
        return wrapper
    return decorator
