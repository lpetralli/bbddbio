import streamlit as st
import psycopg2
import pandas as pd

# Función para conectar a la base de datos
def connect_to_db():
    conn = psycopg2.connect(
        dbname='mpxkpnvb',
        user='mpxkpnvb',
        password='xF3SiYaL2rtKywEaWFkDm8MMVM76L1Bs',
        host='berry.db.elephantsql.com',
        port='5432'
    )
    return conn

# Función para buscar los turnos de un usuario por su apellido
def search_turnos_by_apellido(apellido):
    conn = connect_to_db()
    query = "SELECT * FROM turnos WHERE id_usuario IN (SELECT id FROM usuarios WHERE apellido = %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(query, (apellido,))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

# Interfaz de Streamlit para la página de visualización de turnos

st.title('Visualización de Turnos por Apellido')

apellido = st.text_input("Ingrese su apellido:")

if apellido:
    turnos = search_turnos_by_apellido(apellido)
    if turnos:
        st.write("Turnos encontrados:")
        df_turnos = pd.DataFrame(turnos, columns=['ID', 'ID Usuario', 'ID Doctor', 'Fecha', 'Hora', 'Motivo Consulta'])
        st.write(df_turnos)
    else:
        st.warning("No se encontraron turnos asociados a ese apellido.")


