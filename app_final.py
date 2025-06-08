import streamlit as st
import pandas as pd
import requests
from io import StringIO
from BCRA_.tabs import tab_resumen, tab_prestamos, tab_titulos, tab_depositos, tab_ratios, tab_descarga

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
    url = "https://raw.githubusercontent.com/mbozzi80/Sistemas_Bancos_BCRA/master/bcra_datos_constantes_202502.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df, "202502"
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

tipo_datos = st.sidebar.radio(
    "Selecciona el tipo de valores:",
    options=["Valores Históricos", "Moneda Constante"],
    help="""
    • **Valores Históricos**: Datos originales sin ajuste por inflación
    • **Moneda Constante**: Valores ajustados por inflación al período 202502
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
# Mostrar información de los datos cargados
if df is not None:
    # DEBUG: Mostrar columnas disponibles
    st.write("**DEBUG - Columnas disponibles:**")
    st.write(df.columns.tolist())
    
    if tipo_datos == "Valores Históricos":
        st.success(f"✅ {len(df):,} registros cargados - **Valores Históricos**")
        st.info(f"📊 Datos desde {df['Periodo'].min()} hasta {df['Periodo'].max()}")
        
    else:  # Moneda Constante
        st.success(f"✅ {len(df):,} registros cargados - **Moneda Constante** (base: {periodo_base})")
        st.info(f"💰 Todos los valores expresados en pesos de febrero 2025")
        st.warning("⚠️ Los valores han sido ajustados por inflación para comparabilidad temporal")
    
    # Mostrar información adicional en sidebar
    st.sidebar.success("✅ Datos cargados correctamente")
    st.sidebar.metric("📈 Total de registros", f"{len(df):,}")
    st.sidebar.metric("🏦 Bancos únicos", df['Entidad'].nunique())
    st.sidebar.metric("📅 Períodos", f"{df['Periodo'].min()} - {df['Periodo'].max()}")
    
    if tipo_datos == "Moneda Constante":
        st.sidebar.metric("💰 Base monetaria", "Febrero 2025")
    
    # COMENTAR TEMPORALMENTE LOS TABS PARA DEBUG
    st.write("**DEBUG - Primeras 5 filas:**")
    st.dataframe(df.head())

    
    # Mostrar información adicional en sidebar
    st.sidebar.success("✅ Datos cargados correctamente")
    st.sidebar.metric("📈 Total de registros", f"{len(df):,}")
    st.sidebar.metric("🏦 Bancos únicos", df['Entidad'].nunique())
    st.sidebar.metric("📅 Períodos", f"{df['Periodo'].min()} - {df['Periodo'].max()}")
    
    if tipo_datos == "Moneda Constante":
        st.sidebar.metric("💰 Base monetaria", "Febrero 2025")
    
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
        # Pasar información adicional al tab de descarga
        if tipo_datos == "Moneda Constante":
            st.info(f"💰 Archivo en moneda constante - Base: febrero 2025")
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
    st.sidebar.markdown("""
    **Moneda Constante:**
    - Ajustado por inflación (IPC)
    - Base: Febrero 2025
    - Valores comparables en el tiempo
    - Útil para análisis real
    - Fuente: GitHub
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("🔗 [Repositorio GitHub](https://github.com/mbozzi80/Sistemas_Bancos_BCRA)")

