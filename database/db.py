import psycopg2
import streamlit as st

def get_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets["DB_PORT"],
            sslmode="require",
            connect_timeout=10
        )
        return conn
    except Exception as e:
        st.error(f"DB CONNECTION ERROR: {e}")
        raise

def init_db():
    pass
