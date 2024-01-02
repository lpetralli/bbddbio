import streamlit as st
import psycopg2
import pandas as pd

# Configuración de la conexión: reemplaza con tus propios valores
user = 'mpxkpnvb'
password = 'xF3SiYaL2rtKywEaWFkDm8MMVM76L1Bs'
host = 'berry.db.elephantsql.com'
port = '5432'
dbname = 'mpxkpnvb'

# Función para conectarse a la base de datos
@st.cache(hash_funcs={psycopg2.extensions.connection: id})
def connect_to_db():
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

# Interfaz de Streamlit
st.title('Interfaz de consulta a la base de datos')

# Conectar a la base de datos
conn = connect_to_db()

# Caja de texto para la consulta SQL
query = st.text_area("Ingrese su consulta SQL aquí:")

# Botón para ejecutar la consulta
if st.button('Ejecutar consulta'):
    try:
        data = pd.read_sql_query(query, conn)
        st.write(data)
    except Exception as e:
        st.error(f"Se produjo un error al ejecutar la consulta: {e}")
