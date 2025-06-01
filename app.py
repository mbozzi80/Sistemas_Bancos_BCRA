import streamlit as st
import requests
from BCRA_.tools import procesar_datos_bcra_con_nombres
from BCRA_.tabs import tab_resumen, tab_prestamos, tab_titulos, tab_depositos, tab_ratios, tab_descarga

@st.cache_data
def load_data():
    """Descarga y carga el archivo h_imput.txt desde Dropbox"""
    url = "https://www.dropbox.com/scl/fi/xhbjjclp7sn33ak48nge5/h_imput.txt?rlkey=h3dfmnt9skshzdekrarvetnj1&st=ft0127ge&dl=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Configuración de la página
st.set_page_config(
    page_title="Sistema Bancario Argentino - BCRA",
    page_icon="🏦",
    layout="wide"
)

# Título principal
st.title("🏦 Sistema Bancario Argentino - BCRA")
st.markdown("**La primera plataforma web de análisis bancario argentino con 20 años de datos**")

# Cargar datos una sola vez
with st.spinner("Cargando datos del BCRA..."):
    texto_crudo = load_data()

if texto_crudo is not None:
    st.success("✅ Datos descargados correctamente!")
    
    with st.spinner("Procesando datos bancarios y cargando denominaciones..."):
        df_procesado = procesar_datos_bcra_con_nombres(texto_crudo)
    
    if df_procesado is not None:
        st.success("✅ Datos procesados correctamente con nombres de bancos!")
        
        # Crear las tabs/pestañas
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Resumen General", 
            "💰 Préstamos", 
            "📈 Títulos", 
            "💳 Depósitos", 
            "📊 Ratios", 
            "⬇️ Descarga"
        ])
        
        # Ejecutar cada tab desde su módulo correspondiente
        with tab1:
            tab_resumen.render(df_procesado)
        
        with tab2:
            tab_prestamos.render(df_procesado)
        
        with tab3:
            tab_titulos.render(df_procesado)
        
        with tab4:
            tab_depositos.render(df_procesado)
        
        with tab5:
            tab_ratios.render(df_procesado)
        
        with tab6:
            tab_descarga.render(df_procesado)
    
    else:
        st.error("❌ Error al procesar los datos")
else:
    st.error("❌ No se pudieron cargar los datos")