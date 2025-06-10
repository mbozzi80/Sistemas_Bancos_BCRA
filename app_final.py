import streamlit as st
import pandas as pd
import requests
import re
from io import StringIO
from BCRA_.tabs import tab_resumen, tab_prestamos, tab_titulos, tab_depositos, tab_ratios, tab_descarga

# Configuración de la página
st.set_page_config(
    page_title="Sistema Bancario Argentino",
    page_icon="🏦",
    layout="wide"
)

# INICIALIZAR SESSION STATE PARA RECORDAR TAB ACTIVO
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # 0 = primer tab por defecto

# REEMPLAZAR el st.markdown actual por este CSS más específico:
st.markdown("""
<style>
/* Alinear números a la derecha - MÁS ESPECÍFICO */
div[data-testid="stDataFrame"] table td:not(:first-child),
.stDataFrame table td:not(:first-child),
.dataframe td:not(:first-child) {
    text-align: right !important;
    font-family: monospace !important;
}

/* Primera columna (nombres) a la izquierda */
div[data-testid="stDataFrame"] table td:first-child,
.stDataFrame table td:first-child,
.dataframe td:first-child {
    text-align: left !important;
}

/* Headers alineados */
div[data-testid="stDataFrame"] table th:not(:first-child),
.stDataFrame table th:not(:first-child),
.dataframe th:not(:first-child) {
    text-align: right !important;
}

/* Para st.metric también */
div[data-testid="metric-container"] > div > div:nth-child(2) {
    text-align: right !important;
}
</style>
""", unsafe_allow_html=True)

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
        # AGREGAR ESTAS 4 LÍNEAS NUEVAS:
        headers = {}
        if 'GITHUB_TOKEN' in st.secrets:
            headers = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}
        
        response = requests.get(url, headers=headers)  # ← AGREGAR headers aquí
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
        # AGREGAR ESTAS 4 LÍNEAS NUEVAS:
        headers = {}
        if 'GITHUB_TOKEN' in st.secrets:
            headers = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}
        
        response = requests.get(url, headers=headers)  # ← AGREGAR headers aquí
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df, periodo
    except Exception as e:
        st.error(f"Error al cargar datos en moneda constante: {e}")
        return None, None



# Título principal
st.title("🏦 Sistema Bancario Argentino - BCRA")
st.markdown("**La primera plataforma web de análisis bancario argentino con 20 años de datos**")

# SELECTOR DE TIPO DE DATOS
st.sidebar.header("⚙️ Configuración de Datos")

# Obtener período dinámico para el help text
periodo_dinamico = get_periodo_from_filename()

# DETECTAR CAMBIO EN SELECTOR (para mantener tab activo)
tipo_datos_key = "selector_tipo_datos"
if tipo_datos_key not in st.session_state:
    st.session_state[tipo_datos_key] = "Valores Históricos"

tipo_datos = st.sidebar.radio(
    "Selecciona el tipo de valores:",
    options=["Valores Históricos", "Moneda Constante"],
    help=f"""
    • **Valores Históricos**: Datos originales sin ajuste por inflación
    • **Moneda Constante**: Valores ajustados por inflación al período {periodo_dinamico}
    """,
    key=tipo_datos_key
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
    
    # CREAR TABS CON SESSION STATE PARA MANTENER TAB ACTIVO
    tab_names = [
        "📊 Resumen General", 
        "💰 Préstamos", 
        "📈 Títulos", 
        "💳 Depósitos", 
        "📊 Ratios", 
        "⬇️ Descarga"
    ]
    
    # Usar selectbox en sidebar para controlar tabs
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📂 Navegación")


    # Crear botones para cada tab
    for i, tab_name in enumerate(tab_names):
        # Aplicar estilo diferente al tab activo
        if i == st.session_state.active_tab:
            # Tab activo con color destacado
            if st.sidebar.button(f"➤ {tab_name}", key=f"tab_{i}", use_container_width=True):
                st.session_state.active_tab = i
                st.rerun()
        else:
            # Tab inactivo
            if st.sidebar.button(tab_name, key=f"tab_{i}", use_container_width=True):
                st.session_state.active_tab = i
                st.rerun()


    # Mostrar contenido según tab seleccionado
    selected_tab = st.session_state.active_tab  # ← Cambiar por esta línea
    
    if selected_tab == 0:
        st.markdown(f"## {tab_names[0]}")
        tab_resumen.render(df)
    elif selected_tab == 1:
        st.markdown(f"## {tab_names[1]}")
        tab_prestamos.render(df)
    elif selected_tab == 2:
        st.markdown(f"## {tab_names[2]}")
        tab_titulos.render(df)
    elif selected_tab == 3:
        st.markdown(f"## {tab_names[3]}")
        tab_depositos.render(df)
    elif selected_tab == 4:
        st.markdown(f"## {tab_names[4]}")
        tab_ratios.render(df)
    elif selected_tab == 5:
        st.markdown(f"## {tab_names[5]}")
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
    <div style='font-size: 0.8em;'>
    <strong>Valores Históricos:</strong><br>
    • Datos originales del BCRA<br>
    • Sin ajuste por inflación<br>
    • Útil para análisis nominal<br>
    • Fuente: GitHub
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"""
    <div style='font-size: 0.8em;'>
    <strong>Moneda Constante:</strong><br>
    • Ajustado por inflación (IPC)<br>
    • Base: {periodo_dinamico}<br>
    • Valores comparables en el tiempo<br>
    • Útil para análisis real<br>
    • Fuente: GitHub
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size: 0.8em; text-align: center;'>
🔗 <a href='https://github.com/mbozzi80/Sistemas_Bancos_BCRA' target='_blank'>Repositorio GitHub</a>
</div>
""", unsafe_allow_html=True)

