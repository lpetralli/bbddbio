import streamlit as st
import psycopg2
from datetime import datetime

# Configuración de la conexión
def get_db_connection():
    user = 'mpxkpnvb'
    password = 'xF3SiYaL2rtKywEaWFkDm8MMVM76L1Bs'
    host = 'berry.db.elephantsql.com'
    port = '5432'
    dbname = 'mpxkpnvb'
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

def email_exists(email):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM usuarios WHERE email = %s"
            cur.execute(query, (email,))
            result = cur.fetchone()
            return result is not None
    finally:
        conn.close()

def insert_user(nombre, apellido, email, fecha_nacimiento):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO usuarios (nombre, apellido, email, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (nombre, apellido, email, fecha_nacimiento))
            conn.commit()
    except psycopg2.Error as e:
        st.error(f"Se produjo un error al guardar el usuario: {e}")
    finally:
        conn.close()

# Interfaz de Streamlit
# Título y foto en la misma fila

st.image('labo.jpg')

st.title('✅ Registrar usuario ')

nombre = st.text_input("Nombre", max_chars=50)
apellido = st.text_input("Apellido", max_chars=50)
email = st.text_input("Email", max_chars=100)
fecha_nacimiento = st.date_input("Fecha de Nacimiento", max_value=datetime.today())

if st.button('Guardar'):
    if not nombre or not apellido or not email:
        st.error("Por favor, completa todos los campos.")
    elif fecha_nacimiento >= datetime.today().date():
        st.error("La fecha de nacimiento debe ser anterior a la fecha actual.")
    elif email_exists(email):
        st.error("El email ya está registrado. Por favor, utiliza otro email.")
    else:
        insert_user(nombre, apellido, email, fecha_nacimiento)
        st.success("Usuario registrado exitosamente.")
