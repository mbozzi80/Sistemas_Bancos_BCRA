import streamlit as st
import pandas as pd
import requests
import re
from io import StringIO
from BCRA_.tabs import tab_resumen, tab_prestamos, tab_titulos, tab_depositos, tab_ratios, tab_descarga

@st.cache_data
def get_periodo_from_filename():
    """Extrae el período del nombre del archivo CSV de moneda constante"""
    url = "https://api.github.com/repos/mbozzi80/Sistemas_Bancos_BCRA/contents/"
    try:
        response = requests.get(url)
        files = response.json()
        for file in files:
            if file['name'].startswith('bcra_datos_constantes_'):
                match = re.search(r'bcra_datos_constantes_(\d{6})\.csv', file['name'])
                if match:
                    return match.group(1)
        return "202502"  # Fallback
    except:
        return "202502"  # Fallback

@st.cache_data
def load_historical_data():
    """Carga datos históricos desde GitHub"""
    url = "https://raw.githubusercontent.com/mbozzi80/Sistemas_Bancos_BCRA/master/bcra_datos_finales.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"Error al cargar datos históricos: {e}")
        return None

@st.cache_data
def load_constant_data():
    """Carga datos en moneda constante desde GitHub"""
    # Obtener período dinámicamente
    periodo = get_periodo_from_filename()
    url = f"https://raw.githubusercontent.com/mbozzi80/Sistemas_Bancos_BCRA/master/bcra_datos_constantes_{periodo}.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df, periodo
    except Exception as e:
        st.error(f"Error al cargar datos en moneda constante: {e}")
        return None, None

# Configuración de la página
st.set_page_config(
    page_title="Sistema Bancario Argentino - BCRA",
    page_icon="🏦",
    layout="wide"
)

# Título principal
st.title("🏦 Sistema Bancario Argentino - BCRA")
st.markdown("**La primera plataforma web de análisis bancario argentino con 20 años de datos**")

# SELECTOR DE TIPO DE DATOS
st.sidebar.header("⚙️ Configuración de Datos")

# Obtener período dinámico para el help text
periodo_dinamico = get_periodo_from_filename()

tipo_datos = st.sidebar.radio(
    "Selecciona el tipo de valores:",
    options=["Valores Históricos", "Moneda Constante"],
    help=f"""
    • **Valores Históricos**: Datos originales sin ajuste por inflación
    • **Moneda Constante**: Valores ajustados por inflación al período {periodo_dinamico}
    """
)

# Cargar datos según selección
if tipo_datos == "Valores Históricos":
    st.sidebar.info("📊 Cargando datos históricos desde GitHub...")
    with st.spinner("Cargando datos históricos..."):
        df = load_historical_data()
        periodo_base = None
        
elif tipo_datos == "Moneda Constante":
    st.sidebar.info("💰 Cargando datos en moneda constante...")
    with st.spinner("Cargando datos en moneda constante..."):
        df, periodo_base = load_constant_data()

# Mostrar información de los datos cargados
if df is not None:
    if tipo_datos == "Valores Históricos":
        st.success(f"✅ {len(df):,} registros cargados - **Valores Históricos**")
        st.info(f"📊 Datos desde {df['Periodo'].min()} hasta {df['Periodo'].max()}")
        
    else:  # Moneda Constante
        # Formatear período para mostrar (202502 -> "febrero 2025")
        año = periodo_base[:4]
        mes_num = periodo_base[4:]
        meses = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        mes_nombre = meses[int(mes_num)] if int(mes_num) <= 12 else f"mes {mes_num}"
        
        st.success(f"✅ {len(df):,} registros cargados - **Moneda Constante** (base: {periodo_base})")
        st.info(f"💰 Todos los valores expresados en pesos de {mes_nombre} {año}")
        st.warning("⚠️ Los valores han sido ajustados por inflación para comparabilidad temporal")
    
    # Mostrar información adicional en sidebar
    st.sidebar.success("✅ Datos cargados correctamente")
    st.sidebar.metric("📈 Total de registros", f"{len(df):,}")
    st.sidebar.metric("🏦 Bancos únicos", df['Entidad'].nunique())
    st.sidebar.metric("📅 Períodos", f"{df['Periodo'].min()} - {df['Periodo'].max()}")
    
    if tipo_datos == "Moneda Constante":
        año = periodo_base[:4]
        mes_num = periodo_base[4:]
        meses = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        mes_nombre = meses[int(mes_num)] if int(mes_num) <= 12 else f"mes {mes_num}"
        st.sidebar.metric("💰 Base monetaria", f"{mes_nombre.title()} {año}")
    
    # 6 tabs principales
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
        if tipo_datos == "Moneda Constante":
            año = periodo_base[:4]
            mes_num = periodo_base[4:]
            meses = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
                    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            mes_nombre = meses[int(mes_num)] if int(mes_num) <= 12 else f"mes {mes_num}"
            st.info(f"💰 Archivo en moneda constante - Base: {mes_nombre} {año}")
        tab_descarga.render(df)

else:
    st.error("❌ No se pudieron cargar los datos")
    st.info("💡 Verifica la conectividad a internet y que los archivos estén disponibles en GitHub")

# Footer con información contextual
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Información")

if tipo_datos == "Valores Históricos":
    st.sidebar.markdown("""
    **Valores Históricos:**
    - Datos originales del BCRA
    - Sin ajuste por inflación
    - Útil para análisis nominal
    - Fuente: GitHub
    """)
else:
    st.sidebar.markdown(f"""
    **Moneda Constante:**
    - Ajustado por inflación (IPC)
    - Base: {periodo_dinamico}
    - Valores comparables en el tiempo
    - Útil para análisis real
    - Fuente: GitHub
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("🔗 [Repositorio GitHub](https://github.com/mbozzi80/Sistemas_Bancos_BCRA)")

