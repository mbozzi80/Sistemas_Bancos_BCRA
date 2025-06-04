import streamlit as st
import pandas as pd
import requests
from io import StringIO
from BCRA_.tabs import tab_resumen, tab_prestamos, tab_titulos, tab_depositos, tab_ratios, tab_descarga

@st.cache_data
def load_processed_data():
    """Carga archivo YA PROCESADO desde GitHub"""
    # URL directa del archivo en tu repositorio
    url = "https://raw.githubusercontent.com/mbozzi80/Sistemas_Bancos_BCRA/master/bcra_datos_finales.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

# Configuración de la página
st.set_page_config(
    page_title="Sistema Bancario Argentino - BCRA",
    page_icon="🏦",
    layout="wide"
)

# Título principal
st.title("🏦 Sistema Bancario Argentino - BCRA")
st.markdown("**La primera plataforma web de análisis bancario argentino con 10 años de datos**")

# Cargar datos PRE-PROCESADOS (súper rápido)
with st.spinner("Cargando datos procesados..."):
    df = load_processed_data()

if df is not None:
    st.success(f"✅ {len(df)} registros cargados con denominaciones incluidas!")
    st.info(f"📊 Datos desde {df['Periodo'].min()} hasta {df['Periodo'].max()}")
    
    # 6 tabs funcionando instantáneamente
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Resumen General", 
        "💰 Préstamos", 
        "📈 Títulos", 
        "💳 Depósitos", 
        "📊 Ratios", 
        "⬇️ Descarga"
    ])
    
    # Ejecutar cada tab
    with tab1:
        tab_resumen.render(df)
    
    with tab2:
        tab_prestamos.render(df)
    
    with tab3:
        tab_titulos.render(df)
    
    with tab4:
        tab_depositos.render(df)
    
    with tab5:
        tab_ratios.render(df)
    
    with tab6:
        tab_descarga.render(df)

else:
    st.error("❌ No se pudieron cargar los datos")

    