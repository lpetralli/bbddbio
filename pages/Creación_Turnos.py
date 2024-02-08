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

def user_id_exists(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM usuarios WHERE id = %s"
            cur.execute(query, (id,))
            result = cur.fetchone()
            return result is not None
    finally:
        conn.close()

def insert_turno(id_usuario, id_doctor, fecha, hora, motivo_consulta):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO turnos (id_usuario, id_doctor, fecha, hora, motivo_consulta) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (id_usuario, id_doctor, fecha, hora, motivo_consulta))
            conn.commit()
    except psycopg2.Error as e:
        st.error(f"Se produjo un error al guardar el usuario: {e}")
    finally:
        conn.close()

# Interfaz de Streamlit
# Título y foto en la misma fila

st.image('labo.jpg')

st.title('✅ Registrar usuario ')

id_usuario = st.text_input("ID Usuario")
id_doctor = st.text_input("ID Doctor")
fecha = st.date_input("Fecha")
hora = st.time_input('Hora')
motivo_consulta= st.text_input("Motivo Consulta", max_chars=100)

if st.button('Guardar'):
    if not id_usuario or not id_doctor or not fecha or not hora:
        st.error("Por favor, completa todos los campos.")
    elif fecha <= datetime.today().date():
        st.error("La fecha del turno debe ser mayor o igual a hoy")
    elif user_id_exists(id_usuario) == False:
        st.error("El usuario no existe")
    else:
        insert_turno(id_usuario, id_doctor, fecha, hora, motivo_consulta)
        st.success("Turno registrado exitosamente.")
