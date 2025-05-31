import streamlit as st
import pandas as pd
import requests
from io import StringIO

@st.cache_data
def load_data():
    """Descarga y carga el archivo h_imput.txt desde Dropbox"""
    url = "https://www.dropbox.com/scl/fi/xhbjjclp7sn33ak48nge5/h_imput.txt?rlkey=h3dfmnt9skshzdekrarvetnj1&st=ft0127ge&dl=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        
        # Si es un CSV, usa esto:
        # data = pd.read_csv(StringIO(response.text))
        
        # Si es texto plano, usa esto:
        data = response.text
        
        return data
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# En tu aplicación principal:
st.title("Mi aplicación con datos de h_imput.txt")

with st.spinner("Cargando datos..."):
    data = load_data()

if data is not None:
    st.success("Datos cargados correctamente!")
    # Aquí procesas tus datos
    st.text(f"Primeros 500 caracteres: {str(data)[:500]}")
else:
    st.error("No se pudieron cargar los datos")